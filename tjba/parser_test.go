package main

import (
	"errors"
	"testing"

	"github.com/dadosjusbr/coletores"
	"github.com/dadosjusbr/coletores/status"
	"github.com/stretchr/testify/assert"
)

const tjbaPayload = "testdata/payload.json"

func TestCreateTjbaEmployeesFromJSON(t *testing.T) {
	employees, err := NewTjbaEmployees(tjbaPayload)
	assert.NoError(t, err)

	var expectedTjbaEmployee = tjbaEmployee{
		Reg:                 5014085,
		Name:                "ADAILTON",
		Workplace:           "COORDENACAO DE TRANSPORTE - SALVADOR",
		Role:                "MOTORISTA JUDICIÁRIO",
		Active:              "A",
		Type:                "S",
		Wage:                4896.59,
		PersonalBenefits:    9209.82,
		PositionOfTrust:     0,
		PerksTotal:          1620,
		EventualBenefits:    0,
		IncomeTotal:         15726.41,
		PrevContribution:    1961.05,
		IncomeTax:           1856.3,
		OtherDiscountsTotal: 195.86,
		CeilRetention:       0,
		DiscountTotal:       4013.21,
		FundsTotal:          11713.2,
		OriginPosition:      0,
		Daily:               0,
		Gratification:       0,
	}
	assert.Equal(t, employees[0], expectedTjbaEmployee)
}

func TestFailWhenParsingInvalidTjbaEmployeesJSON(t *testing.T) {
	expectedError := status.NewError(status.InvalidInput, errors.New("Error during JSON parsing"))
	_, err := NewTjbaEmployees("testdata/invalid-payload.json")

	assert.Error(t, err)
	assert.Equal(t, expectedError, err)
}

func TestConvertFromTjbaEmployeeTypeToEmployeeType(t *testing.T) {
	tests := []struct {
		name     string
		value    string
		expected string
	}{
		{"servidor", "S", "servidor"},
		{"membros", "D", "membro"},
		{"pensionistas", "J", "membro"},
		{"undefined", "W", ""},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := employeeType(tt.value); got != tt.expected {
				t.Errorf("employeeType() = %v, want %v", got, tt.expected)
			}
		})
	}
}

func TestConvertFromTjbaEmployeeActiveToEmployeeActive(t *testing.T) {
	tests := []struct {
		name string
		cat  string
		want bool
	}{
		{"active", "A", true},
		{"inactive", "I", false},
		{"undefined", "?", false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := active(tt.cat); got != tt.want {
				t.Errorf("active() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestFromTjbaEmployeeToEmployee(t *testing.T) {
	tjbaEmployees, err := NewTjbaEmployees(tjbaPayload)
	assert.NoError(t, err)

	employees := FromTjbaEmployeeToEmployee(tjbaEmployees)
	assert.Equal(t, len(employees), 1)

	var zero = 0.0
	var expectedPersonalBenefits = 9209.82
	var expectedWage = 4896.59
	var prevContribution = 1961.05
	var ceilRetention = 0.0
	var incomeTax = 1856.3
	var otherDiscounts = 195.86

	var expectedEmployee = coletores.Employee{
		Reg:       "5014085",
		Name:      "ADAILTON",
		Role:      "MOTORISTA JUDICIÁRIO",
		Type:      "servidor",
		Workplace: "COORDENACAO DE TRANSPORTE - SALVADOR",
		Active:    true,
		Income: &coletores.IncomeDetails{
			Total: 15726.41,
			Wage:  &expectedWage,
			Perks: &coletores.Perks{Total: 1620},
			Other: &coletores.Funds{
				Total:            11713.2,
				PersonalBenefits: &expectedPersonalBenefits,
				EventualBenefits: &zero,
				PositionOfTrust:  &zero,
				Gratification:    &zero,
				Daily:            &zero,
				OriginPosition:   &zero,
			},
		},
		Discounts: &coletores.Discount{
			Total:               4013.21,
			PrevContribution:    &prevContribution,
			CeilRetention:       &ceilRetention,
			IncomeTax:           &incomeTax,
			OtherDiscountsTotal: &otherDiscounts,
		},
	}
	assert.Equal(t, employees[0], expectedEmployee)
}
