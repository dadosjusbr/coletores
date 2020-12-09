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
		var perks = coletores.Perks{Total: tjbaEmployee[i].PerksTotal}

		var funds = coletores.Funds{
			Total:            tjbaEmployee[i].FundsTotal,
			PersonalBenefits: &tjbaEmployee[i].PersonalBenefits,
			EventualBenefits: &tjbaEmployee[i].EventualBenefits,
			PositionOfTrust:  &tjbaEmployee[i].PositionOfTrust,
			Gratification:    &tjbaEmployee[i].Gratification,
			Daily:            &tjbaEmployee[i].Daily,
			OriginPosition:   &tjbaEmployee[i].OriginPosition,
		}

		var income = coletores.IncomeDetails{
			Total: tjbaEmployee[i].IncomeTotal,
			Wage:  &tjbaEmployee[i].Wage,
			Perks: &perks,
			Other: &funds,
		}

		var discounts = coletores.Discount{
			Total:               tjbaEmployee[i].DiscountTotal,
			PrevContribution:    &tjbaEmployee[i].PrevContribution,
			CeilRetention:       &tjbaEmployee[i].CeilRetention,
			IncomeTax:           &tjbaEmployee[i].IncomeTax,
			OtherDiscountsTotal: &tjbaEmployee[i].OtherDiscountsTotal,
		}

		var emp = coletores.Employee{}
		emp.Reg = strconv.Itoa(tjbaEmployee[i].Reg)
		emp.Name = tjbaEmployee[i].Name
		emp.Role = tjbaEmployee[i].Role
		emp.Type = employeeType(tjbaEmployee[i].Type)
		emp.Workplace = tjbaEmployee[i].Workplace
		emp.Active = active(tjbaEmployee[i].Active)
		emp.Income = &income
		emp.Discounts = &discounts

		employees = append(employees, emp)
	}
	return employees
}
