package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
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

// getString retrieves a string from map using key, saves it in "v". returns error if string is not found.
func getString(v *string, m map[string]interface{}, key string) error {
	value, ok := m[key]
	if !ok {
		return fmt.Errorf("Value couldn't be retrieved: key %s", key)
	}

	if ok && value == nil {
		return nil
	}

	switch value := value.(type) {
	case string:
		*v = value
		return nil
	case float64:
		*v = fmt.Sprintf("%.0f", value)
		return nil
	default:
		return fmt.Errorf("value not retrieved or is not a string(key: %s, value: %v)", key, value)
	}
}

// getFloat64 retrieves a float64 from map using key and saves it in "v". returns error if float is not found.
func getFloat64(v interface{}, m map[string]interface{}, key string) error {
	value := m[key]
	float, ok := value.(float64)
	if value == nil || !ok {
		return fmt.Errorf("value not retrieved or is not a float64(key: %s, value: %v)", key, value)
	}
	switch v := v.(type) {
	case *float64:
		*v = float
		return nil
	case *(*float64):
		*v = &float
		return nil
	default:
		return fmt.Errorf("paremeter v is not a *float64 or **float64")
	}
}

// getPointerValue returns float value or 0 if nil pointer
func getFloat64Value(p *float64) float64 {
	if p == nil {
		return 0
	}
	return *p
}

// getStringValue returns the string value or empty string if nil pointer
func getStringValue(p *string) string {
	if p == nil {
		return ""
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
