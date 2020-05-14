package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"reflect"
	"strings"
	"testing"

	"github.com/dadosjusbr/storage"
)

func printState(e storage.Employee) {
	b, _ := json.Marshal(e)
	fmt.Println(string(b))
}

func TestIntegration(t *testing.T) {
	testCases := []struct {
		name       string
		month      int
		year       int
		server     *httptest.Server
		outputPath string
	}{
		{"Test for proventos-de-todos-os-servidores-inativos-02-2019", 2, 2019,
			httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				// it was call to download the file
				uri := r.URL.RequestURI()
				if strings.Contains(uri, "download") {
					path := "./test_files/sample.xlsx"
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
			})), "./test_files/proventos-servidores-inativos.json",
		},
		{"Test for proventos-de-todos-os-servidores-inativos-02-2019", 2, 2019,
			httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				// it was call to download the file
				uri := r.URL.RequestURI()
				if strings.Contains(uri, "download") {
					path := "./test_files/sample.xlsx"
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
			})), "./test_files/proventos-membros-inativos.json",
		},
		{"Test for proventos-de-todos-os-servidores-inativos-02-2019", 2, 2019,
			httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				// it was call to download the file
				uri := r.URL.RequestURI()
				if strings.Contains(uri, "download") {
					path := "./test_files/sample.xlsx"
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
			})), "./test_files/valores-percebidos-por-todos-os-pensionistas.json",
		},
		{"Test for proventos-de-todos-os-servidores-inativos-02-2019", 2, 2019,
			httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				// it was call to download the file
				uri := r.URL.RequestURI()
				if strings.Contains(uri, "download") {
					path := "./test_files/sample.xlsx"
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
			})), "./test_files/remuneracao-de-todos-os-servidores-atuvos.json",
		},
		{"Test for proventos-de-todos-os-servidores-inativos-02-2019", 2, 2019,
			httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				// it was call to download the file
				uri := r.URL.RequestURI()
				if strings.Contains(uri, "download") {
					path := "./test_files/sample.xlsx"
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
			})), "./test_files/remuneracao-de-todos-os-membros-ativos.json",
		},
	}
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
			testOutputSample := r[0]
			desiredOutput, err := ioutil.ReadFile(tt.outputPath)
			if err != nil {
				t.Errorf("fail to read desired output file, got %q", err)
			}
			var res storage.Employee
			err = json.Unmarshal(desiredOutput, &res)
			if err != nil {
				t.Errorf("want nil, got %q", err)
			}
			if res.Reg != testOutputSample.Reg {
				t.Errorf("reg was supposed to be %s, got %s", testOutputSample.Reg, res.Reg)
			}
			if res.Name != testOutputSample.Name {
				t.Errorf("name was supposed to be %s, got %s", testOutputSample.Name, res.Name)
			}
			if !reflect.DeepEqual(res.Discounts, testOutputSample.Discounts) {
				t.Errorf("expect discounts to be equal, got differents")
			}
			if !reflect.DeepEqual(res.Income, testOutputSample.Income) {
				t.Errorf("expect incomes to be equal, got differents")
			}
		})
	}
}
