package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/antchfx/htmlquery"
	"golang.org/x/net/html"
	"golang.org/x/net/html/charset"
)

func crawl(name, cpf string, month, year int) error {
	acessCode, err := accessCode(name, cpf)
	if err != nil {
		return fmt.Errorf("Access Code Error: %q", err)
	}

	data, err := queryData(acessCode, month, year)
	if err != nil {
		return fmt.Errorf("Query data error: %q", err)
	}

	dataDesc := fmt.Sprintf("remuneracoes-trepb-%02d-%04d", month, year)
	if err = save(dataDesc, data); err != nil {
		return fmt.Errorf("Error saving data to file: %q", err)
	}

	return nil
}

// queryData query server for data of a specified month and year.
func queryData(acessCode string, month, year int) ([]*html.Node, error) {
	query := fmt.Sprintf(`acao=AnexoVIII&folha=&valida=true&toExcel=false&chaveDeAcesso=%s&mes=%d&ano=%04d`, acessCode, month, year)
	queryURL := fmt.Sprintf(`http://apps.tre-pb.jus.br/transparenciaDadosServidores/infoServidores?%s`, query)
	req, err := http.NewRequest("GET", queryURL, nil)
	if err != nil {
		return nil, fmt.Errorf("error creating GET request to %s: %q", queryURL, err)
	}
	req.Header.Add("Accept-Charset", "utf-8")

	doc, err := httpReq(req)
	if err != nil {
		return nil, fmt.Errorf("error making data request: %q", err)
	}

	tables, err := htmlquery.QueryAll(doc, "//table")
	if err != nil {
		return nil, fmt.Errorf("error while making query for data tables: %q", err)
	}
	if len(tables) == 0 {
		return nil, fmt.Errorf("couldn't find any data tables")
	}
	return tables, nil
}

// save creates a file in the output folder and save the data nodes to it.
func save(desc string, data []*html.Node) error {
	if err := os.Mkdir("output", os.ModePerm); err != nil && !os.IsExist(err) {
		return fmt.Errorf("error creating output folder(%s): %q", "/output", err)
	}

	fileName := fmt.Sprintf("%s.html", desc)
	f, err := os.Create("./output/" + fileName)
	if err != nil {
		return fmt.Errorf("error creating file(%s):%q", fileName, err)
	}
	defer f.Close()

	for _, node := range data {
		r, err := charset.NewReader(strings.NewReader(htmlquery.OutputHTML(node, true)), "latin1")
		if err != nil {
			log.Fatal(err)
		}

		if _, err = io.Copy(f, r); err != nil {
			os.Remove(fileName)
			return fmt.Errorf("error copying response content to file: %q", err)
		}
	}
	return nil
}
