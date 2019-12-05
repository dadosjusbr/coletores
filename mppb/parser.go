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

// Mapping of headers to indexes
var headersMap = []map[string]int{
	ESTAGIARIOS: map[string]int{
		"NOME":                0,
		"CARGO":               1,
		"LOTAÇÃO":             2,
		"REMUNERAÇÃO":         3,
		"OUTRAS VERBAS":       4,
		"FUNÇÃO DE CONFIANÇA": 5,
		"13º VENCIMENTO":      6,
		"FÉRIAS":              7,
		"PERMANÊNCIA":         8,
		"PREVIDENCIÁRIA":      10,
		"IMPOSTO":             11,
		"RETENÇÃO":            12,
		"TEMPORÁRIAS":         16,
		"INDENIZAÇÕES":        15,
	},

	INDENIZACOES: map[string]int{
		"MATRÍCULA":      0,
		"ALIMENTAÇÃO":    4,
		"SAÚDE":          5,
		"PECÚNIA":        6,
		"MORADIA":        7,
		"NATALIDADE":     8,
		"AJUDA DE CUSTO": 9, // first col for eventualBenefits
		"DESPESA":        21,
	},

	REMUNERACOES: map[string]int{
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
	},
}

// Parse parses the ods tables.
func Parse(files []string) error {
	data, err := dataAsSlices(files)
	if err != nil {
		return fmt.Errorf("error trying to parse data as slices: %q", err)
	}
	// TODO
	fmt.Printf("%v\n", data)
	return nil
}

func dataAsSlices(files []string) (map[int][][]string, error) {
	var (
		perksAndbenefits [][]string
		employees        [][]string
		interns          [][]string
	)
	for _, file := range files {
		var doc ods.Doc
		f, err := ods.Open(file)
		if err != nil {
			return nil, fmt.Errorf("ods.Open error(%s): %q", file, err)
		}
		f.ParseContent(&doc)
		fileType := dataType(file)
		if err := assertHeaders(doc, fileType); err != nil {
			logError("assertHeaders() for %s error: %q", file, err)
			continue
		}
		switch fileType {
		case REMUNERACOES:
			employees = append(employees, getEmployees(doc)...)
			break
		case ESTAGIARIOS:
			interns = append(interns, getEmployees(doc)...)
			break
		case INDENIZACOES:
			perksAndbenefits = append(perksAndbenefits, getEmployees(doc)...)
			break
		}
		f.Close()
	}
	return map[int][][]string{
		REMUNERACOES: employees,
		ESTAGIARIOS:  interns,
		INDENIZACOES: perksAndbenefits,
	}, nil
}

func dataType(fileName string) int {
	if strings.Contains(fileName, "indenizacoes") {
		return INDENIZACOES
	} else if strings.Contains(fileName, "estagiarios") {
		return ESTAGIARIOS
	} else if strings.Contains(fileName, "membros") || strings.Contains(fileName, "servidores") || strings.Contains(fileName, "aposentados") {
		return REMUNERACOES
	}
	return -1
}

func getEmployees(doc ods.Doc) [][]string {
	var lastLine int
	for i, values := range doc.Table[0].Strings() {
		if len(values) < 1 {
			continue
		}
		if values[0] == "TOTAL GERAL" {
			lastLine = i - 1
			break
		}
	}
	if lastLine == 0 {
		return [][]string{}
	}
	return cleanStrings(doc.Table[0].Strings()[10:lastLine])
}

func getHeaders(doc ods.Doc, fileType int) []string {
	var headers []string
	raw := cleanStrings(doc.Table[0].Strings()[5:8])
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
	for key, value := range headersMap[fileType] {
		if err := containsHeader(headers, key, value); err != nil {
			return err
		}
	}
	return nil
}

func containsHeader(headers []string, key string, value int) error {
	if strings.Contains(headers[value], key) {
		return nil
	}
	return fmt.Errorf("couldn't find %s at position %d", key, value)
}

func cleanStrings(raw [][]string) [][]string {
	for row := range raw {
		for col := range raw[row] {
			raw[row][col] = strings.ToUpper(strings.ReplaceAll(strings.ReplaceAll(raw[row][col], "N/D", ""), "\n", " "))
		}
	}
	return raw
}
