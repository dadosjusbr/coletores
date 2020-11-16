package main

import (
	"encoding/json"
	"fmt"
	"math"
	"strings"

	"github.com/dadosjusbr/coletores"
)

// parse takes a json filePath and retrieve the array of employees from it.
func parse(filePath string) ([]coletores.Employee, error) {
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
func parseEmployees(m map[string]interface{}) ([]coletores.Employee, error) {
	var employees []coletores.Employee
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
func parseCategory(category map[string]interface{}) ([]coletores.Employee, error) {
	var employees []coletores.Employee
	catInfo, err := catInfo(category)
	if err != nil {
		return nil, fmt.Errorf("error retrieving category info: %q", err)
	}

	empsMap, err := getSliceOfMaps(category, "listaAnexoviii")
	if err != nil {
		return nil, fmt.Errorf("couldn't find map for category: %q", err)
	}

	for i, emp := range empsMap {
		errKey, fieldErr := findNil(emp)
		if fieldErr {
			return nil, fmt.Errorf("error parsing employee at (%s: %d): missing key %q - %v", catInfo, i, errKey, emp)
		}

		trt13Emp, err := newTRT13Employee(emp)
		if err != nil {
			return nil, fmt.Errorf("error creating trt13Employee(%s: %d): %q", catInfo, i, err)
		}
		newEmp := newEmployee(trt13Emp, catInfo)
		employees = append(employees, newEmp)
	}
	return employees, nil
}

// catInfo retrieves category info from a category map.
func catInfo(category map[string]interface{}) (string, error) {
	cat, ok := category["rotuloCabecalho"]
	if !ok || cat == nil {
		return "", fmt.Errorf("couldn't find string for role")
	}
	catInfo, ok := cat.(string)
	if !ok {
		return "", fmt.Errorf("retrieved rotuloCabecalho is not a string")
	}
	return catInfo, nil
}

// newTRT13Employee creates a trt13Employee from a map[string]interface{}
func newTRT13Employee(emp map[string]interface{}) (trt13Employee, error) {
	var e trt13Employee
	empJSON, err := json.Marshal(emp)
	if err != nil {
		return e, fmt.Errorf("error marshaling map: %q", err)
	}
	err = json.Unmarshal(empJSON, &e)
	if err != nil {
		return e, fmt.Errorf("error unmarshaling trt13employee: %q", err)
	}
	return e, nil
}

// newEmployee creates an coletores.employee from a trt13Employee
func newEmployee(emp trt13Employee, catInfo string) coletores.Employee {
	e := coletores.Employee{}
	e.Reg = emp.Reg
	e.Name = emp.Name
	e.Role = emp.Role
	e.Workplace = emp.Workplace
	e.Active = active(catInfo)
	e.Type = employeeType(catInfo)
	e.Income = employeeIncome(emp)
	e.Discounts = employeeDiscounts(emp)
	return e
}

// employeeIncome creates an *coletores.IncomeDetails from a trt13Employee
func employeeIncome(emp trt13Employee) *coletores.IncomeDetails {
	in := coletores.IncomeDetails{Perks: &coletores.Perks{}}
	wage := emp.Income.Wage + emp.Income.Subsidio
	in.Wage = &wage
	in.Perks.Total = emp.Income.Perks
	in.Other = employeeFunds(emp)
	in.Total = totalIncome(in)
	return &in
}

// employeeFunds creates an *coletores.Funds from a trt13Employee
func employeeFunds(emp trt13Employee) *coletores.Funds {
	o := coletores.Funds{}
	o.PersonalBenefits = &emp.Income.PersonalBenefits
	o.EventualBenefits = &emp.Income.EventualBenefits
	o.Gratification = &emp.Income.Gratification
	o.Daily = &emp.Daily
	o.OriginPosition = &emp.OriginPosition
	o.Total = totalFunds(o)
	return &o
}

// employeeDiscounts creates an *coletores.Discount from a trt13Employee
func employeeDiscounts(emp trt13Employee) *coletores.Discount {
	d := coletores.Discount{}
	d.PrevContribution = &emp.Discount.PrevContribution
	d.CeilRetention = &emp.Discount.CeilRetantion
	d.IncomeTax = &emp.Discount.IncomeTax
	d.Others = map[string]float64{"other_discounts": emp.Discount.Sundry}
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
func totalDiscounts(d coletores.Discount) float64 {
	total := getFloat64Value(d.PrevContribution) + getFloat64Value(d.CeilRetention) + getFloat64Value(d.IncomeTax) + sumMapValues(d.Others)
	return math.Round(total*100) / 100
}

// totalFunds returns the sum of funds.
func totalFunds(f coletores.Funds) float64 {
	total := getFloat64Value(f.PersonalBenefits) + getFloat64Value(f.EventualBenefits) +
		getFloat64Value(f.PositionOfTrust) + getFloat64Value(f.Daily) + getFloat64Value(f.Gratification) + getFloat64Value(f.OriginPosition) + sumMapValues(f.Others)
	return math.Round(total*100) / 100
}

// grossIncome returns the sum of incomes.
func totalIncome(in coletores.IncomeDetails) float64 {
	total := getFloat64Value(in.Wage) + in.Perks.Total + in.Other.Total
	return math.Round(total*100) / 100
}
