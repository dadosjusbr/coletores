package main

import (
	"math"
	"testing"

	"github.com/dadosjusbr/coletores"
)

func areFloatsEqual(a, b float64) bool {
	tolerance := 0.001
	diff := math.Abs(a - b)
	return diff < tolerance
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

func getPointer(n float64) *float64 {
	return &n
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

func TestDiscounts(t *testing.T) {
	testCases := []struct {
		name            string
		row             []string
		indentification string
		funds           *coletores.Discount
		indexMap        map[string]int
	}{
		{
			"Should get discounts",
			[]string{"680729", "ALBÉRICO GOMES GUERRA", "PROMOTOR 3. ENTRANCIA", "INATIVOS", "33689.11", "90.0", "50.00", "30.00", "20.00", "10.00", "33689.11", "3759.70", "6837.63", "0.00", "10597.33", "23091.78", "500.00", "500.00"},
			"proventos-de-todos-os-membros-inativos",
			&coletores.Discount{
				Total:            10597.33,
				CeilRetention:    getPointer(0),
				IncomeTax:        getPointer(6837.63),
				PrevContribution: getPointer(3759.70),
			},
			indexies["proventos-de-todos-os-membros-inativos"],
		},
	}
	for _, tt := range testCases {
		t.Run(tt.name, func(t *testing.T) {
			res, _ := getDiscounts(tt.row, tt.indentification, tt.indexMap)
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
		{"Should has sucess on getting file name", "./output/fileName-02-2019.xlsx", "fileName"},
		{"Should has sucess on getting file name", "./output/01-29-february-file-name-02-2019.xlsx", "01-29-february-file-name"},
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
