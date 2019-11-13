package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"strings"

	storage "github.com/dadosjusbr/storage"
)

func parse(filePath string) ([]storage.Employee, error) {
	resultJSON, err := readJSON(filePath)
	if err != nil {
		return nil, fmt.Errorf("error reading json: %q", err)
	}

	emps, err := parseEmployees(resultJSON)
	if err != nil {
		return nil, fmt.Errorf("error parsing employees: %q", err)
	}
	return emps, nil
}

func readJSON(filePath string) (map[string]interface{}, error) {
	jsonFile, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("error trying to open file at (%s) : %q", filePath, err)
	}
	defer jsonFile.Close()

	byteValue, err := ioutil.ReadAll(jsonFile)
	var result map[string]interface{}
	err = json.Unmarshal(byteValue, &result)
	if err != nil {
		return nil, fmt.Errorf("error trying to unmarshal json: %q", err)
	}
	return result, nil
}

func parseEmployees(m map[string]interface{}) ([]storage.Employee, error) {
	var employees []storage.Employee
	mapArray, err := getSliceOfMaps(m, "listaAnexoviiiServidorMagistradoPensionista")
	if err != nil {
		return nil, fmt.Errorf("error trying to retrieve array of categories: %q", err)
	}
	for i, category := range mapArray {
		empSlice, err := parseCategory(category)
		if err != nil {
			return nil, fmt.Errorf("error parsing category(%d): %q", i, err)
		}
		employees = append(employees, empSlice...)
	}
	return employees, nil
}

func parseCategory(category map[string]interface{}) ([]storage.Employee, error) {
	var employees []storage.Employee
	var catInfo string
	if err := getString(&catInfo, category, "rotuloCabecalho"); err != nil {
		return nil, fmt.Errorf("couldn't find string for role: %q", err)
	}

	cMap, err := getSliceOfMaps(category, "listaAnexoviii")
	if err != nil {
		return nil, fmt.Errorf("couldn't find map for category: %q", err)
	}

	for i, empMap := range cMap {
		newEmp, err := newEmployee(empMap, catInfo)
		if err != nil {
			return nil, fmt.Errorf("error parsing employee at (%s: %d): %q", catInfo, i, err)
		}
		employees = append(employees, newEmp)
	}
	return employees, nil
}

func newEmployee(emp map[string]interface{}, catInfo string) (storage.Employee, error) {
	// Creating employee struct as needed.
	e := storage.Employee{
		Income:    &storage.IncomeDetails{Other: &storage.Funds{}, Perks: &storage.Perks{}},
		Discounts: &storage.Discount{},
	}
	if err := employeeBasicInfo(&e, emp, catInfo); err != nil {
		return e, fmt.Errorf("error parsing employee basic info: %q", err)
	}
	if err := employeeIncome(e.Income, emp); err != nil {
		return e, fmt.Errorf("error parsing employee income: %q", err)
	}
	if err := employeeDiscounts(e.Discounts, emp); err != nil {
		return e, fmt.Errorf("error parsing employee income: %q", err)
	}
	return e, nil
}

func employeeBasicInfo(e *storage.Employee, emp map[string]interface{}, catInfo string) error {
	if err := getString(&e.Name, emp, "nome"); err != nil {
		return fmt.Errorf("couldn't retrieve employee name: %q", err)
	}
	if err := getString(&e.Role, emp, "cargo"); err != nil {
		return fmt.Errorf("couldn't retrieve employee role: %q", err)
	}
	if err := getString(&e.Workplace, emp, "lotacao"); err != nil {
		return fmt.Errorf("couldn't retrieve employee workplace: %q", err)
	}
	if err := getString(&e.Reg, emp, "id"); err != nil {
		return fmt.Errorf("couldn't retrieve employee id: %q", err)
	}
	e.Active = active(catInfo)
	e.Type = employeeType(catInfo)
	return nil
}

func employeeType(cat string) string {
	if strings.Contains(cat, "Servidores") {
		return "servidor"
	} else if strings.Contains(cat, "Magistrados") {
		return "membro"
	} else if strings.Contains(cat, "Pensionistas") {
		return "pensionista"
	}
	return ""
}

func active(cat string) bool {
	return !strings.Contains(cat, "Inativos")
}

func employeeIncome(in *storage.IncomeDetails, emp map[string]interface{}) error {
	incomeMap, err := getMap(emp, "rendimentos")
	if err != nil {
		return fmt.Errorf("couldn't retrieve income map (k: rendimentos): %q", err)
	}
	if err := getFloat64(&in.Wage, incomeMap, "remuneracaoParadigma"); err != nil {
		return fmt.Errorf("couldn't retrieve employee wage: %q", err)
	}
	if err := getFloat64(&in.Perks.Total, incomeMap, "indenizacoes"); err != nil {
		return fmt.Errorf("couldn't retrieve employee total perks: %q", err)
	}
	if err := employeeIncomeOthers(in.Other, emp); err != nil {
		return fmt.Errorf("error retrieving employee other incomes: %q", err)
	}
	return nil
}

func employeeIncomeOthers(o *storage.Funds, emp map[string]interface{}) error {
	incomeMap, err := getMap(emp, "rendimentos")
	if err != nil {
		return fmt.Errorf("couldn't retrieve income map (k: rendimentos): %q", err)
	}
	if err := getFloat64(&o.PersonalBenefits, incomeMap, "vantagensPessoais"); err != nil {
		return fmt.Errorf("couldn't retrieve employee personal benefits: %q", err)
	}
	if err := getFloat64(&o.EventualBenefits, incomeMap, "vantagensEventuais"); err != nil {
		return fmt.Errorf("couldn't retrieve employee eventual benefits: %q", err)
	}
	if err := getFloat64(&o.Gratification, incomeMap, "gratificacao"); err != nil {
		return fmt.Errorf("couldn't retrieve employee gratifications: %q", err)
	}
	//Revisar. Pensionistas recebem por subsidio
	if err := getFloat64(&o.PositionOfTrust, incomeMap, "subsidio"); err != nil {
		return fmt.Errorf("couldn't retrieve employee position of trust: %q", err)
	}
	if err := getFloat64(&o.OriginPosition, emp, "remuneracaoOrgaoOrigem"); err != nil {
		return fmt.Errorf("couldn't retrieve employee total perks: %q", err)
	}
	if err := getFloat64(&o.Daily, emp, "diarias"); err != nil {
		return fmt.Errorf("couldn't retrieve employee total perks: %q", err)
	}
	return nil
}

func employeeDiscounts(d *storage.Discount, emp map[string]interface{}) error {
	discountsMap, err := getMap(emp, "descontos")
	if err != nil {
		return fmt.Errorf("couldn't retrieve discounts map (k: rendimentos): %q", err)
	}
	if err := getFloat64(&d.PrevContribution, discountsMap, "previdenciaPublica"); err != nil {
		return fmt.Errorf("couldn't retrieve employee Prev Contribution: %q", err)
	}
	if err := getFloat64(&d.IncomeTax, discountsMap, "impostoRenda"); err != nil {
		return fmt.Errorf("couldn't retrieve employee income tax: %q", err)
	}
	if err := getFloat64(&d.CeilRetention, discountsMap, "retencaoTeto"); err != nil {
		return fmt.Errorf("couldn't retrieve employee income tax: %q", err)
	}
	// Others
	d.Others = make(map[string]float64)
	var sundry float64
	if err := getFloat64(&sundry, discountsMap, "descontosDiversos"); err != nil {
		return fmt.Errorf("couldn't retrieve employee sundry: %q", err)
	}
	d.Others["sundry"] = sundry
	return nil
}
