package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"

	"github.com/antchfx/htmlquery"
	"golang.org/x/net/html"
	"golang.org/x/net/html/charset"
)

// crawl will access the TRE-PB api and retrieve payment files for a given month and year.
// name and cpf might be necessary to get an api key if no access code is saved in cache file.
func crawl(filePath, name, cpf string, month, year int) error {
	acessCode, err := accessCode(name, cpf)
	if err != nil {
		return fmt.Errorf("Access Code Error: %q", err)
	}

	data, err := queryData(acessCode, month, year)
	if err != nil {
		return fmt.Errorf("Query data error: %q", err)
	}

	if err = save(filePath, data); err != nil {
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

// save creates a file in the filePath and save the data nodes to it.
func save(filePath string, data []*html.Node) error {
	f, err := os.Create(filePath)
	if err != nil {
		return fmt.Errorf("error creating file(%s):%q", filePath, err)
	}
	defer f.Close()

	for _, node := range data {
		r, err := charset.NewReader(strings.NewReader(htmlquery.OutputHTML(node, true)), "latin1")
		if err != nil {
			return err
		}

		if _, err = io.Copy(f, r); err != nil {
			os.Remove(filePath)
			return fmt.Errorf("error copying response content to file: %q", err)
		}
	}
	return nil
}
