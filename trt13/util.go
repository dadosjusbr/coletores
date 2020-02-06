package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

// readJSON takes a filepath that should contain a json file and returns it as a map.
func readJSON(filePath string) (map[string]interface{}, error) {
	jsonFile, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("error trying to open file at (%s) : %q", filePath, err)
	}
	defer jsonFile.Close()

	byteValue, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		return nil, fmt.Errorf("error trying to read file at (%s) to []byte : %q", filePath, err)
	}

	var result map[string]interface{}
	err = json.Unmarshal(byteValue, &result)
	if err != nil {
		return nil, fmt.Errorf("error trying to unmarshal json: %q", err)
	}
	return result, nil
}

// findNil verifies if map contains any nil values.
func findNil(m map[string]interface{}) (string, bool) {
	for k, v := range m {
		if v == nil && k != "matricula" {
			return k, true
		}
		switch v.(type) {
		case map[string]interface{}:
			k, found := findNil(v.(map[string]interface{}))
			if found && k != "matricula" {
				return k, true
			}
		}
	}
	return "", false
}

// getMap returns a map from map(m) using key. returns error if string is not found.
func getMap(m map[string]interface{}, key string) (map[string]interface{}, error) {
	rm := m[key]
	if result, ok := rm.(map[string]interface{}); ok {
		return result, nil
	}
	return nil, fmt.Errorf("value not retrieved or is not a map[string]interface{}(key: %s)", key)
}

// getSliceOfMaps returns a slice of maps from map(m) using key. returns error if string is not found.
func getSliceOfMaps(m map[string]interface{}, key string) ([]map[string]interface{}, error) {
	rm := m[key]
	var result []map[string]interface{}
	if slice, ok := rm.([]interface{}); ok {
		for i, v := range slice {
			if cm, ok := v.(map[string]interface{}); ok {
				result = append(result, cm)
			} else {
				return nil, fmt.Errorf("%d ith element of slice is not a map[string]interface{}", i)
			}
		}
		return result, nil
	}
	return nil, fmt.Errorf("value not retrieved or is not a map[string]interface{}(key: %s)", key)
}

// getPointerValue returns float value or 0 if nil pointer
func getFloat64Value(p *float64) float64 {
	if p == nil {
		return 0
	}
	return *p
}

// sumMapValues returns the sum of all the values from the map.
func sumMapValues(m map[string]float64) float64 {
	var sum float64
	for _, v := range m {
		sum += v
	}
	return sum
}

// logError prints to Stderr
func logError(format string, args ...interface{}) {
	time := fmt.Sprintf("%s: ", time.Now().Format(time.RFC3339))
	fmt.Fprintf(os.Stderr, time+format+"\n", args...)
}
