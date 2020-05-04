package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestFullProcess(t *testing.T) {
	testCases := []struct {
		name    string
		month   int
		year    int
		path    string
		baseURL string
		server  *httptest.Server
	}{
		{"Test for proventos de todos os servidores inativos", 2, 2019, "output", "",
			httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				// it was call to download the file
				if strings.Contains(r.URL.Path, "download") {
					path := "./test_files/proventos.xlsx"
					b, err := ioutil.ReadFile(path)
					if err != nil {
						fmt.Println("error on reading file ", err)
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
			}))},
	}
	for _, tt := range testCases {
		t.Run(tt.name, func(t *testing.T) {
			s, e := Crawl("output", 2, 2019, tt.server.URL+"/")
			fmt.Println(e)
			fmt.Println(s)
		})
	}
}
