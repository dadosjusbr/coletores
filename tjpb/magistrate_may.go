package main

import (
	"bytes"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	"github.com/dadosjusbr/storage"
	"github.com/gocarina/gocsv"
)

// magistrate_may.go parse all magistrate.pdf before may/2020.

type magMay struct { // Our example struct, you can use "-" to ignore a field
	Name             string   `csv:"name"`
	Role             string   `csv:"role"`
	Workplace        string   `csv:"workplace"`
	Wage             *float64 `csv:"wage"`
	PersonalBenefits *float64 `csv:"personalBenefits"`
	Subsidy          *float64 `csv:"subsidy"`
	Perks            *float64 `csv:"perks"`
	EventualBenefits *float64 `csv:"eventualBenefits"`
	Gratification    *float64 `csv:"gratification"`
	TotalIncome      *float64 `csv:"totalIncome"`
	PrevContribution *float64 `csv:"prevContribution"`
	IncomeTax        *float64 `csv:"incomeTax"`
	OthersDisc       *float64 `csv:"othersDisc"`
	CeilRetention    *float64 `csv:"ceilRetention"`
	TotalDisc        *float64 `csv:"totalDisc"`
	IncomeFinal      *float64 `csv:"netIncome"`
	OriginPosition   *float64 `csv:"originPosition"`
	Daily            *float64 `csv:"daily"`
}

func parserMagMay(path string) ([]storage.Employee, error) {
	templateArea := []string{"93.137,16.838,550.931,103.135",
		"94.19,99.978,544.617,211.532",
		"93.137,209.428,548.827,817.715",
		"94.19,368.34,545.669,827.186"}
	var csvByte [][]byte
	csvFinal := headersMagMay()
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
		csvByte = append(csvByte, outb.Bytes())
		reader := setCSVReader(&outb)
		rows, err := reader.ReadAll()
		if err != nil {
			// TODO uses status lib to deal with errors.
			logError("Error reading rows from stdout: %v", err)
			os.Exit(1)
		}
		if i == 2 {
			rows = treatDoubleLines(rows, 2)
		}
		if i == 3 {
			rows = fixNumberColumns(rows)
		}
		csvFinal = appendCSVColumns(csvFinal, rows)
	}
	fileName := strings.Replace(filepath.Base(path), ".pdf", ".csv", 1)
	//TODO output

	if err := createCsv(fileName, csvFinal); err != nil {
		logError("Error creating csv: %v, error: %v", fileName, err)
		os.Exit(1)
	}
	magMay, err := csvToMagMay(fileName)
	if err != nil {
		logError("Error parsing csv: %v, to struct.  error: %v", fileName, err)
		os.Exit(1)
	}
	employees := toEmployeeMagMay(magMay)
	return employees, nil
}

//csvToMagMay parse csv into []magMay struct.
func csvToMagMay(fileName string) ([]magMay, error) {
	magMay := []magMay{}
	empFile, err := os.OpenFile(fileName, os.O_RDWR|os.O_CREATE, os.ModePerm)
	if err != nil {
		return nil, fmt.Errorf("Error oppening csv: %v, error: %v", fileName, err)
	}
	defer empFile.Close()
	if err := gocsv.UnmarshalFile(empFile, &magMay); err != nil { // Load Employees from file
		return nil, fmt.Errorf("Error Unmarshalling json to magisterMay csv: %v, error: %v", fileName, err)
		os.Exit(1)
	}
	return magMay, nil
}

//setHeaders Set headers to CSV based on his pdf template.
func headersMagMay() [][]string {
	var csvFinal [][]string
	headers := []string{"name", "role", "workplace", "wage", "personalBenefits", "subsidy",
		"perks", "eventualBenefits", "gratification", "totalIncome", "prevContribution", "incomeTax",
		"othersDisc", "ceilRetention", "totalDisc", "netIncome", "originPosition", "daily"}
	return append(csvFinal, headers)
}

//toEmployee Receives a []servantMay and transform it into a []storage.Employee
func toEmployeeMagMay(magMay []magMay) []storage.Employee {
	var empSet []storage.Employee
	for i := range magMay {
		var emp = storage.Employee{}
		emp.Name = magMay[i].Name
		emp.Role = magMay[i].Role
		emp.Type = "magistrado"
		emp.Workplace = magMay[i].Workplace
		emp.Active = employeeActive(magMay[i].Role)
		emp.Income = employeeIncomeMagMay(magMay[i])
		emp.Discounts = employeeDiscMagMay(magMay[i])
		empSet = append(empSet, emp)
	}
	return empSet
}

//employeeDiscountInfo receives a magisterMay, create a storage.Discount, match fields and return.
func employeeDiscMagMay(emp magMay) *storage.Discount {
	var d storage.Discount
	d.CeilRetention = emp.CeilRetention
	d.IncomeTax = emp.IncomeTax
	d.PrevContribution = emp.PrevContribution
	d.Total = *emp.TotalDisc
	d.Others = make(map[string]float64)
	d.Others["Descontos Diversos"] = *emp.OthersDisc
	return &d
}

//employeeIncome receives a magisterMay, create a storage.IncomeDetails, match fields and return.
// Wage
func employeeIncomeMagMay(emp magMay) *storage.IncomeDetails {
	in := storage.IncomeDetails{}
	perks := storage.Perks{}
	other := storage.Funds{}
	sumWage := *emp.Wage + *emp.Subsidy
	in.Wage = &sumWage
	perks.Total = *emp.Perks
	other.PersonalBenefits = emp.PersonalBenefits
	other.Gratification = emp.Gratification
	other.Daily = emp.Daily
	other.EventualBenefits = emp.EventualBenefits
	other.OriginPosition = emp.OriginPosition
	other.Total = *other.PersonalBenefits + *other.Gratification + *other.Daily + *other.EventualBenefits + *other.OriginPosition
	in.Perks = &perks
	in.Other = &other
	in.Total = *in.Wage + in.Other.Total + in.Perks.Total
	return &in
}
