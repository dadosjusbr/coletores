package main

import (
	"fmt"

	"github.com/360EntSecGroup-Skylar/excelize"
	"github.com/dadosjusbr/storage"
)

const (
	// page name to process
	sheetName = "Sheet"

	// index of unique register code on the row
	registerCodeIndex = 0

	// index of name on the row
	nameIndex = 1

	// index of role on the row
	roleIndex = 2
)

// Parse parses the xlsx tables
func Parse(paths []string) ([]storage.Employee, error) {
	var employees []storage.Employee
	for _, path := range paths {
		documentIdentification := getFileDocumentation(path)
		file, err := excelize.OpenFile(path)
		if err != nil {
			return nil, fmt.Errorf("error opening document %s for parse: %q", documentIdentification, err)
		}
		rows := file.GetRows(sheetName)
		numberOfRows := len(rows)
		var employee storage.Employee
		for index, row := range rows {
			if index == 1 || index == 2 || index == 3 || index == numberOfRows-1 {
				continue
			}
			employee = storage.Employee{
				Reg:       row[registerCodeIndex],
				Name:      row[nameIndex],
				Role:      row[roleIndex],
				Type:      getType(documentIdentification),
				Workplace: "mppe",
				Active:    isActive(documentIdentification),
				Income:    getIncome(row),
				Discounts: getDiscounts(row),
			}
			employees = append(employees, employee)
		}
	}
	return employees, nil
}

func getDiscounts(row []string) *storage.Discount {
	return nil
}

func getIncome(row []string) *storage.IncomeDetails {
	return nil
}

// it returns the employee type
func getType(documentIdentification string) string {
	switch documentIdentification {
	case "proventos-de-todos-os-membros-inativos":
		return "membro"
	case "proventos-de-todos-os-servidores-inativos":
		return "servidor"
	case "remuneracao-de-todos-os-membros-ativos":
		return "membro"
	case "remuneracao-de-todos-os-servidores-atuvos":
		return "servidor"
	case "valores-percebidos-por-todos-os-colaboradores":
		return "colaborador"
	case "valores-percebidos-por-todos-os-pensionistas":
		return "pensionista"
	default:
		return "indefinido"
	}
}

// it checks if the document is of active members or not
func isActive(documentIdentification string) bool {
	switch documentIdentification {
	case "proventos-de-todos-os-membros-inativos":
		return false
	case "proventos-de-todos-os-servidores-inativos":
		return false
	case "verbas-referentes-a-exercicios-anteriores":
		return false
	case "verbas-indenizatorias-e-outras-remuneracoes-temporarias":
		return false
	case "valores-percebidos-por-todos-os-pensionistas":
		return false
	default:
		return true
	}
}

// it cuts off month, year and extension from name
// to get file name
func getFileDocumentation(fileName string) string {
	fileSize := len(fileName)
	name := fileName[0 : fileSize-13]
	return name
}
