package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"reflect"
	"strings"
	"testing"

	"github.com/dadosjusbr/storage"
)

//proventos-de-todos-os-servidores-inativos-02-2019.xlsx
func TestIntegration(t *testing.T) {
	testCases := []struct {
		name     string
		month    int
		year     int
		server   *httptest.Server
		employee storage.Employee
	}{
		{"Test for proventos-de-todos-os-servidores-inativos-02-2019", 2, 2019,
			httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				// it was call to download the file
				uri := r.URL.RequestURI()
				if strings.Contains(uri, "download") {
					path := "./test_files/proventos-de-todos-os-servidores-inativos-02-2019.xlsx"
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
				Active:    true,
				Type:      "membro",
				Workplace: "mppe",
				Role:      "TECNICO MINIST SUPLEMENTAR                        ",
				Discounts: &storage.Discount{
					Total:            1748491,
					PrevContribution: getPointer(1462.34),
					CeilRetention:    getPointer(0),
					IncomeTax:        getPointer(3208.91),
					Others:           nil,
				},
				Income: &storage.IncomeDetails{
					Total: 17171.58,
					Wage:  getPointer(15155.98),
					Other: &storage.Funds{
						Total:            15155.98,
						PersonalBenefits: nil,
						EventualBenefits: nil,
						PositionOfTrust:  nil,
						Daily:            nil,
						Gratification:    nil,
						OriginPosition:   nil,
						Others:           nil,
					},
					Perks: &storage.Perks{
						Total:          500,
						Food:           nil,
						Transportation: nil,
						PreSchool:      nil,
						Health:         nil,
						BirthAid:       nil,
						HousingAid:     nil,
						Subsistence:    nil,
						Others: map[string]float64{
							"christmasPerk":         0.0,
							"indemnity":             500,
							"loyaltyJob":            0.0,
							"otherAmmounts":         1515.6,
							"permanencePerk":        0.0,
							"temporaryRemuneration": 0.0,
							"vacacionPerk":          0.0,
						},
					},
				},
			}},
		// {"Test for remuneracao-de-todos-os-membros-ativos-02-2019", 2, 2019,
		// 	httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// 		// it was call to download the file
		// 		uri := r.URL.RequestURI()
		// 		if strings.Contains(uri, "download") {
		// 			path := "./test_files/remuneracao-de-todos-os-membros-ativos-02-2019.xlsx"
		// 			b, err := ioutil.ReadFile(path)
		// 			if err != nil {
		// 				t.Errorf("expecting null err, got %q", err)
		// 			}
		// 			w.Write(b)
		// 			return
		// 		}
		// 		// it was call to make crawl
		// 		fmt.Fprint(w, "<div><link src=\".../4554/resource-fevereiro:download=5051:membros-ativos-02-2019\"/></div>"+
		// 			"<div><link src=\".../4554/resource:download=4312:membros-inativos-02-2019\"/></div>"+
		// 			"<div><link src=\".../31342sas2/endpoint:download=9999:servidores-ativos-02-2019\"/></div>"+
		// 			"<div><link src=\".../ghytr6/resource:download=1098:servidores-inativos-02-2019\"/></div>"+
		// 			"<div><link src=\".../5tghjuw2/Controller:random=5453:pensionistas-02-2019\"/></div>"+
		// 			"<div><link src=\".../random/servlet:code=3490:contracheque-valores-percebidos-colaboradores-fevereiro\"/></div>"+
		// 			"<div><link src=\".../controller_servlet:download=5378:dea-022019\"/></div>"+
		// 			"<div><link src=\".../members_controller:code=8712:virt-fevereiro-2019\"/></div>")
		// 		return
		// 	})), storage.Employee{
		// 		Reg:       "1771124",
		// 		Name:      "ADALBERTO MENDES PINTO VIEIRA",
		// 		Active:    false,
		// 		Type:      "membro",
		// 		Workplace: "mppe",
		// 		Role:      "PROCURADOR DE JUSTICA                             ",
		// 	}},
		// {"Test for remuneracao-de-todos-os-servidores-atuvos-02-2019", 2, 2019,
		// 	httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// 		// it was call to download the file
		// 		uri := r.URL.RequestURI()
		// 		if strings.Contains(uri, "download") {
		// 			path := "./test_files/remuneracao-de-todos-os-servidores-atuvos-02-2019.xlsx"
		// 			b, err := ioutil.ReadFile(path)
		// 			if err != nil {
		// 				t.Errorf("expecting null err, got %q", err)
		// 			}
		// 			w.Write(b)
		// 			return
		// 		}
		// 		// it was call to make crawl
		// 		fmt.Fprint(w, "<div><link src=\".../4554/resource-fevereiro:download=5051:membros-ativos-02-2019\"/></div>"+
		// 			"<div><link src=\".../4554/resource:download=4312:membros-inativos-02-2019\"/></div>"+
		// 			"<div><link src=\".../31342sas2/endpoint:download=9999:servidores-ativos-02-2019\"/></div>"+
		// 			"<div><link src=\".../ghytr6/resource:download=1098:servidores-inativos-02-2019\"/></div>"+
		// 			"<div><link src=\".../5tghjuw2/Controller:random=5453:pensionistas-02-2019\"/></div>"+
		// 			"<div><link src=\".../random/servlet:code=3490:contracheque-valores-percebidos-colaboradores-fevereiro\"/></div>"+
		// 			"<div><link src=\".../controller_servlet:download=5378:dea-022019\"/></div>"+
		// 			"<div><link src=\".../members_controller:code=8712:virt-fevereiro-2019\"/></div>")
		// 		return
		// 	})), storage.Employee{
		// 		Reg:       "1894196",
		// 		Name:      "AARÃO GOMES DE SOUZA",
		// 		Active:    false,
		// 		Type:      "membro",
		// 		Workplace: "mppe",
		// 		Role:      "TECNICO MINISTERIAL                               ",
		// 	}},
		// {"Test for rvalores-percebidos-por-todos-os-pensionistas-02-2019", 2, 2019,
		// 	httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// 		// it was call to download the file
		// 		uri := r.URL.RequestURI()
		// 		if strings.Contains(uri, "download") {
		// 			path := "./test_files/valores-percebidos-por-todos-os-pensionistas-02-2019.xlsx"
		// 			b, err := ioutil.ReadFile(path)
		// 			if err != nil {
		// 				t.Errorf("expecting null err, got %q", err)
		// 			}
		// 			w.Write(b)
		// 			return
		// 		}
		// 		// it was call to make crawl
		// 		fmt.Fprint(w, "<div><link src=\".../4554/resource-fevereiro:download=5051:membros-ativos-02-2019\"/></div>"+
		// 			"<div><link src=\".../4554/resource:download=4312:membros-inativos-02-2019\"/></div>"+
		// 			"<div><link src=\".../31342sas2/endpoint:download=9999:servidores-ativos-02-2019\"/></div>"+
		// 			"<div><link src=\".../ghytr6/resource:download=1098:servidores-inativos-02-2019\"/></div>"+
		// 			"<div><link src=\".../5tghjuw2/Controller:random=5453:pensionistas-02-2019\"/></div>"+
		// 			"<div><link src=\".../random/servlet:code=3490:contracheque-valores-percebidos-colaboradores-fevereiro\"/></div>"+
		// 			"<div><link src=\".../controller_servlet:download=5378:dea-022019\"/></div>"+
		// 			"<div><link src=\".../members_controller:code=8712:virt-fevereiro-2019\"/></div>")
		// 		return
		// 	})), storage.Employee{
		// 		Reg:       "219021101",
		// 		Name:      "ADALCINA VIEIRA LUCENA",
		// 		Active:    false,
		// 		Type:      "membro",
		// 		Workplace: "mppe",
		// 		Role:      "PENSIONISTA",
		// 	}},
		// {"Test for proventos-de-todos-os-membros-inativos-02-2019", 2, 2019,
		// 	httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// 		// it was call to download the file
		// 		uri := r.URL.RequestURI()
		// 		if strings.Contains(uri, "download") {
		// 			path := "./test_files/proventos-de-todos-os-membros-inativos-02-2019.xlsx"
		// 			b, err := ioutil.ReadFile(path)
		// 			if err != nil {
		// 				t.Errorf("expecting null err, got %q", err)
		// 			}
		// 			w.Write(b)
		// 			return
		// 		}
		// 		// it was call to make crawl
		// 		fmt.Fprint(w, "<div><link src=\".../4554/resource-fevereiro:download=5051:membros-ativos-02-2019\"/></div>"+
		// 			"<div><link src=\".../4554/resource:download=4312:membros-inativos-02-2019\"/></div>"+
		// 			"<div><link src=\".../31342sas2/endpoint:download=9999:servidores-ativos-02-2019\"/></div>"+
		// 			"<div><link src=\".../ghytr6/resource:download=1098:servidores-inativos-02-2019\"/></div>"+
		// 			"<div><link src=\".../5tghjuw2/Controller:random=5453:pensionistas-02-2019\"/></div>"+
		// 			"<div><link src=\".../random/servlet:code=3490:contracheque-valores-percebidos-colaboradores-fevereiro\"/></div>"+
		// 			"<div><link src=\".../controller_servlet:download=5378:dea-022019\"/></div>"+
		// 			"<div><link src=\".../members_controller:code=8712:virt-fevereiro-2019\"/></div>")
		// 		return
		// 	})), storage.Employee{
		// 		Reg:       "1885065",
		// 		Name:      "ADLLA RIJO FARIAS COSTA",
		// 		Active:    false,
		// 		Type:      "membro",
		// 		Workplace: "mppe",
		// 		Role:      "PROMOTOR 1. ENTRANCIA                             ",
		// 	}},
	}
	for _, tt := range testCases {
		t.Run(tt.name, func(t *testing.T) {
			c, e := Crawl("./output", 2, 2019, tt.server.URL+"/")
			if e != nil {
				t.Errorf("want error nil, got %q", e)
			}
			r, e := Parse(c)
			if e != nil {
				t.Errorf("want error nil, got %q", e)
			}
			sample := r[0]
			// Comparing sample with test object
			if reflect.DeepEqual(sample, tt.employee) {
				fmt.Println("equal")
			}

			fmt.Println("not equal")
			// if sample.Reg != tt.employee.Reg {
			// 	t.Errorf("got %s, want %s", sample.Reg, tt.employee.Reg)
			// }
			// if sample.Name != tt.employee.Name {
			// 	t.Errorf("got %s, want %s", sample.Name, tt.employee.Name)
			// }
			// if sample.Role != tt.employee.Role {
			// 	t.Errorf("got %s, want %s", sample.Role, tt.employee.Role)
			// }
			// if sample.Workplace != tt.employee.Workplace {
			// 	t.Errorf("got %s, want %s", sample.Workplace, tt.employee.Workplace)
			// }
		})
	}
}
