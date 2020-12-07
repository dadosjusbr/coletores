package main

import (
	"encoding/json"
)

// newtjbaEmployee creates a tjbaEmployee from a map[string]interface{}
func newTjbaEmployees(payload string) ([]tjbaEmployee, error) {
	var employees []tjbaEmployee
	err := json.Unmarshal([]byte(payload), &employees)
	return employees, err
}

// employeeType returns employee.Type based in category string.
func employeeType(value string) string {
	// possible values from the source: S, D and J
	if value == "S" {
		return "servidor"
	} else if value == "D" || value == "J" {
		return "membro"
	}
	return ""
}

// active returns Employee.Active based in category string.
func active(value string) bool {
	// possible values from the source: A or I
	return value == "A"
}
