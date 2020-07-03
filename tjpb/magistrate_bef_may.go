package main

import (
	"bytes"
	"encoding/csv"
	"fmt"
	"os"
	"os/exec"
	"strings"

	"github.com/dadosjusbr/storage"
	"github.com/gocarina/gocsv"
)

// magistrate_bef_may.go parse all servants.pdf before may/2020.

type magBefMay struct { // Our example struct, you can use "-" to ignore a field
	Name             string   `csv:"name"`
	Role             string   `csv:"role"`
	Workplace        string   `csv:"workplace"`
	Wage             *float64 `csv:"wage"`
	PersonalBenefits *float64 `csv:"personalBenefits"`
	Gratification    *float64 `csv:"gratification"`
	Perks            *float64 `csv:"perks"`
	EventualBenefits *float64 `csv:"eventualBenefits"`
	PrevContribution *float64 `csv:"prevContribution"`
	IncomeTax        *float64 `csv:"incomeTax"`
	OthersDisc       *float64 `csv:"othersDisc"`
	CeilRetention    *float64 `csv:"ceilRetention"`
	TotalDisc        *float64 `csv:"totalDisc"`
	TotalIncome      *float64 `csv:"totalIncome"`
	IncomeFinal      *float64 `csv:"netIncome"`
	Daily            *float64 `csv:"daily"`
}

func parserMagBefMay(path string) ([]storage.Employee, error) {
	// We generate this template using release 1.2.1 of https://github.com/tabulapdf/tabula
	templateArea := []string{"101.475,35.64,557.865,130.68",
		"100.485,129.69,564.795,234.63",
		"104.445,231.66,564.795,745.473",
		"102.465,365.31,554.895,397.98",
		"102.465,404.91,554.895,747.45"}
	csvFinal := headersMagBefMay()
	for i, templ := range templateArea {
		//This cmd execute a tabula script(https://github.com/tabulapdf/tabula-java)
		//where tmpl is the template area, which corresponds to the coordinates (x1,2,y1,2) of
		//one or more columns in the table.
		cmdList := strings.Split(fmt.Sprintf(`java -jar tabula-1.0.3-jar-with-dependencies.jar -t -a %v -p all %v`, templ, path), " ")
		cmd := exec.Command(cmdList[0], cmdList[1:]...)
		var outb, errb bytes.Buffer
		cmd.Stdout = &outb
		cmd.Stderr = &errb
		cmd.Run()
		reader := csv.NewReader(&outb)
		// Allow records to have a variable number of fields
		// This template isnt simple to parse into records, so this line is to receive
		// records the way it was possible and treat after.
		reader.FieldsPerRecord = -1
		// Reads csv from bytes buffer
		rows, err := reader.ReadAll()
		if err != nil {
			logError("Error reading rows from stdout: %v", err)
			os.Exit(1)
		}
		// When the templ refers to worksplace Column, treating double lines is necessary
		if i == 2 {
			// Pass rows and a knew invariable and non-empty column pos.
			rows = treatDoubleLines(rows, 3)
		}
		// When the templ refers to column of numbers, treating cels to format numbers and
		// remove characters.
		if i == 3 || i == 4 {
			rows = fixNumberColumns(rows)
		}
		csvFinal = appendCSVColumns(csvFinal, rows)
	}

	//TODO uses lib to format errors
	fileName := strings.Replace(path, ".pdf", ".csv", 1)
	if err := createCsv(fileName, csvFinal); err != nil {
		logError("Error creating csv: %v, error : %v", fileName, err)
		os.Exit(1)
	}
	magBefMay, err := csvToMagBefMay(fileName)
	if err != nil {
		logError("Error creating csv: %v, error : %v", fileName, err)
		os.Exit(1)
	}
	employees := toEmployeeMagistrateBeforeMay(magBefMay)
	return employees, nil
}

//csvToMagBefMay parse csv into []magBefMay struct.
func csvToMagBefMay(fileName string) ([]magBefMay, error) {
	//TODO uses status lib to format errors.
	magistrateEmps, err := os.OpenFile(fileName, os.O_RDWR|os.O_CREATE, os.ModePerm)
	if err != nil {
		return nil, fmt.Errorf("Error oppening csv: %v, error: %v", fileName, err)
	}
	fmt.Println(fileName, "CSV TO MAG BEF MAY")
	defer magistrateEmps.Close()
	/*
		reader := csv.NewReader(magistrateEmps)
		teste, _ := reader.ReadAll()
		fmt.Println(teste)
	*/
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

//toEmployee Receives a []magBefMay and transform it into a []storage.Employee
func toEmployeeMagistrateBeforeMay(mag []magBefMay) []storage.Employee {
	var empSet []storage.Employee
	for i := range mag {
		empSet = append(empSet, storage.Employee{
			Name:      mag[i].Name,
			Role:      mag[i].Role,
			Type:      "magistrado",
			Workplace: mag[i].Workplace,
			Active:    employeeActive(mag[i].Role),
			Income:    employeeIncomeMagistrateBeforeMay(mag[i]),
			Discounts: employeeDiscMagistrateBeforeMay(mag[i]),
		})
	}
	return empSet
}

//employeeDiscountInfo receives a magBefMay, create a storage.Discount, match fields and return.
func employeeDiscMagistrateBeforeMay(emp magBefMay) *storage.Discount {
	var d storage.Discount
	d.CeilRetention = emp.CeilRetention
	d.IncomeTax = emp.IncomeTax
	d.PrevContribution = emp.PrevContribution
	d.Total = *emp.TotalDisc
	d.Others = make(map[string]float64)
	d.Others["Descontos Diversos"] = *emp.OthersDisc
	return &d
}

//employeeIncome receives a magBefMay, create a storage.IncomeDetails, match fields and return.
func employeeIncomeMagistrateBeforeMay(emp magBefMay) *storage.IncomeDetails {
	in := storage.IncomeDetails{}
	perks := storage.Perks{}
	other := storage.Funds{}
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
