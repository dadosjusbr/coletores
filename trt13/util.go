package main

import "fmt"

func getValue(m map[string]interface{}, key string) interface{} {
	v, ok := m[key]
	if ok {
		return v
	}
	return nil
}

func getMap(m map[string]interface{}, key string) (map[string]interface{}, error) {
	rm := getValue(m, key)
	if result, ok := rm.(map[string]interface{}); ok {
		return result, nil
	}
	return nil, fmt.Errorf("value not retrieved or is not a map[string]interface{}(key: %s)", key)
}

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

func getString(v *string, m map[string]interface{}, key string) error {
	value := getValue(m, key)
	valueStr, ok := value.(string)
	if value == nil || !ok {
		return fmt.Errorf("value not retrieved or is not a string(key: %s, value: %v)", key, value)
	}
	*v = valueStr
	return nil
}

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
