package main

import (
	"reflect"
	"testing"

	storage "github.com/dadosjusbr/storage"
	"github.com/stretchr/testify/assert"
)

const empSample = `{   
    "id":872,
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
	pb   = 2.0
	eb   = 3.0
	pt   = 4.0
	d    = 5.0
	grat = 6.0
	orig = 7.0
)
var expectedEmployeeBasicInfo = storage.Employee{Reg: "872", Name: "ABIA", Workplace: "GABINETE", Role: "ANALISTA", Active: true, Type: "servidor"}
var expectedIncomeOthers = storage.Funds{PersonalBenefits: &pb, EventualBenefits: &eb, PositionOfTrust: &pt, Daily: &d, Gratification: &grat, OriginPosition: &orig}
var expectedDiscounts = storage.Discount{PrevContribution: &pb, IncomeTax: &eb, CeilRetention: &d, Others: map[string]float64{"sundry": 4}, Total: 14}
var expectedIncome = storage.IncomeDetails{Wage: &orig, Perks: &storage.Perks{Total: 0}, Other: &expectedIncomeOthers}
var expectedNewEmployee = storage.Employee{Reg: "872", Name: "ABIA", Workplace: "GABINETE", Role: "ANALISTA", Active: true, Type: "servidor", Income: &expectedIncome, Discounts: &expectedDiscounts}

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

func Test_employeeBasicInfo(t *testing.T) {
	j, err := jsonExample(empSample)
	assert.NoError(t, err)
	var e storage.Employee

	type args struct {
		e       *storage.Employee
		emp     map[string]interface{}
		catInfo string
	}
	tests := []struct {
		name    string
		args    args
		wantErr bool
		want    *storage.Employee
	}{
		{"ok", args{&e, j, "Servidores Ativos"}, false, &expectedEmployeeBasicInfo},
		{"missing name", args{&e, map[string]interface{}{}, "Servidores Ativos"}, true, nil},
		{"missing role", args{&e, map[string]interface{}{"nome": ""}, "Servidores Ativos"}, true, nil},
		{"missing workplace", args{&e, map[string]interface{}{"nome": "", "cargo": ""}, "Servidores Ativos"}, true, nil},
		{"missing Reg", args{&e, map[string]interface{}{"nome": "", "cargo": "", "lotacao": ""}, "Servidores Ativos"}, true, nil},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if err := employeeBasicInfo(tt.args.e, tt.args.emp, tt.args.catInfo); (err != nil) != tt.wantErr {
				t.Errorf("employeeBasicInfo() error = %v, wantErr %v", err, tt.wantErr)
			}
			if !tt.wantErr && !reflect.DeepEqual(tt.args.e, tt.want) {
				t.Errorf("employeeBasicInfo() result error. got: %v, want %v", tt.args.e, tt.want)
			}
		})
	}
}

func Test_employeeIncomeOthers(t *testing.T) {
	j, err := jsonExample(empSample)
	assert.NoError(t, err)
	var o storage.Funds

	type args struct {
		o   *storage.Funds
		emp map[string]interface{}
	}
	tests := []struct {
		name    string
		args    args
		wantErr bool
		want    *storage.Funds
	}{
		{"ok", args{&o, j}, false, &expectedIncomeOthers},
		{"missing rendimentos map", args{&o, map[string]interface{}{}}, true, nil},
		{"missing personal benefits", args{&o, map[string]interface{}{"rendimentos": map[string]interface{}{}}}, true, nil},
		{"missing eventual benefits",
			args{&o, map[string]interface{}{"rendimentos": map[string]interface{}{
				"vantagensPessoais": 0.0,
			}}}, true, nil},

		{"missing gratification",
			args{&o, map[string]interface{}{"rendimentos": map[string]interface{}{
				"vantagensPessoais": 0.0, "vantagensEventuais": 0.0,
			}}}, true, nil},

		{"missing Position Of Trust",
			args{&o, map[string]interface{}{"rendimentos": map[string]interface{}{
				"vantagensPessoais": 0.0, "vantagensEventuais": 0.0, "gratificacao": 0.0,
			}}}, true, nil},

		{"missing Origin Position",
			args{&o, map[string]interface{}{"rendimentos": map[string]interface{}{
				"vantagensPessoais": 0.0, "vantagensEventuais": 0.0, "gratificacao": 0.0,
				"subsidio": 0.0,
			}}}, true, nil},

		{"missing Daily",
			args{&o, map[string]interface{}{"rendimentos": map[string]interface{}{
				"vantagensPessoais": 0.0, "vantagensEventuais": 0.0, "gratificacao": 0.0,
				"subsidio": 0.0,
			}, "remuneracaoOrgaoOrigem": 0.0}}, true, nil},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if err := employeeIncomeOthers(tt.args.o, tt.args.emp); (err != nil) != tt.wantErr {
				t.Errorf("employeeIncomeOthers() error = %v, wantErr %v", err, tt.wantErr)
			}
			if !tt.wantErr && !reflect.DeepEqual(tt.args.o, tt.want) {
				t.Errorf("employeeIncomeOthers() result error. got: %v, want %v", tt.args.o, tt.want)
			}
		})
	}
}

func Test_employeeDiscounts(t *testing.T) {
	j, err := jsonExample(empSample)
	assert.NoError(t, err)
	var d storage.Discount

	type args struct {
		d   *storage.Discount
		emp map[string]interface{}
	}
	tests := []struct {
		name    string
		args    args
		wantErr bool
		want    *storage.Discount
	}{
		{"ok", args{&d, j}, false, &expectedDiscounts},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if err := employeeDiscounts(tt.args.d, tt.args.emp); (err != nil) != tt.wantErr {
				t.Errorf("employeeDiscounts() error = %v, wantErr %v", err, tt.wantErr)
			}
			if !tt.wantErr && !reflect.DeepEqual(tt.args.d, tt.want) {
				t.Errorf("employeeDiscounts() result error. got: %v, want %v", tt.args.d, tt.want)
			}
		})
	}
}
