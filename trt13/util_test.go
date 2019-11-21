package main

import (
	"encoding/json"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

const getValueSample = `{"float64":872.0,
"string":"ABIA",
"latin": "àôãõç",
"map": {"a": "a"},
"list": ["1", "2", "3"],
"mapSlice": [{}]
}`

func jsonMap(j string) (map[string]interface{}, error) {
	var empSample map[string]interface{}
	err := json.Unmarshal([]byte(j), &empSample)
	return empSample, err
}

func Test_readJSON(t *testing.T) {
	f, err := os.Create("./_test.json")
	assert.NoError(t, err)
	_, err = f.Write([]byte(getValueSample))
	assert.NoError(t, err)

	actual, err := readJSON("./_test.json")
	assert.NoError(t, err)
	expected, err := jsonMap(getValueSample)
	assert.NoError(t, err)
	assert.Equal(t, actual, expected)
	assert.NoError(t, os.Remove("./_test.json"))
	_, err = readJSON("_invalidPath")
	assert.Error(t, err)
}

func Test_getMap(t *testing.T) {
	sample, err := jsonMap(getValueSample)
	assert.NoError(t, err)
	m, err := getMap(sample, "map")
	assert.NoError(t, err)
	assert.Equal(t, map[string]interface{}{"a": "a"}, m)
	_, err = getMap(sample, "")
	assert.Error(t, err)
}

func Test_getSliceOfMap(t *testing.T) {
	sample, err := jsonMap(getValueSample)
	assert.NoError(t, err)
	_, err = getSliceOfMaps(sample, "map")
	assert.Error(t, err)
	_, err = getSliceOfMaps(sample, "list")
	assert.Error(t, err)
	m, err := getSliceOfMaps(sample, "mapSlice")
	assert.NoError(t, err)
	assert.Equal(t, []map[string]interface{}{{}}, m)
}

func Test_findNil(t *testing.T) {
	tests := []struct {
		name      string
		arg       map[string]interface{}
		wantValue string
		wantOK    bool
	}{
		{"find nil in map", map[string]interface{}{"a": nil}, "a", true},
		{"no nil in map", map[string]interface{}{"a": map[string]interface{}{"b": "c"}}, "", false},
		{"nil in inner map", map[string]interface{}{"a": map[string]interface{}{"b": nil}}, "b", true},
		{"nil and map", map[string]interface{}{"e": nil, "a": map[string]interface{}{"b": "c"}, "c": "d", "f": "d"}, "e", true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, ok := findNil(tt.arg)
			if got != tt.wantValue {
				t.Errorf("findNil() got = %v, want %v", got, tt.wantValue)
			}
			if ok != tt.wantOK {
				t.Errorf("findNil() ok = %v, want %v", ok, tt.wantOK)
			}
		})
	}
}
