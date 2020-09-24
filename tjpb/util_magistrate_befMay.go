package main

import (
	"fmt"
	"os"

	"github.com/dadosjusbr/coletores"
	"github.com/gocarina/gocsv"
)

//csvToMagBefMay parse csv into []magBefMay struct.
func csvToMagBefMay(fileName string) ([]magBefMay, error) {
	//TODO uses status lib to format errors.
	magistrateEmps, err := os.OpenFile(fileName, os.O_RDWR|os.O_CREATE, os.ModePerm)
	if err != nil {
		return nil, fmt.Errorf("Error oppening csv: %v, error: %v", fileName, err)
	}
	defer magistrateEmps.Close()

	magBefMay := []magBefMay{}
	//TODO uses status lib to format errors.
	if err := gocsv.UnmarshalFile(magistrateEmps, &magBefMay); err != nil { // Load Employees from file
		return nil, fmt.Errorf("Error Unmarshalling CSV to Magister before may csv: %v, error: %v", fileName, err)
	}
	return magBefMay, nil
}

//setHeaders Set headers to CSV based on his pdf template.
func headersMagBefMay() [][]string {
	var csvFinal [][]string
	headers := []string{"name", "role", "workplace", "wage", "personalBenefits", "gratification",
		"perks", "eventualBenefits", "prevContribution", "incomeTax",
		"othersDisc", "ceilRetention", "totalDisc", "totalIncome", "netIncome", "daily"}
	return append(csvFinal, headers)
}

//toEmployee Receives a []magBefMay and transform it into a []coletores.Employee
func toEmployeeMagistrateBeforeMay(mag []magBefMay) []coletores.Employee {
	var empSet []coletores.Employee
	for i := range mag {
		empSet = append(empSet, coletores.Employee{
			Name:      mag[i].Name,
			Role:      mag[i].Role,
			Type:      "membro",
			Workplace: mag[i].Workplace,
			Active:    employeeActive(mag[i].Role),
			Income:    employeeIncomeMagistrateBeforeMay(mag[i]),
			Discounts: employeeDiscMagistrateBeforeMay(mag[i]),
		})
	}
	return empSet
}

//employeeDiscountInfo receives a magBefMay, create a coletores.Discount, match fields and return.
func employeeDiscMagistrateBeforeMay(emp magBefMay) *coletores.Discount {
	var d coletores.Discount
	d.CeilRetention = emp.CeilRetention
	d.IncomeTax = emp.IncomeTax
	d.PrevContribution = emp.PrevContribution
	d.Total = *emp.TotalDisc
	d.Others = make(map[string]float64)
	d.Others["Descontos Diversos"] = *emp.OthersDisc
	return &d
}

//employeeIncome receives a magBefMay, create a coletores.IncomeDetails, match fields and return.
func employeeIncomeMagistrateBeforeMay(emp magBefMay) *coletores.IncomeDetails {
	in := coletores.IncomeDetails{}
	perks := coletores.Perks{}
	other := coletores.Funds{}
	in.Wage = emp.Wage
	perks.Total = *emp.Perks
	other.Gratification = emp.Gratification
	other.PersonalBenefits = emp.PersonalBenefits
	other.Daily = emp.Daily
	other.EventualBenefits = emp.EventualBenefits
	other.Total = *other.Gratification + *other.PersonalBenefits + *other.Daily + *other.EventualBenefits
	in.Perks = &perks
	in.Other = &other
	in.Total = *in.Wage + in.Other.Total + in.Perks.Total
	return &in
}
