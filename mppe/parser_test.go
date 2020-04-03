package main

import (
	"math"
	"testing"

	"github.com/dadosjusbr/storage"
)

func getPointer(n float64) *float64 {
	return &n
}

func TestGetPointer(t *testing.T) {
	value := 10.0
	pointerValue := getPointer(value)
	if *pointerValue != value {
		t.Errorf("got %f, want %v", *pointerValue, value)
	}
}

func areFloatsEqual(a, b float64) bool {
	tolerance := 0.001
	diff := math.Abs(a - b)
	if diff < tolerance {
		return true
	}
	return false
}

func TestAreFloatsEqual(t *testing.T) {
	testCases := []struct {
		name string
		a    float64
		b    float64
		out  bool
	}{
		{"Should get true for comparison", 3.14, 3.141, true},
		{"Should get false for comparison", 3.14, 3.142, false},
	}
	for _, tt := range testCases {
		t.Run(tt.name, func(t *testing.T) {
			res := areFloatsEqual(tt.a, tt.b)
			if res != tt.out {
				t.Errorf("got %t, want %t", res, tt.out)
			}
		})
	}
}

func TestGetOthers(t *testing.T) {
	testCases := []struct {
		name           string
		row            []string
		identification string
		out            map[string]float64
	}{
		{"Should get other ammounts with total R$ 90,00, loyalty job R$ 50,0, christmas perk R$ 30,0, vacacion Perk R$ 20,0 and permanence perk R$ 10",
			[]string{"680729", "ALBÉRICO GOMES GUERRA", "PROMOTOR 3. ENTRANCIA", "INATIVOS", "33689.11", "90.0", "50.00", "30.00", "20.00", "10.00", "33689.11", "3759.70", "6837.63", "0.00", "10597.33", "23091.78", "500.00", "500.00"},
			"proventos-de-todos-os-membros-inativos",
			map[string]float64{
				"otherAmmounts":         90.0,
				"loyaltyJob":            50.0,
				"christmasPerk":         30.0,
				"vacacionPerk":          20.0,
				"permanencePerk":        10.0,
				"indemnity":             500.0,
				"temporaryRemuneration": 500.0}},
	}
	for _, tt := range testCases {
		t.Run(tt.name, func(t *testing.T) {
			others, _ := getOthers(tt.row, tt.identification)
			if !areFloatsEqual(others["otherAmmounts"], tt.out["otherAmmounts"]) {
				t.Errorf("got %f, want %f", others["otherAmmounts"], tt.out["otherAmmounts"])
			}
			if !areFloatsEqual(others["loyaltyJob"], tt.out["loyaltyJob"]) {
				t.Errorf("got %f, want %f", others["loyaltyJob"], tt.out["loyaltyJob"])
			}
			if !areFloatsEqual(others["christmasPerk"], tt.out["christmasPerk"]) {
				t.Errorf("got %f, want %f", others["christmasPerk"], tt.out["christmasPerk"])
			}
			if !areFloatsEqual(others["vacacionPerk"], tt.out["vacacionPerk"]) {
				t.Errorf("got %f, want %f", others["vacacionPerk"], tt.out["vacacionPerk"])
			}
			if !areFloatsEqual(others["permanencePerk"], tt.out["permanencePerk"]) {
				t.Errorf("got %f, want %f", others["permanencePerk"], tt.out["permanencePerk"])
			}
			if !areFloatsEqual(others["indemnity"], tt.out["indemnity"]) {
				t.Errorf("got %f, want %f", others["indemnity"], tt.out["indemnity"])
			}
			if !areFloatsEqual(others["temporaryRemuneration"], tt.out["temporaryRemuneration"]) {
				t.Errorf("got %f, want %f", others["temporaryRemuneration"], tt.out["temporaryRemuneration"])
			}
		})
	}
}

func TestGetDiscounts_Sucess(t *testing.T) {
	testCases := []struct {
		name           string
		row            []string
		identification string
		discount       *storage.Discount
	}{
		{"should get a discount with total R$ 10.597,33, ceil retention R$ 0,0, income tax R$ 6.837,63 and prev contribution R$ 3.759,7",
			[]string{"680729", "ALBÉRICO GOMES GUERRA", "PROMOTOR 3. ENTRANCIA", "INATIVOS", "33689.11", "0.00", "0.00", "0.00", "0.00", "0.00", "33689.11", "3759.70", "6837.63", "0.00", "10597.33", "23091.78", "500.00", "500.00"},
			"proventos-de-todos-os-membros-inativos",
			&storage.Discount{Total: 10597.33, PrevContribution: getPointer(3759.7), CeilRetention: getPointer(0), IncomeTax: getPointer(6837.63)}},
	}
	for _, tt := range testCases {
		t.Run(tt.name, func(t *testing.T) {
			discount, _ := getDiscounts(tt.row, tt.identification)
			if !areFloatsEqual(discount.Total, tt.discount.Total) {
				t.Errorf("got %f, want %f", discount.Total, tt.discount.Total)
			}
			if !areFloatsEqual(*discount.PrevContribution, *tt.discount.PrevContribution) {
				t.Errorf("got %f, want %f", *discount.PrevContribution, *tt.discount.PrevContribution)
			}
			if !areFloatsEqual(*discount.CeilRetention, *tt.discount.CeilRetention) {
				t.Errorf("got %f, want %f", *discount.CeilRetention, *tt.discount.CeilRetention)
			}
			if !areFloatsEqual(*discount.IncomeTax, *tt.discount.IncomeTax) {
				t.Errorf("got %f, want %f", *discount.IncomeTax, *tt.discount.IncomeTax)
			}
		})
	}
}

func TestGetType(t *testing.T) {
	testCases := []struct {
		name string
		in   string
		out  string
	}{
		{"It should give membro", "proventos-de-todos-os-membros-inativos", "membro"},
		{"It should give servidor", "proventos-de-todos-os-servidores-inativos", "servidor"},
		{"It should give membro", "remuneracao-de-todos-os-membros-ativos", "membro"},
		{"It should give servidor", "remuneracao-de-todos-os-servidores-atuvos", "servidor"},
		{"It should give colaborador", "valores-percebidos-por-todos-os-colaboradores", "colaborador"},
		{"It should give pensionista", "valores-percebidos-por-todos-os-pensionistas", "pensionista"},
		{"It should give indefinido", "verbas-indenizatorias-e-outras-remuneracoes-temporarias", "indefinido"},
		{"It should give indefinido", "verbas-referentes-a-exercicios-anteriores", "indefinido"},
	}
	for _, tt := range testCases {
		t.Run(tt.name, func(t *testing.T) {
			res := getType(tt.in)
			if res != tt.out {
				t.Errorf("got %s, want %s", res, tt.out)
			}
		})
	}
}

func TestGetFunds(t *testing.T) {
	testCases := []struct {
		name            string
		row             []string
		indentification string
		funds           *storage.Funds
	}{
		{
			"Should get the right Total for employee with R$ 33689.11 as total ammount",
			[]string{"680729", "ALBÉRICO GOMES GUERRA", "PROMOTOR 3. ENTRANCIA", "INATIVOS", "33689.11", "90.0", "50.00", "30.00", "20.00", "10.00", "33689.11", "3759.70", "6837.63", "0.00", "10597.33", "23091.78", "500.00", "500.00"},
			"proventos-de-todos-os-membros-inativos",
			&storage.Funds{
				Total: 33689.11,
			},
		},
	}
	for _, tt := range testCases {
		t.Run(tt.name, func(t *testing.T) {
			res, _ := getFunds(tt.row, tt.indentification)
			if !areFloatsEqual(res.Total, tt.funds.Total) {
				t.Errorf("got %f, want %f", res.Total, tt.funds.Total)
			}
		})
	}
}

func TestIsActive(t *testing.T) {
	testCases := []struct {
		name string
		in   string
		out  bool
	}{
		{"It should give false", "proventos-de-todos-os-membros-inativos", false},
		{"It should give false", "proventos-de-todos-os-servidores-inativos", false},
		{"It should give true", "remuneracao-de-todos-os-membros-ativos", true},
		{"It should give true", "remuneracao-de-todos-os-servidores-atuvos", true},
		{"It should give true", "valores-percebidos-por-todos-os-colaboradores", true},
		{"It should give false", "valores-percebidos-por-todos-os-pensionistas", false},
		{"It should give false", "verbas-indenizatorias-e-outras-remuneracoes-temporarias", false},
		{"It should give false", "verbas-referentes-a-exercicios-anteriores", false},
	}
	for _, tt := range testCases {
		t.Run(tt.name, func(t *testing.T) {
			res := isActive(tt.in)
			if res != tt.out {
				t.Errorf("got %t, want %t", res, tt.out)
			}
		})
	}
}

func TestGetTypeOfFile(t *testing.T) {
	testCases := []struct {
		name string
		in   string
		out  string
	}{
		{"Should has sucess on getting file name", "fileName-02-2019.xlsx", "fileName"},
		{"Should has sucess on getting file name", "01-29-february-file-name-02-2019.xlsx", "01-29-february-file-name"},
	}
	for _, tt := range testCases {
		t.Run(tt.name, func(t *testing.T) {
			res := getFileDocumentation(tt.in)
			if res != tt.out {
				t.Errorf("got %s, want %s", res, tt.out)
			}
		})
	}
}
