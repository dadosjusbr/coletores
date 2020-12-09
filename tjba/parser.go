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

// employeeType returns employee.Type
func employeeType(value string) string {
	// possible values from the source: S (servidor), D (desembargador) and J (juiz)
	if value == "S" {
		return "servidor"
	} else if value == "D" || value == "J" {
		return "membro"
	}
	return ""
}

// active returns Employee.Active
func active(value string) bool {
	// possible values from the source: A (ativo) or I (inativo)
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

		var employee = coletores.Employee{}
		employee.Reg = strconv.Itoa(tjbaEmployee[i].Reg)
		employee.Name = tjbaEmployee[i].Name
		employee.Role = tjbaEmployee[i].Role
		employee.Type = employeeType(tjbaEmployee[i].Type)
		employee.Workplace = tjbaEmployee[i].Workplace
		employee.Active = active(tjbaEmployee[i].Active)
		employee.Income = &income
		employee.Discounts = &discounts

		employees = append(employees, employee)
	}
	return employees
}
