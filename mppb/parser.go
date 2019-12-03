package main

import (
	"fmt"
	"strings"

	"github.com/knieriem/odf/ods"
)

// Data type
const (
	ESTAGIARIOS  = 0
	INDENIZACOES = 1
	REMUNERACOES = 2
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
	for _, file := range files {
		var doc ods.Doc
		f, err := ods.Open(file)
		if err != nil {
			return fmt.Errorf("ods.Open error(%s): %q", file, err)
		}
		f.ParseContent(&doc)
		fileType := dataType(file)
		if err := assertHeaders(doc, fileType); err != nil {
			logError("assertHeaders() for %s error: %q", file, err)
		}
		f.Close()
	}
	return nil
}

func dataType(fileName string) int {
	if strings.Contains(fileName, "indenizacoes") {
		return INDENIZACOES
	} else if strings.Contains(fileName, "estagiarios") {
		return ESTAGIARIOS
	} else if strings.Contains(fileName, "membros") || strings.Contains(fileName, "servidores") {
		return REMUNERACOES
	}
	return -1
}

func getHeaders(doc ods.Doc, fileType int) []string {
	var headers []string
	raw := doc.Table[0].Strings()[5:8]
	for row := range raw {
		for col := range raw[row] {
			raw[row][col] = strings.ToUpper(strings.ReplaceAll(raw[row][col], "\n", " "))
		}
	}
	switch fileType {
	case INDENIZACOES:
		headers = append(headers, raw[0][:4]...)
		headers = append(headers, raw[2][4:]...)
		break
	case ESTAGIARIOS:
		headers = append(headers, raw[0][:3]...)
		headers = append(headers, raw[2][3:9]...)
		headers = append(headers, raw[1][9])
		headers = append(headers, raw[2][10:]...)
		headers = append(headers, raw[1][13])
		headers = append(headers, raw[0][14:]...)
		break
	case REMUNERACOES:
		headers = append(headers, raw[0][:4]...)
		headers = append(headers, raw[2][4:10]...)
		headers = append(headers, raw[1][10:13]...)
		headers = append(headers, raw[2][13:]...)
		break
	}
	return headers
}

func assertHeaders(doc ods.Doc, fileType int) error {
	headers := getHeaders(doc, fileType)
	switch fileType {
	case REMUNERACOES:
		for key, value := range mapping {
			if err := containsHeader(headers, key, value); err != nil {
				return err
			}
		}
		return nil
	case ESTAGIARIOS:
		for key, value := range mapping {
			if key == "MATRÍCULA" {
				continue
			}
			if err := containsHeader(headers, key, value-1); err != nil {
				return err
			}
		}
		return nil
	default:
		return fmt.Errorf("couldn't fit fileType: %d", fileType)
	}
}

func containsHeader(headers []string, key string, value int) error {
	if strings.Contains(headers[value], key) {
		return nil
	}
	return fmt.Errorf("couldn't find %s at position %d", key, value)
}
