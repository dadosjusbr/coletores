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
)

func crawl(name, cpf string, month, year int) {
	acessCode, err := accessCode(name, cpf)
	if err != nil {
		log.Fatalf("Access Code Error: %q", err)
	}

	data, err := queryData(acessCode, month, year)
	if err != nil {
		log.Fatalf("Query data error: %q", err)
	}

	dataDesc := fmt.Sprintf("remuneracoes-trepb-%02d-%04d", month, year)
	if err = save(dataDesc, data); err != nil {
		log.Fatalf("Error saving data to file: %q", err)
	}
}

// queryData query server for data of a specified month and year.
func queryData(acessCode string, month, year int) ([]*html.Node, error) {
	query := fmt.Sprintf(`acao=AnexoVIII&folha=&valida=true&toExcel=false&chaveDeAcesso=%s&mes=%d&ano=%04d`, acessCode, month, year)
	queryURL := fmt.Sprintf(`http://apps.tre-pb.jus.br/transparenciaDadosServidores/infoServidores?%s`, query)
	req, err := http.NewRequest("GET", queryURL, nil)
	if err != nil {
		return nil, fmt.Errorf("error creating GET request to %s: %q", queryURL, err)
	}

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
		nodeReader := strings.NewReader(htmlquery.OutputHTML(node, true))
		if io.Copy(f, nodeReader); err != nil {
			os.Remove(fileName)
			return fmt.Errorf("error copying response content to file: %q", err)
		}
	}
	return nil
}
