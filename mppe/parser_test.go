package main

import "testing"

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
