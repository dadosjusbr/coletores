package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

const empSample = `[{
	"matricula": 5014085,
	"dataReferencia": 1577847600000,
	"nome": "ADAILTON",
	"lotacao": "COORDENACAO DE TRANSPORTE - SALVADOR",
	"cargo": "MOTORISTA JUDICIÁRIO",
	"status": "A",
	"tipoServidor": "S",
	"valorParadigma": 4896.59,
	"valorVantagemPessoal": 9209.82,
	"valorComissao": 0,
	"valorIndenizacao": 1620,
	"valorVantagemEventual": 0,
	"totalCredito": 15726.41,
	"valorPrevidencia": 1961.05,
	"valorIR": 1856.3,
	"valorDescontoDiverso": 195.86,
	"valorRetencaoTeto": 0,
	"totalDebito": 4013.21,
	"valorLiquido": 11713.2,
	"valorRemuneracaoOrigem": 0,
	"valorDiaria": 0,
	"valorGratificacao": 0,
	"vantagensPessoais": [],
	"vantagensEventuais": [],
	"ano": null,
	"mes": null,
	"id": 5014085
}]`

func TestGetListOfEmployees(t *testing.T) {
	employees, err := newTjbaEmployees(empSample)
	assert.NoError(t, err)

	var expectedTjbaEmployee = tjbaEmployee{
		Reg:                   5014085,
		Name:                  "ADAILTON",
		Workplace:             "COORDENACAO DE TRANSPORTE - SALVADOR",
		Role:                  "MOTORISTA JUDICIÁRIO",
		Status:                "A",
		EmployeeType:          "S",
		Wage:                  4896.59,
		PersonalBenefitsValue: 9209.82,
		ComissionValue:        0,
		PerksValue:            1620,
		EventualBenefitsValue: 0,
		CreditTotal:           15726.41,
		PrevContribution:      1961.05,
		IncomeTax:             1856.3,
		Sundry:                195.86,
		RetantionValue:        0,
		DebtTotal:             4013.21,
		Value:                 11713.2,
		WageOriginValue:       0,
		Daily:                 0,
		Gratification:         0,
	}
	assert.Equal(t, employees[0], expectedTjbaEmployee)
}

func TestEmployeeType(t *testing.T) {
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

func TestActiveOrNot(t *testing.T) {
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
