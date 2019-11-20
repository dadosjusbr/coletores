package main

import (
	"encoding/json"
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

	// Employee list back to json
	cMapJSON, err := json.Marshal(cMap)
	if err != nil {
		return nil, fmt.Errorf("error marshaling employee list from category: %q", err)
	}

	// Translate employee list to []trt13Employee
	var trt13Employees []trt13Employee
	err = json.Unmarshal(cMapJSON, &trt13Employees)
	if err != nil {
		return nil, fmt.Errorf("error unmarshaling employee list from category: %q", err)
	}

	for i, emp := range trt13Employees {
		newEmp := newEmployee(emp, catInfo)
		if err != nil {
			return nil, fmt.Errorf("error parsing employee at (%s: %d): %q", catInfo, i, err)
		}
		employees = append(employees, newEmp)
	}
	return employees, nil
}

// newEmployee creates an storage.employee from a trt13Employee
func newEmployee(emp trt13Employee, catInfo string) storage.Employee {
	e := storage.Employee{}
	e.Reg = fmt.Sprintf("%.0f", getFloat64Value(emp.Reg))
	e.Name = getStringValue(emp.Name)
	e.Role = getStringValue(emp.Role)
	e.Workplace = getStringValue(emp.Workplace)
	e.Active = active(catInfo)
	e.Type = employeeType(catInfo)
	e.Income = employeeIncome(emp)
	e.Discounts = employeeDiscounts(emp)
	return e
}

// employeeIncome creates an *storage.IncomeDetails from a trt13Employee
func employeeIncome(emp trt13Employee) *storage.IncomeDetails {
	in := storage.IncomeDetails{Perks: &storage.Perks{}}
	in.Wage = emp.Income.Wage
	in.Perks.Total = getFloat64Value(emp.Income.Perks)
	in.Other = employeeFunds(emp)
	in.Total = totalIncome(in)
	return &in
}

// employeeFunds creates an *storage.Funds from a trt13Employee
func employeeFunds(emp trt13Employee) *storage.Funds {
	o := storage.Funds{}
	o.PersonalBenefits = emp.Income.PersonalBenefits
	o.EventualBenefits = emp.Income.EventualBenefits
	o.PositionOfTrust = emp.Income.Subsidio
	o.Gratification = emp.Income.Gratification
	o.Daily = emp.Daily
	o.OriginPosition = emp.OriginPosition
	o.Total = totalFunds(o)
	return &o
}

// employeeDiscounts creates an *storage.Discount from a trt13Employee
func employeeDiscounts(emp trt13Employee) *storage.Discount {
	d := storage.Discount{}
	d.PrevContribution = emp.Discount.PrevContribution
	d.CeilRetention = emp.Discount.CeilRetantion
	d.IncomeTax = emp.Discount.IncomeTax
	d.Others = map[string]float64{"other_discounts": getFloat64Value(emp.Discount.Sundry)}
	d.Total = totalDiscounts(d)
	return &d
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

// totalDiscounts returns the sum of discounts.
func totalDiscounts(d storage.Discount) float64 {
	total := getFloat64Value(d.PrevContribution) + getFloat64Value(d.CeilRetention) + getFloat64Value(d.IncomeTax) + sumMapValues(d.Others)
	return math.Round(total*100) / 100
}

// totalFunds returns the sum of funds.
func totalFunds(f storage.Funds) float64 {
	total := getFloat64Value(f.PersonalBenefits) + getFloat64Value(f.EventualBenefits) +
		getFloat64Value(f.PositionOfTrust) + getFloat64Value(f.Daily) + getFloat64Value(f.Gratification) + sumMapValues(f.Others)
	return math.Round(total*100) / 100
}

// grossIncome returns the sum of incomes.
func totalIncome(in storage.IncomeDetails) float64 {
	total := getFloat64Value(in.Wage) + in.Perks.Total + in.Other.Total
	return math.Round(total*100) / 100
}
