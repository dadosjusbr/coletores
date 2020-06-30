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

type servant struct { // Our example struct, you can use "-" to ignore a field
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

func parserServer(path string) ([]storage.Employee, error) {
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
		if i == 2 {
			rows = treatDoubleLines(rows)
		}
		if i == 3 {
			rows = fixNumberColumns(rows)
		}
		fmt.Println(rows)
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
	clientsFile, err := os.OpenFile(strings.Replace(filepath.Base(path), ".pdf", ".csv", 1), os.O_RDWR|os.O_CREATE, os.ModePerm)
	if err != nil {
		logError("Error oppening csv: %v", err)
		os.Exit(1)
	}
	defer clientsFile.Close()
	serv := []servant{}
	if err := gocsv.UnmarshalFile(clientsFile, &serv); err != nil { // Load Employees from file
		logError("Error Unmarshalling CSV to servantMay csv: %v", err)
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
func toEmployee(serv []servant) []storage.Employee {
	var empSet []storage.Employee
	for i := range serv {
		var emp = storage.Employee{}
		emp.Name = serv[i].Name
		emp.Role = serv[i].Role
		emp.Type = "servidor"
		emp.Workplace = serv[i].Workplace
		emp.Active = employeeActive(serv[i].Role)
		emp.Income = employeeIncome(serv[i])
		emp.Discounts = employeeDisc(serv[i])
		empSet = append(empSet, emp)
	}
	return empSet
}

//employeeDiscountInfo receives a servantMay, create a storage.Discount, match fields and return.
func employeeDisc(emp servant) *storage.Discount {
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
func employeeIncome(emp servant) *storage.IncomeDetails {
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
