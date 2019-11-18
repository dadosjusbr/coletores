package main

import (
	"fmt"
	"math"
	"strings"

	"github.com/dadosjusbr/storage"
)

// parse takes a json filePath and retrieve the array of employees from it.
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

// parseEmployees takes a map in the format returned from the trt13 api and retrieves employees list.
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

// parseCategory will parse a category of employees and return the employee list.
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

// newEmployee creates an employee from a json map.
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

// employeeBasicInfo retrieves the basic information of the employee
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

// employeeType returns employee.Type based in category string.
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

// active returns Employee.Active based in category string.
func active(cat string) bool {
	return !strings.Contains(cat, "Inativos") && !strings.Contains(cat, "Pensionistas")
}

// employeeIncome retrieves employee income information.
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
	in.Total = totalIncome(in)
	return nil
}

// employeeIncomeOthers retrieves the employee funds.
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

// employeeDiscounts retrieves employee discounts.
func employeeDiscounts(d *storage.Discount, emp map[string]interface{}) error {
	discountsMap, err := getMap(emp, "descontos")
	if err != nil {
		return fmt.Errorf("couldn't retrieve discounts map (k: descontos): %q", err)
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
	d.Total = totalDiscounts(d)
	return nil
}

// totalDiscounts returns the sum of discounts.
func totalDiscounts(d *storage.Discount) float64 {
	total := getFloat64Value(d.PrevContribution) + getFloat64Value(d.CeilRetention) + getFloat64Value(d.IncomeTax) + sumMapValues(d.Others)
	return math.Round(total*100) / 100
}

// grossIncome returns the sum of incomes.
func totalIncome(in *storage.IncomeDetails) float64 {
	o := *in.Other
	totalOthers := getFloat64Value(o.PersonalBenefits) + getFloat64Value(o.EventualBenefits) +
		getFloat64Value(o.PositionOfTrust) + getFloat64Value(o.Daily) + getFloat64Value(o.Gratification) + sumMapValues(o.Others)
	total := getFloat64Value(in.Wage) + in.Perks.Total + totalOthers
	return math.Round(total*100) / 100
}
