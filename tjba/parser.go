package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"

	"github.com/dadosjusbr/coletores"
	"github.com/dadosjusbr/coletores/status"
)

func parse(filePath string) ([]coletores.Employee, error) {
	tjbaEmployees, err := newTjbaEmployees(filePath)
	if err != nil {
		return nil, fmt.Errorf("error parsing employees: %q", err)
	}

	employees := fromTjbaEmployeeToEmployee(tjbaEmployees)
	return employees, nil
}

// newTjbaEmployees creates a tjbaEmployee from a JSON file
func newTjbaEmployees(filePath string) ([]tjbaEmployee, error) {
	jsonFile, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("error trying to open file at (%s) : %q", filePath, err)
	}
	defer jsonFile.Close()

	byteValue, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		return nil, fmt.Errorf("error trying to read file at (%s) to []byte : %q", filePath, err)
	}

	var employees []tjbaEmployee
	err = json.Unmarshal(byteValue, &employees)

	if err != nil {
		return nil, status.NewError(status.InvalidInput, errors.New("Error during JSON parsing"))
	}
	return employees, nil
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

// fromTjbaEmployeeToEmployee convert from TJ-BA employee to coletores.Employee
func fromTjbaEmployeeToEmployee(tjbaEmployee []tjbaEmployee) []coletores.Employee {
	var employees []coletores.Employee
	for i := range tjbaEmployee {
		employee := coletores.Employee{}
		employee.Reg = strconv.Itoa(tjbaEmployee[i].Reg)
		employee.Name = tjbaEmployee[i].Name
		employee.Role = tjbaEmployee[i].Role
		employee.Type = employeeType(tjbaEmployee[i].Type)
		employee.Workplace = tjbaEmployee[i].Workplace
		employee.Active = active(tjbaEmployee[i].Active)
		employee.Income = &coletores.IncomeDetails{
			Total: tjbaEmployee[i].IncomeTotal,
			Wage:  &tjbaEmployee[i].Wage,
			Perks: &coletores.Perks{Total: tjbaEmployee[i].PerksTotal},
			Other: &coletores.Funds{
				Total:            tjbaEmployee[i].FundsTotal,
				PersonalBenefits: &tjbaEmployee[i].PersonalBenefits,
				EventualBenefits: &tjbaEmployee[i].EventualBenefits,
				PositionOfTrust:  &tjbaEmployee[i].PositionOfTrust,
				Gratification:    &tjbaEmployee[i].Gratification,
				Daily:            &tjbaEmployee[i].Daily,
				OriginPosition:   &tjbaEmployee[i].OriginPosition,
			},
		}
		employee.Discounts = &coletores.Discount{
			Total:               tjbaEmployee[i].DiscountTotal,
			PrevContribution:    &tjbaEmployee[i].PrevContribution,
			CeilRetention:       &tjbaEmployee[i].CeilRetention,
			IncomeTax:           &tjbaEmployee[i].IncomeTax,
			OtherDiscountsTotal: &tjbaEmployee[i].OtherDiscountsTotal,
		}

		employees = append(employees, employee)
	}
	return employees
}
