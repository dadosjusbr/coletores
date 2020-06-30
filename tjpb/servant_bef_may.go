package main

import (
	"bytes"
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	"github.com/dadosjusbr/storage"
	"github.com/gocarina/gocsv"
)

// servang_bef_may.go parse all servants.pdf before may/2020.

type servBefMay struct { // Our example struct, you can use "-" to ignore a field
	Name             string   `csv:"name"`
	Role             string   `csv:"role"`
	Workplace        string   `csv:"workplace"`
	Wage             *float64 `csv:"wage"`
	PersonalBenefits *float64 `csv:"personalBenefits"`
	PositionOfTrust  *float64 `csv:"positionOfTrust"`
	Perks            *float64 `csv:"perks"`
	EventualBenefits *float64 `csv:"eventualBenefits"`
	TotalIncome      *float64 `csv:"totalIncome"`
	PrevContribution *float64 `csv:"prevContribution"`
	IncomeTax        *float64 `csv:"incomeTax"`
	OthersDisc       *float64 `csv:"othersDisc"`
	CeilRetention    *float64 `csv:"ceilRetention"`
	TotalDisc        *float64 `csv:"totalDisc"`
	IncomeFinal      *float64 `csv:"incomeFinal"`
	Daily            *float64 `csv:"daily"`
}

func parserServBefMay(path string) ([]storage.Employee, error) {
	// We generate this template using release 1.2.1 of https://github.com/tabulapdf/tabula
	templateArea := []string{"94.19,13.681,545.669,109.45",
		"94.19,106.292,545.669,228.371",
		"96.295,226.266,544.617,499.89",
		"94.19,387.283,545.669,814.558"}
	csvFinal := headers()
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
		reader := setCSVReader(&outb)
		rows, err := reader.ReadAll()
		if err != nil {
			logError("Error reading rows from stdout: %v", err)
			os.Exit(1)
		}
		// When the templ refers to worksplace Column, treating double lines is necessary
		if i == 2 {
			rows = treatDoubleLines(rows)
		}
		// When the templ refers to column of numbers, treating cels to format numbers and
		// remove characters.
		if i == 3 {
			rows = fixNumberColumns(rows)
		}
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
	serv := []servBefMay{}
	//TODO uses status lib to format errors.
	if err := gocsv.UnmarshalFile(clientsFile, &serv); err != nil { // Load Employees from file
		logError("Error Unmarshalling CSV to servantBefMay csv: %v, error: ", fileName, err)
		os.Exit(1)
	}
	employees := toEmployee(serv)
	return employees, nil
}

//setHeaders Set headers to CSV based on his pdf template.
func headers() [][]string {
	var csvFinal [][]string
	headers := []string{"name", "role", "workplace", "wage", "personalBenefits", "positionOfTrust",
		"perks", "eventualBenefits", "totalIncome", "prevContribution", "incomeTax",
		"othersDisc", "ceilRetention", "totalDisc", "incomeFinal", "daily"}
	return append(csvFinal, headers)
}

//toEmployee Receives a []servantMay and transform it into a []storage.Employee
func toEmployee(serv []servBefMay) []storage.Employee {
	var empSet []storage.Employee
	for i := range serv {
		empSet = append(empSet, storage.Employee{
			Name:      serv[i].Name,
			Role:      serv[i].Role,
			Type:      "servidor",
			Workplace: serv[i].Workplace,
			Active:    employeeActive(serv[i].Role),
			Income:    employeeIncome(serv[i]),
			Discounts: employeeDisc(serv[i]),
		})
	}
	return empSet
}

//employeeDiscountInfo receives a servantMay, create a storage.Discount, match fields and return.
func employeeDisc(emp servBefMay) *storage.Discount {
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
func employeeIncome(emp servBefMay) *storage.IncomeDetails {
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
