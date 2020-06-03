package main

import (
	"fmt"
	"math"
	"strings"

	"github.com/dadosjusbr/storage"
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
	ESTAGIARIOS: {
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

	INDENIZACOES: {
		"MATRÍCULA":             0,
		"ALIMENTAÇÃO":           4,
		"SAÚDE":                 5,
		"PECÚNIA":               6,
		"MORADIA":               7,
		"LICENÇA COMPENSATÓRIA": 8,
		"NATALIDADE":            9,
		"AJUDA DE CUSTO":        10, // first col for eventualBenefits
		"DESPESA":               22,
	},

	REMUNERACOES: {
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
func Parse(files []string) ([]storage.Employee, error) {
	var employees []storage.Employee
	var parseErr bool

	perks, err := retrievePerksData(files)
	if err != nil {
		return nil, fmt.Errorf("error trying to retrieve perks data: %q", err)
	}
	for _, f := range files {
		if dataType(f) == INDENIZACOES {
			continue
		}

		data, err := dataAsSlices(f)
		if err != nil {
			return nil, fmt.Errorf("error trying to parse data as slices(%s): %q", f, err)
		}
		if len(data) == 0 {
			return nil, fmt.Errorf("No data to be parsed. (%s)", f)
		}

		emps, ok := retrieveEmployees(data, perks, f)
		if !ok {
			parseErr = true
		}
		employees = append(employees, emps...)
	}
	if parseErr {
		return employees, fmt.Errorf("parse error")
	}
	return employees, nil
}

func retrievePerksData(files []string) ([][]string, error) {
	for _, f := range files {
		if dataType(f) == INDENIZACOES {
			return dataAsSlices(f)
		}
	}
	return nil, nil
}

func retrieveEmployees(emps [][]string, perks [][]string, fileName string) ([]storage.Employee, bool) {
	ok := true
	var employees []storage.Employee
	fileType := dataType(fileName)
	for _, emp := range emps {
		var err error
		var newEmp *storage.Employee
		if fileType == REMUNERACOES {
			empPerks := retrievePerksLine(emp[0], perks)
			if newEmp, err = newEmployee(emp, empPerks, fileName); err != nil {
				ok = false
				logError("error retrieving employee from %s: %q", fileName, err)
				continue
			}
		} else if fileType == ESTAGIARIOS {
			if newEmp, err = newIntern(emp, fileName); err != nil {
				ok = false
				logError("error retrieving employee from %s: %q", fileName, err)
				continue
			}
		}
		employees = append(employees, *newEmp)
	}
	return employees, ok
}

func retrievePerksLine(regNum string, perks [][]string) []string {
	if perks == nil || len(perks) == 0 {
		return nil
	}
	for _, p := range perks {
		if p[headersMap[INDENIZACOES]["MATRÍCULA"]] == regNum {
			return p
		}
	}
	return nil
}

func newIntern(emp []string, fileName string) (*storage.Employee, error) {
	fileType := dataType(fileName)
	var newEmp storage.Employee
	var err error
	newEmp.Name = retrieveString(emp, "NOME", fileType)
	newEmp.Role = retrieveString(emp, "CARGO", fileType)
	newEmp.Workplace = retrieveString(emp, "LOTAÇÃO", fileType)
	newEmp.Type = employeeType(fileName)
	newEmp.Active = employeeActive(fileName)
	if newEmp.Income, err = internIncomeInfo(emp, fileType); err != nil {
		return nil, fmt.Errorf("error parsing new employee: %q", err)
	}
	if newEmp.Discounts, err = employeeDiscountInfo(emp, fileType); err != nil {
		return nil, fmt.Errorf("error parsing new employee: %q", err)
	}
	return &newEmp, nil
}

func newEmployee(emp []string, perks []string, fileName string) (*storage.Employee, error) {
	fileType := dataType(fileName)
	var newEmp storage.Employee
	var err error
	newEmp.Reg = retrieveString(emp, "MATRÍCULA", fileType)
	newEmp.Name = retrieveString(emp, "NOME", fileType)
	newEmp.Role = retrieveString(emp, "CARGO", fileType)
	newEmp.Workplace = retrieveString(emp, "LOTAÇÃO", fileType)
	newEmp.Type = employeeType(fileName)
	newEmp.Active = employeeActive(fileName)
	if newEmp.Income, err = employeeIncomeInfo(emp, perks, fileType); err != nil {
		return nil, fmt.Errorf("error parsing new employee: %q", err)
	}
	if newEmp.Discounts, err = employeeDiscountInfo(emp, fileType); err != nil {
		return nil, fmt.Errorf("error parsing new employee: %q", err)
	}
	return &newEmp, nil
}

func employeeActive(fileName string) bool {
	return (strings.Contains(fileName, "Inativos") || strings.Contains(fileName, "aposentados")) == false
}

func employeeType(fileName string) string {
	if strings.Contains(fileName, "servidor") {
		return "servidor"
	} else if strings.Contains(fileName, "membro") {
		return "membro"
	} else if strings.Contains(fileName, "aposentados") {
		return "pensionista"
	} else if strings.Contains(fileName, "estagiario") {
		return "estagiario"
	}
	return ""
}

func internIncomeInfo(emp []string, fileType int) (*storage.IncomeDetails, error) {
	var err error
	var in storage.IncomeDetails
	in.Perks = &storage.Perks{}
	in.Other = &storage.Funds{}
	if err = retrieveFloat64(&in.Wage, emp, "REMUNERAÇÃO", fileType); err != nil {
		return nil, fmt.Errorf("error retrieving employee income info: %q", err)
	}
	if err = retrieveFloat64(&in.Perks.Total, emp, "INDENIZAÇÕES", fileType); err != nil {
		return nil, fmt.Errorf("error retrieving employee income info: %q", err)
	}

	pb, err := sumKeyValues(emp, []string{"OUTRAS VERBAS", "PERMANÊNCIA"}, fileType)
	if err != nil {
		return nil, fmt.Errorf("error retrieving funds(regNum: %s): %q", emp[0], err)
	}
	in.Other.PersonalBenefits = &pb
	eb, err := sumKeyValues(emp, []string{"FÉRIAS", "13º VENCIMENTO", "TEMPORÁRIAS"}, fileType)
	if err != nil {
		return nil, fmt.Errorf("error retrieving funds(regNum: %s): %q", emp[0], err)
	}
	if err := retrieveFloat64(&in.Other.PositionOfTrust, emp, "FUNÇÃO DE CONFIANÇA", fileType); err != nil {
		return nil, fmt.Errorf("error retrieving funds(regNum: %s): %q", emp[0], err)
	}
	in.Other.EventualBenefits = &eb
	total := eb + pb + getFloat64Value(in.Other.PositionOfTrust)
	in.Other.Total = math.Round(total*100) / 100
	in.Total = totalIncome(in)
	return &in, nil
}

func employeeIncomeInfo(emp []string, perks []string, fileType int) (*storage.IncomeDetails, error) {
	var err error
	var in storage.IncomeDetails
	if err = retrieveFloat64(&in.Wage, emp, "CARGO EFETIVO", fileType); err != nil {
		return nil, fmt.Errorf("error retrieving employee income info: %q", err)
	}
	if in.Perks, err = employeePerks(emp[headersMap[fileType]["MATRÍCULA"]], perks); err != nil {
		return nil, fmt.Errorf("error retrieving employee perks: %q", err)
	}
	if in.Other, err = employeeIncomeFunds(emp, perks, fileType); err != nil {
		return nil, fmt.Errorf("error retrieving employee funds: %q", err)
	}
	in.Total = totalIncome(in)
	return &in, nil
}

func employeePerks(reg string, perks []string) (*storage.Perks, error) {
	var inPerks storage.Perks
	if perks == nil || len(perks) == 0 {
		inPerks.Total = 0
		return &inPerks, nil
	}

	if reg != perks[headersMap[INDENIZACOES]["MATRÍCULA"]] {
		return nil, fmt.Errorf("error retrieving perks: employee reg does not match perks. %s, %v", reg, perks)
	}
	if err := retrieveFloat64(&inPerks.Food, perks, "ALIMENTAÇÃO", INDENIZACOES); err != nil {
		return nil, fmt.Errorf("error retrieving perks(regNum: %s): %q", reg, err)
	}
	if err := retrieveFloat64(&inPerks.Health, perks, "SAÚDE", INDENIZACOES); err != nil {
		return nil, fmt.Errorf("error retrieving perks(regNum: %s): %q", reg, err)
	}
	if err := retrieveFloat64(&inPerks.HousingAid, perks, "MORADIA", INDENIZACOES); err != nil {
		return nil, fmt.Errorf("error retrieving perks(regNum: %s): %q", reg, err)
	}
	if err := retrieveFloat64(&inPerks.BirthAid, perks, "NATALIDADE", INDENIZACOES); err != nil {
		return nil, fmt.Errorf("error retrieving perks(regNum: %s): %q", reg, err)
	}
	if err := retrieveFloat64(&inPerks.Subsistence, perks, "AJUDA DE CUSTO", INDENIZACOES); err != nil {
		return nil, fmt.Errorf("error retrieving perks(regNum: %s): %q", reg, err)
	}
	var pecunia float64
	if err := retrieveFloat64(&pecunia, perks, "PECÚNIA", INDENIZACOES); err != nil {
		return nil, fmt.Errorf("error retrieving perks(regNum: %s): %q", reg, err)
	}
	var compens float64
	if err := retrieveFloat64(&compens, perks, "LICENÇA COMPENSATÓRIA", INDENIZACOES); err != nil {
		return nil, fmt.Errorf("error retrieving perks(regNum: %s): %q", reg, err)
	}
	inPerks.Others = map[string]float64{"pecunia": pecunia, "Licença Compensatória": compens}
	inPerks.Total = totalPerks(inPerks)
	return &inPerks, nil
}

func employeeIncomeFunds(emp []string, perks []string, fileType int) (*storage.Funds, error) {
	var o storage.Funds
	pb, err := sumKeyValues(emp, []string{"OUTRAS VERBAS", "PERMANÊNCIA"}, fileType)
	if err != nil {
		return nil, fmt.Errorf("error retrieving funds(regNum: %s): %q", emp[0], err)
	}
	o.PersonalBenefits = &pb
	ebKeys, err := sumKeyValues(emp, []string{"FÉRIAS", "GRATIFICAÇÃO NATALINA"}, fileType)
	if err != nil {
		return nil, fmt.Errorf("error retrieving funds(regNum: %s): %q", emp[0], err)
	}
	var ebPerks float64
	if perks != nil && len(perks) > 0 {
		ebPerks, err = sumIndexes(perks, 11, 21)
		if err != nil {
			return nil, fmt.Errorf("error retrieving funds(regNum: %s): %q", emp[0], err)
		}
	}
	eb := math.Round((ebPerks+ebKeys)*100) / 100
	o.EventualBenefits = &eb
	if err := retrieveFloat64(&o.PositionOfTrust, emp, "CARGO EM COMISSÃO", fileType); err != nil {
		return nil, fmt.Errorf("error retrieving funds(regNum: %s): %q", emp[0], err)
	}
	total := eb + pb + getFloat64Value(o.PositionOfTrust)
	o.Total = math.Round(total*100) / 100
	return &o, nil
}

func totalPerks(p storage.Perks) float64 {
	return getFloat64Value(p.Food, p.Health, p.HousingAid, p.BirthAid, p.Subsistence) + sumMapValues(p.Others)
}

func totalIncome(in storage.IncomeDetails) float64 {
	total := getFloat64Value(in.Wage)
	if in.Other != nil {
		total += in.Other.Total
	}
	if in.Perks != nil {
		total += in.Perks.Total
	}
	return math.Round(total*100) / 100
}

func employeeDiscountInfo(emp []string, fileType int) (*storage.Discount, error) {
	var d storage.Discount
	if err := retrieveFloat64(&d.PrevContribution, emp, "PREVIDENCIÁRIA", fileType); err != nil {
		return nil, fmt.Errorf("error retrieving discounts(regNum: %s): %q", emp[0], err)
	}
	if err := retrieveFloat64(&d.CeilRetention, emp, "RETENÇÃO", fileType); err != nil {
		return nil, fmt.Errorf("error retrieving discounts(regNum: %s): %q", emp[0], err)
	}
	if err := retrieveFloat64(&d.IncomeTax, emp, "IMPOSTO", fileType); err != nil {
		return nil, fmt.Errorf("error retrieving discounts(regNum: %s): %q", emp[0], err)
	}
	d.Total = getFloat64Value(d.PrevContribution, d.CeilRetention, d.IncomeTax)
	return &d, nil
}

func dataAsSlices(file string) ([][]string, error) {
	var result [][]string
	var doc ods.Doc
	f, err := ods.Open(file)
	if err != nil {
		return nil, fmt.Errorf("ods.Open error(%s): %q", file, err)
	}
	f.ParseContent(&doc)
	fileType := dataType(file)
	if err := assertHeaders(doc, fileType); err != nil {
		return nil, fmt.Errorf("assertHeaders() for %s error: %q", file, err)
	}
	result = append(result, getEmployees(doc)...)
	f.Close()
	return result, nil
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
