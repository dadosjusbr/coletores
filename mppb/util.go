package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
	"time"
)

// logError prints to Stderr
func logError(format string, args ...interface{}) {
	time := fmt.Sprintf("%s: ", time.Now().Format(time.RFC3339))
	fmt.Fprintf(os.Stderr, time+format+"\n", args...)
}

func retrieveString(emp []string, key string, fileType int) string {
	return emp[headersMap[fileType][key]]
}

func retrieveFloat64(v interface{}, emp []string, key string, fileType int) error {
	var err error
	var value float64
	valueStr := retrieveString(emp, key, fileType)
	if valueStr == "" {
		value = 0.0
	} else {
		value, err = parseFloat(valueStr)
		if err != nil {
			return fmt.Errorf("error retrieving float %s from %v: %q", key, emp, err)
		}
	}

	if v, ok := v.(**float64); ok {
		*v = &value
		return nil
	}
	if v, ok := v.(*float64); ok {
		*v = value
		return nil
	}
	return fmt.Errorf("error retrieving float %s: v must be *float64 or **float64", key)
}

// sumMapValues takes a map of string -> float64 and return the sum of the map values.
func sumMapValues(m map[string]float64) float64 {
	var sum float64
	if m == nil {
		return 0
	}
	for _, v := range m {
		sum += v
	}
	return math.Round(sum*100) / 100
}

// parseFloat makes the string with format "xx.xx,xx" able to be parsed by the strconv.ParseFloat and return it parsed.
func parseFloat(s string) (float64, error) {
	s = strings.Trim(s, " ")
	s = strings.Replace(s, ",", ".", 1)
	if n := strings.Count(s, "."); n > 1 {
		s = strings.Replace(s, ".", "", n-1)
	}
	return strconv.ParseFloat(s, 64)
}

// getValue takes a list of float64 pointers and returns it's sum, 0 if nil
func getFloat64Value(pointers ...*float64) float64 {
	var total float64
	for _, p := range pointers {
		if p == nil {
			total += 0
			continue
		}
		total += *p
	}
	return math.Round(total*100) / 100.0
}

// cleanStrings makes all strings to uppercase and removes N/D fields
func cleanStrings(raw [][]string) [][]string {
	for row := range raw {
		for col := range raw[row] {
			raw[row][col] = strings.ToUpper(strings.ReplaceAll(strings.ReplaceAll(raw[row][col], "N/D", ""), "\n", " "))
		}
	}
	return raw
}

func sumIndexes(data []string, start int, end int) (float64, error) {
	var total float64
	if start > end || len(data) < end {
		return 0, fmt.Errorf("sumIndexes() error: start:%d, end:%d, len: %d", start, end, len(data))
	}

	for i := start; i <= end; i++ {
		tmp, err := parseFloat(data[i])
		if err != nil {
			return 0, fmt.Errorf("sumIndexes() error: %q", err)
		}
		total += tmp
	}
	return math.Round(total*100) / 100, nil
}

func sumKeyValues(data []string, keys []string, fileType int) (float64, error) {
	var total float64
	var tmp float64
	for _, k := range keys {
		if err := retrieveFloat64(&tmp, data, k, fileType); err != nil {
			return 0, fmt.Errorf("sum key values error: %q", err)
		}
		total += tmp
	}
	return math.Round(total*100) / 100, nil
}
