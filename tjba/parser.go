package main

import (
	"encoding/json"
	"strconv"

	"github.com/dadosjusbr/coletores"
)

// newtjbaEmployee creates a tjbaEmployee from a map[string]interface{}
func newTjbaEmployees(payload string) ([]tjbaEmployee, error) {
	var employees []tjbaEmployee
	err := json.Unmarshal([]byte(payload), &employees)
	return employees, err
}

// employeeType returns employee.Type based in category string.
func employeeType(value string) string {
	// possible values from the source: S, D and J
	if value == "S" {
		return "servidor"
	} else if value == "D" || value == "J" {
		return "membro"
	}
	return ""
}

// active returns Employee.Active based in category string.
func active(value string) bool {
	// possible values from the source: A or I
	return value == "A"
}

// FromTjbaEmployeeToEmployee convert from TJ-BA employee to coletores.Employee
func FromTjbaEmployeeToEmployee(tjbaEmployee []tjbaEmployee) []coletores.Employee {
	var employees []coletores.Employee
	for i := range tjbaEmployee {
		var perks = coletores.Perks{Total: tjbaEmployee[i].PerksValue}

		var income = coletores.IncomeDetails{}
		income.Total = tjbaEmployee[i].CreditTotal
		income.Wage = &tjbaEmployee[i].Wage
		income.Perks = &perks

		var discounts = coletores.Discount{
			Total:               tjbaEmployee[i].DebtTotal,
			PrevContribution:    &tjbaEmployee[i].PrevContribution,
			CeilRetention:       &tjbaEmployee[i].RetantionValue,
			IncomeTax:           &tjbaEmployee[i].IncomeTax,
			OtherDiscountsTotal: &tjbaEmployee[i].Sundry,
		}

		var emp = coletores.Employee{}
		emp.Reg = strconv.Itoa(tjbaEmployee[i].Reg)
		emp.Name = tjbaEmployee[i].Name
		emp.Role = tjbaEmployee[i].Role
		emp.Type = employeeType(tjbaEmployee[i].EmployeeType)
		emp.Workplace = tjbaEmployee[i].Workplace
		emp.Active = active(tjbaEmployee[i].Status)
		emp.Income = &income
		emp.Discounts = &discounts

		employees = append(employees, emp)
	}
	return employees
}
