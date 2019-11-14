package main

import (
	"encoding/json"
	"reflect"
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

func jsonExample(j string) (map[string]interface{}, error) {
	var empSample map[string]interface{}
	err := json.Unmarshal([]byte(j), &empSample)
	return empSample, err
}

func Test_getMap(t *testing.T) {
	sample, err := jsonExample(getValueSample)
	assert.NoError(t, err)
	m, err := getMap(sample, "map")
	assert.NoError(t, err)
	assert.Equal(t, map[string]interface{}{"a": "a"}, m)
	_, err = getMap(sample, "")
	assert.Error(t, err)
}

func Test_getSliceOfMap(t *testing.T) {
	sample, err := jsonExample(getValueSample)
	assert.NoError(t, err)
	_, err = getSliceOfMaps(sample, "map")
	assert.Error(t, err)
	_, err = getSliceOfMaps(sample, "list")
	assert.Error(t, err)
	m, err := getSliceOfMaps(sample, "mapSlice")
	assert.NoError(t, err)
	assert.Equal(t, []map[string]interface{}{{}}, m)
}

func Test_getString(t *testing.T) {
	sample, err := jsonExample(getValueSample)
	assert.NoError(t, err)
	var result string
	assert.NoError(t, getString(&result, sample, "string"))
	assert.Equal(t, "ABIA", result)
	assert.NoError(t, getString(&result, sample, "latin"))
	assert.Equal(t, "àôãõç", result)
	assert.NoError(t, getString(&result, sample, "float64"))
	assert.Equal(t, "872", result)
	assert.Error(t, getString(&result, sample, "map"))
}

func Test_getValue(t *testing.T) {
	sample, err := jsonExample(getValueSample)
	assert.NoError(t, err)
	type args struct {
		m   map[string]interface{}
		key string
	}
	tests := []struct {
		name string
		args args
		want interface{}
	}{
		{"float64", args{sample, `float64`}, 872.0},
		{"string", args{sample, `string`}, "ABIA"},
		{"map", args{sample, `map`}, map[string]interface{}{"a": "a"}},
		{"list", args{sample, `list`}, []interface{}{"1", "2", "3"}},
		{"not found", args{sample, `nil`}, nil},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := getValue(tt.args.m, tt.args.key)
			if !reflect.DeepEqual(got, tt.want) {
				t.Errorf("getValue() = %v (%T), want %v (%T)", got, got, tt.want, tt.want)
			}
		})
	}
}

func Test_getFloat64(t *testing.T) {
	var float float64
	var pointer *float64
	sample, err := jsonExample(getValueSample)
	assert.NoError(t, err)

	type args struct {
		v   interface{}
		m   map[string]interface{}
		key string
	}
	tests := []struct {
		name    string
		args    args
		wantErr bool
		want    float64
	}{
		{"not found", args{&float, sample, ""}, true, 0},
		{"not a float", args{&float, sample, "string"}, true, 0},
		{"invalid v paremeter", args{nil, sample, "float64"}, true, 0},
		{"validFloat", args{&float, sample, "float64"}, false, 872.0},
		{"validFloat to pointer", args{&pointer, sample, "float64"}, false, 872.0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if err := getFloat64(tt.args.v, tt.args.m, tt.args.key); (err != nil) != tt.wantErr {
				t.Fatalf("retrieveFloat() error = %v, wantErr %v", err, tt.wantErr)
			}
			if !tt.wantErr {
				if v, ok := tt.args.v.(**float64); ok {
					if *(*v) != tt.want {
						t.Fatalf("retrieveFloat() want %f, have %f", tt.want, *(*v))
					}
				}
				if v, ok := tt.args.v.(*float64); ok {
					if *v != tt.want {
						t.Fatalf("retrieveFloat() want %f, have %f", tt.want, *v)
					}
				}
			}
		})
	}
}
