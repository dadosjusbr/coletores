package main

import (
	"fmt"
	"strings"

	"github.com/knieriem/odf/ods"
)

var mapping = map[string]int{
	"MATRÍCULA":             0,
	"NOME":                  1,
	"CARGO":                 2,
	"LOTAÇÃO":               3,
	"CARGO EFETIVO":         4,
	"OUTRAS VERBAS":         5,
	"CARGO EM COMISSÃO":     6,
	"GRATIFICAÇÃO NATALINA": 7,
	"FÉRIAS":                8,
	"PERMANÊNCIA":           9,
	"TEMPORÁRIAS":           10,
	"INDENIZATÓRIAS":        11,
	"PREVIDENCIÁRIA":        13,
	"IMPOSTO":               14,
	"RETENÇÃO":              15,
}

// Parser parses the ods tables.
func Parser(files []string) error {
	var doc ods.Doc
	for _, file := range files {
		f, err := ods.Open(file)
		if err != nil {
			return fmt.Errorf("ods.Open error(%s): %q", file, err)
		}
		f.ParseContent(&doc)
		/*
			json, err := json.MarshalIndent(getHeaders(doc), "", " ")
			if err != nil {
				return fmt.Errorf("marshalling error")
			}
			fmt.Printf("%s", json)
		*/

		if err := assertHeaders(doc); err != nil {
			return fmt.Errorf("assertHeaders() error: %q", err)
		}

	}
	return nil
}

func getHeaders(doc ods.Doc) [][]string {
	headers := doc.Table[0].Strings()[5:8]
	for row := range headers {
		for col := range headers[row] {
			headers[row][col] = strings.ToUpper(strings.ReplaceAll(headers[row][col], "\n", " "))
		}
	}
	return headers
}

func assertHeaders(doc ods.Doc) error {
	headers := getHeaders(doc)
	for key, value := range mapping {
		if err := containsHeader(headers, key, value); err != nil {
			return err
		}
	}
	return nil
}

func containsHeader(headers [][]string, key string, value int) error {
	for row := range headers {
		for i, cell := range headers[row] {
			if strings.Contains(cell, key) {
				if i != value {
					return fmt.Errorf("%s should be at position %d, but was in %d instead", key, value, i)
				}
				return nil
			}
		}
	}
	return fmt.Errorf("couldn't find %s", key)
}
