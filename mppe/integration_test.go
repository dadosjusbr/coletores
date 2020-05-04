package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/dadosjusbr/storage"
)

func TestIntegration(t *testing.T) {
	testCases := []struct {
		name     string
		month    int
		year     int
		server   *httptest.Server
		employee storage.Employee
	}{
		{"Test for proventos-de-todos-os-membros-inativos", 2, 2019,
			httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				// it was call to download the file
				if strings.Contains(r.URL.RequestURI(), "download") {
					path := "./test_files/proventos-de-todos-os-membros-inativos.xlsx"
					b, err := ioutil.ReadFile(path)
					if err != nil {
						t.Errorf("expecting null err, got %q", err)
					}
					w.Write(b)
					return
				}
				// it was call to make crawl
				fmt.Fprint(w, "<div><link src=\".../4554/resource-fevereiro:download=5051:membros-ativos-02-2019\"/></div>"+
					"<div><link src=\".../4554/resource:download=4312:membros-inativos-02-2019\"/></div>"+
					"<div><link src=\".../31342sas2/endpoint:download=9999:servidores-ativos-02-2019\"/></div>"+
					"<div><link src=\".../ghytr6/resource:download=1098:servidores-inativos-02-2019\"/></div>"+
					"<div><link src=\".../5tghjuw2/Controller:random=5453:pensionistas-02-2019\"/></div>"+
					"<div><link src=\".../random/servlet:code=3490:contracheque-valores-percebidos-colaboradores-fevereiro\"/></div>"+
					"<div><link src=\".../controller_servlet:download=5378:dea-022019\"/></div>"+
					"<div><link src=\".../members_controller:code=8712:virt-fevereiro-2019\"/></div>")
				return
			})), storage.Employee{
				Reg:       "1885065",
				Name:      "ADLLA RIJO FARIAS COSTA",
				Active:    false,
				Type:      "membro",
				Workplace: "mppe",
				Role:      "PROMOTOR 1. ENTRANCIA                             ",
			}},
		{"Test for proventos-de-todos-os-servidores-inativos", 2, 2019,
			httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				// it was call to download the file
				if strings.Contains(r.URL.RequestURI(), "download") {
					path := "./test_files/proventos-de-todos-os-servidores-inativos.xlsx"
					b, err := ioutil.ReadFile(path)
					if err != nil {
						t.Errorf("expecting null err, got %q", err)
					}
					w.Write(b)
					return
				}
				// it was call to make crawl
				fmt.Fprint(w, "<div><link src=\".../4554/resource-fevereiro:download=5051:membros-ativos-02-2019\"/></div>"+
					"<div><link src=\".../4554/resource:download=4312:membros-inativos-02-2019\"/></div>"+
					"<div><link src=\".../31342sas2/endpoint:download=9999:servidores-ativos-02-2019\"/></div>"+
					"<div><link src=\".../ghytr6/resource:download=1098:servidores-inativos-02-2019\"/></div>"+
					"<div><link src=\".../5tghjuw2/Controller:random=5453:pensionistas-02-2019\"/></div>"+
					"<div><link src=\".../random/servlet:code=3490:contracheque-valores-percebidos-colaboradores-fevereiro\"/></div>"+
					"<div><link src=\".../controller_servlet:download=5378:dea-022019\"/></div>"+
					"<div><link src=\".../members_controller:code=8712:virt-fevereiro-2019\"/></div>")
				return
			})), storage.Employee{
				Reg:       "1748491",
				Name:      "ADOLFO VILANOVA DE ASSIS",
				Active:    false,
				Type:      "membro",
				Workplace: "mppe",
				Role:      "TECNICO MINIST SUPLEMENTAR                        ",
			}},
	}
	//proventos-de-todos-os-servidores-inativos.xlsx
	for _, tt := range testCases {
		t.Run(tt.name, func(t *testing.T) {
			c, e := Crawl("./test_files", 2, 2019, tt.server.URL+"/")
			if e != nil {
				t.Errorf("want error nil, got %q", e)
			}
			r, e := Parse(c)
			if e != nil {
				t.Errorf("want error nil, got %q", e)
			}
			sample := r[0]
			fmt.Println(sample)
			if sample.Reg != tt.employee.Reg {
				t.Errorf("got %s, want %s", sample.Reg, tt.employee.Reg)
			}
			if sample.Name != tt.employee.Name {
				t.Errorf("got %s, want %s", sample.Name, tt.employee.Name)
			}
			if sample.Role != tt.employee.Role {
				t.Errorf("got %s, want %s", sample.Role, tt.employee.Role)
			}
			if sample.Workplace != tt.employee.Workplace {
				t.Errorf("got %s, want %s", sample.Workplace, tt.employee.Workplace)
			}
		})
	}
}
