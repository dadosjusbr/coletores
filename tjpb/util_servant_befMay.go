package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"

	"github.com/dadosjusbr/storage"
	"github.com/gocarina/gocsv"
)

//csvToStructServBefMay parse csv into []servBefMay struct.
func csvToStructServBefMay(fileName string) ([]servBefMay, error) {
	//TODO uses status lib to format errors.
	servEmps, err := os.OpenFile(fileName, os.O_RDWR|os.O_CREATE, os.ModePerm)
	if err != nil {
		return nil, fmt.Errorf("Error oppening csv: %v, error: %v", fileName, err)
	}
	defer servEmps.Close()
	servBefMay := []servBefMay{}
	//TODO uses status lib to format errors.
	if err := gocsv.UnmarshalFile(servEmps, &servBefMay); err != nil { // Load Employees from file
		return nil, fmt.Errorf("Error Unmarshalling CSV to servant before may csv: %v, error: %v", fileName, err)
	}
	return servBefMay, nil
}

//setHeaders Set headers to CSV based on his pdf template.
func headersServBefMay() [][]string {
	var csvFinal [][]string
	headers := []string{"name", "role", "workplace", "wage", "personalBenefits", "positionOfTrust",
		"perks", "eventualBenefits", "totalIncome", "prevContribution", "incomeTax",
		"othersDisc", "ceilRetention", "totalDisc", "incomeFinal", "daily"}
	return append(csvFinal, headers)
}

//toEmployee Receives a []servantMay and transform it into a []storage.Employee
func toEmployeeServBefMay(serv []servBefMay) []storage.Employee {
	var empSet []storage.Employee
	for i := range serv {
		empSet = append(empSet, storage.Employee{
			Name:      serv[i].Name,
			Role:      serv[i].Role,
			Type:      "servidor",
			Workplace: serv[i].Workplace,
			Active:    employeeActive(serv[i].Role),
			Income:    employeeIncomeServBefMay(serv[i]),
			Discounts: employeeDiscServBefMay(serv[i]),
		})
	}
	return empSet
}

//employeeDiscServBefMay receives a servBefMay, create a storage.Discount, match fields and return.
func employeeDiscServBefMay(emp servBefMay) *storage.Discount {
	var d storage.Discount
	d.CeilRetention = emp.CeilRetention
	d.IncomeTax = emp.IncomeTax
	d.PrevContribution = emp.PrevContribution
	d.Total = *emp.TotalDisc
	d.Others = make(map[string]float64)
	d.Others["Descontos Diversos"] = *emp.OthersDisc
	return &d
}

//employeeIncomeServBefMay receives a servBefMay, create a storage.IncomeDetails, match fields and return.
func employeeIncomeServBefMay(emp servBefMay) *storage.IncomeDetails {
	in := storage.IncomeDetails{}
	perks := storage.Perks{}
	other := storage.Funds{}
	in.Wage = emp.Wage
	perks.Total = *emp.Perks
	other.PositionOfTrust = emp.PositionOfTrust
	other.PersonalBenefits = emp.PersonalBenefits
	other.Daily = emp.Daily
	other.EventualBenefits = emp.EventualBenefits
	other.Total = *other.PositionOfTrust + *other.PersonalBenefits + *other.Daily + *other.EventualBenefits
	in.Perks = &perks
	in.Other = &other
	in.Total = *in.Wage + in.Other.Total + in.Perks.Total
	return &in
}

func setCSVReader(in io.Reader) gocsv.CSVReader {
	r := csv.NewReader(in)
	r.FieldsPerRecord = -1
	return r
}
