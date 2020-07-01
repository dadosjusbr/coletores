package main

import (
	"bytes"
	"encoding/csv"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	"github.com/dadosjusbr/storage"
	"github.com/gocarina/gocsv"
)

// magister_bef_may.go parse all servants.pdf before may/2020.

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
	csvFinal := headersMag()
	for i, templ := range templateArea {
		//This cmd execute a tabula script(https://github.com/tabulapdf/tabula-java)
		//where tmpl is the template area, which corresponds to the coordinates (x1,2,y1,2) of
		//one or more columns in the table.
		cmdList := strings.Split(fmt.Sprintf(`java -jar tabula-1.0.3-jar-with-dependencies.jar -t -a %v -p all %v`, templ, filepath.Base(path)), " ")
		cmd := exec.Command(cmdList[0], cmdList[1:]...)
		var outb, errb bytes.Buffer
		cmd.Stdout = &outb
		cmd.Stderr = &errb
		cmd.Run()
		reader := csv.NewReader(&outb)
		reader.FieldsPerRecord = -1
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
		file, err := os.Create(fmt.Sprintf("%v.csv", i))
		if err != nil {
			logError("Error creating csv: %q", err)
			os.Exit(1)
		}
		defer file.Close()
		writer := gocsv.DefaultCSVWriter(file)
		defer writer.Flush()
		writer.WriteAll(rows)

		csvFinal = appendCSVColumns(csvFinal, rows)
	}
	file, err := os.Create(strings.Replace(filepath.Base(path), ".pdf", ".csv", 1))
	if err != nil {
		logError("Error creating csv: %q", err)
		os.Exit(1)
	}
	defer file.Close()
	writer := gocsv.DefaultCSVWriter(file)
	defer writer.Flush()
	writer.WriteAll(csvFinal)
	fileName := strings.Replace(filepath.Base(path), ".pdf", ".csv", 1)
	//TODO uses status lib to format errors.
	clientsFile, err := os.OpenFile(fileName, os.O_RDWR|os.O_CREATE, os.ModePerm)
	if err != nil {
		logError("Error oppening csv: %v, error: %v", fileName, err)
		os.Exit(1)
	}
	defer clientsFile.Close()
	mag := []magBefMay{}
	//TODO uses status lib to format errors.
	if err := gocsv.UnmarshalFile(clientsFile, &mag); err != nil { // Load Employees from file
		logError("Error Unmarshalling CSV to Magister before may csv: %v, error: ", fileName, err)
		os.Exit(1)
	}
	employees := toEmployeeMag(mag)
	return employees, nil
}

//setHeaders Set headers to CSV based on his pdf template.
func headersMag() [][]string {
	var csvFinal [][]string
	headers := []string{"name", "role", "workplace", "wage", "personalBenefits", "gratification",
		"perks", "eventualBenefits", "prevContribution", "incomeTax",
		"othersDisc", "ceilRetention", "totalDisc", "totalIncome", "netIncome", "daily"}
	return append(csvFinal, headers)
}

//toEmployee Receives a []servBefMay and transform it into a []storage.Employee
func toEmployeeMag(mag []magBefMay) []storage.Employee {
	var empSet []storage.Employee
	for i := range mag {
		empSet = append(empSet, storage.Employee{
			Name:      mag[i].Name,
			Role:      mag[i].Role,
			Type:      "magistrado",
			Workplace: mag[i].Workplace,
			Active:    employeeActive(mag[i].Role),
			Income:    employeeIncomeMag(mag[i]),
			Discounts: employeeDiscMag(mag[i]),
		})
	}
	return empSet
}

//employeeDiscountInfo receives a servantMay, create a storage.Discount, match fields and return.
func employeeDiscMag(emp magBefMay) *storage.Discount {
	var d storage.Discount
	d.CeilRetention = emp.CeilRetention
	d.IncomeTax = emp.IncomeTax
	d.PrevContribution = emp.PrevContribution
	d.Total = *emp.TotalDisc
	d.Others = make(map[string]float64)
	d.Others["Descontos Diversos"] = *emp.OthersDisc
	return &d
}

//employeeIncome receives a servantMay, create a storage.IncomeDetails, match fields and return.
func employeeIncomeMag(emp magBefMay) *storage.IncomeDetails {
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
