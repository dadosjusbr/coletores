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
	var result map[string]interface{}
	err = json.Unmarshal(byteValue, &result)
	if err != nil {
		return nil, fmt.Errorf("error trying to unmarshal json: %q", err)
	}
	return result, nil
}

// getValue tries to retrieve a value from map with key, return nil if none found.
func getValue(m map[string]interface{}, key string) interface{} {
	v, ok := m[key]
	if ok {
		return v
	}
	return nil
}

// getMap returns a map from map(m) using key. returns error if string is not found.
func getMap(m map[string]interface{}, key string) (map[string]interface{}, error) {
	rm := getValue(m, key)
	if result, ok := rm.(map[string]interface{}); ok {
		return result, nil
	}
	return nil, fmt.Errorf("value not retrieved or is not a map[string]interface{}(key: %s)", key)
}

// getSliceOfMaps returns a slice of maps from map(m) using key. returns error if string is not found.
func getSliceOfMaps(m map[string]interface{}, key string) ([]map[string]interface{}, error) {
	rm := getValue(m, key)
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
	value := getValue(m, key)
	valueStr, ok := value.(string)
	if value == nil || !ok {
		if valueF, ok := value.(float64); ok {
			valueStr = fmt.Sprintf("%.0f", valueF)
		} else {
			return fmt.Errorf("value not retrieved or is not a string(key: %s, value: %v)", key, value)
		}
	}
	*v = valueStr
	return nil
}

// getFloat64 retrieves a float64 from map using key and saves it in "v". returns error if float is not found.
func getFloat64(v interface{}, m map[string]interface{}, key string) error {
	value := getValue(m, key)
	float, ok := value.(float64)
	if value == nil || !ok {
		return fmt.Errorf("value not retrieved or is not a float64(key: %s, value: %v)", key, value)
	}
	if v, ok := v.(*float64); ok {
		*v = float
		return nil
	}
	if v, ok := v.(*(*float64)); ok {
		*v = &float
		return nil
	}
	return fmt.Errorf("paremeter v is not a *float64 or **float64")
}

// getPointerValue get float value or nil from pointer
func getPointerValue(p *float64) float64 {
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
