package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/360EntSecGroup-Skylar/excelize"
	"github.com/dadosjusbr/storage"
)

const (
	// index of unique register code on the row
	registerCodeIndex = 0

	// index of name on the row
	nameIndex = 1

	// index of role on the row
	roleIndex = 2

	// index of total discount
	totalDiscountIndex = 16

	// index of ceil retention
	ceilRetentionIndex = 13

	// index of income tax
	incomeTaxIndex = 12

	// index of prev contribution
	prevContributionIndex = 11

	// index of income details
	totalIncomeDetailsIndex = 10

	// index of wage
	wageIndex = 4

	// index of total perks
	totalPerkIndex = 6

	// index for "Outras Verbas Remuneratórias, Legais ou Judiciais" at sheet
	otherAmmountsIndex = 5

	// index for "Função de Confiança" at sheet
	loyaltyJobIndex = 6

	// index for "Gratificação Natalina" at sheet
	christmasPerkIndex = 7

	// index of "Férias (1/3 constitucional)" at sheet
	vacacionPerkIndex = 8

	// index of "Abono de Permanência" at sheet
	permanencePerkIndex = 9

	//index of indemnity
	indemnityIndex = 16

	// index of "Outras Remunerações Retroativas/Temporárias"
	temporaryRemunerationIndex = 17
)

var (
	indexies = map[string]map[string]int{
		"remuneracao-de-todos-os-membros-ativos": map[string]int{
			"totalDiscountsIndex":        14,
			"ceilRetentionIndex":         13,
			"incomeTaxIndex":             12,
			"prevContributionIndex":      11,
			"totalIncomeDetailsIndex":    10,
			"wageIndex":                  4,
			"indemnityIndex":             16,
			"temporaryRemunerationIndex": 17,
			"otherAmmountsIndex":         5,
			"loyaltyJobIndex":            6,
			"christmasPerkIndex":         7,
			"vacacionPerkIndex":          8,
			"permanencePerkIndex":        9,
			"nameIndex":                  1,
			"roleIndex":                  2,
			"registerCodeIndex":          0,
		},
		"proventos-de-todos-os-membros-inativos": map[string]int{
			"totalDiscountsIndex":        14,
			"ceilRetentionIndex":         13,
			"incomeTaxIndex":             12,
			"prevContributionIndex":      11,
			"totalIncomeDetailsIndex":    10,
			"wageIndex":                  4,
			"indemnityIndex":             16,
			"temporaryRemunerationIndex": 17,
			"otherAmmountsIndex":         5,
			"loyaltyJobIndex":            6,
			"christmasPerkIndex":         7,
			"vacacionPerkIndex":          8,
			"permanencePerkIndex":        9,
			"nameIndex":                  1,
			"roleIndex":                  2,
			"registerCodeIndex":          0,
		},
	}
)

// Parse parses the xlsx tables
func Parse(paths []string) ([]storage.Employee, error) {
	var employees []storage.Employee
	for _, path := range paths {
		documentIdentification := getFileDocumentation(path)
		indexMap := indexies[documentIdentification]
		fmt.Println(documentIdentification)
		file, err := excelize.OpenFile(path)
		if err != nil {
			return nil, fmt.Errorf("error opening document %s for parse: %q", documentIdentification, err)
		}
		fileMap := file.GetSheetMap()
		rows := file.GetRows(fileMap[1])
		numberOfRows := len(rows)
		var employee storage.Employee
		for index, row := range rows {
			if index == 0 || index == 1 || index == 2 || index == numberOfRows-1 || index == numberOfRows-2 || index == numberOfRows-3 {
				continue
			}
			discounts, err := getDiscounts(row, documentIdentification, indexMap)
			if err != nil {
				return nil, err
			}
			incomeDetails, err := getIncome(row, documentIdentification, indexMap)
			if err != nil {
				return nil, err
			}
			employee = storage.Employee{
				Reg:       row[indexMap["registerCodeIndex"]],
				Name:      row[indexMap["nameIndex"]],
				Role:      row[indexMap["roleIndex"]],
				Type:      getType(documentIdentification),
				Workplace: "mppe",
				Active:    isActive(documentIdentification),
				Income:    incomeDetails,
				Discounts: discounts,
			}
			employees = append(employees, employee)
		}
	}
	return employees, nil
}

// it returns the total discounts sumary
func getDiscounts(row []string, documentIdentification string, indexMap map[string]int) (*storage.Discount, error) {
	totalDiscount, err := strconv.ParseFloat(row[indexMap["totalDiscountIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing total discount from string to float64 for document %s: %q", documentIdentification, err)
	}
	ceilRetention, err := strconv.ParseFloat(row[indexMap["ceilRetentionIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing ceil retention from string to float64 for document %s: %q", documentIdentification, err)
	}
	incomeTax, err := strconv.ParseFloat(row[indexMap["incomeTaxIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing income tax from string to float64 for document %s: %q", documentIdentification, err)
	}
	prevContribution, err := strconv.ParseFloat(row[indexMap["prevContributionIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing prev contribution from string to float64 for document %s: %q", documentIdentification, err)
	}
	return &storage.Discount{
		Total:            totalDiscount,
		CeilRetention:    &ceilRetention,
		IncomeTax:        &incomeTax,
		PrevContribution: &prevContribution,
	}, nil
}

// it returns the incomes sumary
func getIncome(row []string, documentIdentification string, indexMap map[string]int) (*storage.IncomeDetails, error) {
	grossSalary, err := strconv.ParseFloat(row[indexMap["totalIncomeDetailsIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing total of income details from string to float64 for document %s: %q", documentIdentification, err)
	}
	wage, err := strconv.ParseFloat(row[indexMap["wageIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing wage of income details from string to float64 for document %s: %q", documentIdentification, err)
	}
	perks, err := getPerks(row, documentIdentification, indexMap)
	if err != nil {
		return nil, err
	}
	funds, err := getFunds(row, documentIdentification, indexMap)
	if err != nil {
		return nil, err
	}
	indemnity, err := strconv.ParseFloat(row[indexMap["indemnityIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing indemnity from string to float64 for document %s: %q", documentIdentification, err)
	}
	temporaryRemuneration, err := strconv.ParseFloat(row[indexMap["temporaryRemunerationIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing temporary remuneration from string to float64 for document %s: %q", documentIdentification, err)
	}
	return &storage.IncomeDetails{
		Total: grossSalary + indemnity + temporaryRemuneration,
		Wage:  &wage,
		Perks: perks,
		Other: funds,
	}, nil
}

// it retrieves employee perks
func getPerks(row []string, documentIdentification string, indexMap map[string]int) (*storage.Perks, error) {
	indemnity, err := strconv.ParseFloat(row[indexMap["indemnityIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing indemnity from string to float64 for document %s: %q", documentIdentification, err)
	}
	temporaryRemuneration, err := strconv.ParseFloat(row[indexMap["temporaryRemunerationIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing temporary remuneration from string to float64 for document %s: %q", documentIdentification, err)
	}
	others, err := getOthers(row, documentIdentification, indexMap)
	if err != nil {
		return nil, err
	}
	return &storage.Perks{
		Total:  indemnity + temporaryRemuneration,
		Others: others,
	}, nil
}

func getFunds(row []string, documentIdentification string, indexMap map[string]int) (*storage.Funds, error) {
	wage, err := strconv.ParseFloat(row[indexMap["wageIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing wage of income details from string to float64 for document %s: %q", documentIdentification, err)
	}
	return &storage.Funds{
		Total: wage,
	}, nil
}

// get others information about perks
func getOthers(row []string, documentIdentification string, indexMap map[string]int) (map[string]float64, error) {
	otherAmmounts, err := strconv.ParseFloat(row[indexMap["otherAmmountsIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing other ammounts from string to float64 for document %s: %q", documentIdentification, err)
	}
	loyaltyJob, err := strconv.ParseFloat(row[indexMap["loyaltyJobIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing loyalty job from string to float64 for document %s: %q", documentIdentification, err)
	}
	christmasPerk, err := strconv.ParseFloat(row[indexMap["christmasPerkIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing christmas perk from string to float64 for document %s: %q", documentIdentification, err)
	}
	vacacionPerk, err := strconv.ParseFloat(row[indexMap["vacacionPerkIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing vacation perk from string to float64 for document %s: %q", documentIdentification, err)
	}
	permanencePerk, err := strconv.ParseFloat(row[indexMap["permanencePerkIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing permanence perk from string to float64 for document %s: %q", documentIdentification, err)
	}
	indemnity, err := strconv.ParseFloat(row[indexMap["indemnityIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing indemnity from string to float64 for document %s: %q", documentIdentification, err)
	}
	temporaryRemuneration, err := strconv.ParseFloat(row[indexMap["temporaryRemunerationIndex"]], 64)
	if err != nil {
		return nil, fmt.Errorf("error on parsing temporary remuneration from string to float64 for document %s: %q", documentIdentification, err)
	}
	return map[string]float64{
		"otherAmmounts":         otherAmmounts,
		"loyaltyJob":            loyaltyJob,
		"christmasPerk":         christmasPerk,
		"vacacionPerk":          vacacionPerk,
		"permanencePerk":        permanencePerk,
		"indemnity":             indemnity,
		"temporaryRemuneration": temporaryRemuneration,
	}, nil
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
	return strings.Split(name, "/")[2]
}
