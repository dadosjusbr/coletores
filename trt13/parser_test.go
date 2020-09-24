package main

import (
	"encoding/json"
	"testing"

	"github.com/dadosjusbr/coletores"
	"github.com/stretchr/testify/assert"
)

const empSample = `{   
    "matricula":"872",
    "nome":"ABIA",
    "lotacao":"GABINETE",
    "cargo":"ANALISTA",
    "rendimentos":{
        "remuneracaoParadigma":7,
        "vantagensPessoais":2.0,
        "subsidio":4,
        "indenizacoes":5,
        "vantagensEventuais":3,
        "gratificacao":6
        },
    "descontos":{
        "previdenciaPublica":2,
        "impostoRenda":3,
        "descontosDiversos":4,
        "retencaoTeto":5
    },
    "remuneracaoOrgaoOrigem":7.0,
    "diarias":5
}`

var (
	two    = 2.0
	three  = 3.0
	four   = 4.0
	five   = 5.0
	six    = 6.0
	seven  = 7.0
	eleven = 11.0
)
var (
	expectedEmployeeBasicInfo = coletores.Employee{Reg: "872", Name: "ABIA", Workplace: "GABINETE", Role: "ANALISTA", Active: true, Type: "servidor"}
	expectedIncomeOthers      = coletores.Funds{Total: 23, PersonalBenefits: &two, EventualBenefits: &three, Daily: &five, Gratification: &six, OriginPosition: &seven}
	expectedDiscounts         = coletores.Discount{PrevContribution: &two, IncomeTax: &three, CeilRetention: &five, Others: map[string]float64{"other_discounts": 4}, Total: 14}
	perks                     = coletores.Perks{Total: 5}
	expectedIncome            = coletores.IncomeDetails{Total: 39, Wage: &eleven, Perks: &perks, Other: &expectedIncomeOthers}
	expectedNewEmployee       = coletores.Employee{Reg: "872", Name: "ABIA", Workplace: "GABINETE", Role: "ANALISTA", Active: true, Type: "servidor", Income: &expectedIncome, Discounts: &expectedDiscounts}
)

func employeeSample(s string) (trt13Employee, error) {
	var emp trt13Employee
	err := json.Unmarshal([]byte(s), &emp)
	return emp, err
}

func Test_employeeType(t *testing.T) {
	tests := []struct {
		name string
		cat  string
		want string
	}{
		{"servidor", "Servidores Ativos", "servidor"},
		{"membros", "Magistrados Ativos", "membro"},
		{"pensionistas", "Pensionistas", "pensionista"},
		{"undefined", "Ativos", ""},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := employeeType(tt.cat); got != tt.want {
				t.Errorf("employeeType() = %v, want %v", got, tt.want)
			}
		})
	}
}

func Test_active(t *testing.T) {
	tests := []struct {
		name string
		cat  string
		want bool
	}{
		{"servidor", "Servidores Ativos", true},
		{"membros", "Magistrados Ativos", true},
		{"pensionistas", "Pensionistas", false},
		{"servidores in", "Servidores Inativos", false},
		{"membros in", "Magistrados Inativos", false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := active(tt.cat); got != tt.want {
				t.Errorf("active() = %v, want %v", got, tt.want)
			}
		})
	}
}

func Test_employeeFunds(t *testing.T) {
	emp, err := employeeSample(empSample)
	assert.NoError(t, err)

	funds := employeeFunds(emp)
	assert.Equal(t, expectedIncomeOthers, *funds)
}

func Test_employeeDiscounts(t *testing.T) {
	emp, err := employeeSample(empSample)
	assert.NoError(t, err)

	disc := employeeDiscounts(emp)
	assert.Equal(t, expectedDiscounts, *disc)
}

func Test_employeeIncome(t *testing.T) {
	emp, err := employeeSample(empSample)
	assert.NoError(t, err)

	in := employeeIncome(emp)
	assert.Equal(t, expectedIncome, *in)
}

func Test_newEmployee(t *testing.T) {
	emp, err := employeeSample(empSample)
	assert.NoError(t, err)

	e := newEmployee(emp, "Servidores Ativos")
	assert.Equal(t, expectedNewEmployee, e)
}
