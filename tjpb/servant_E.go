package main

import (
	"bytes"
	"fmt"
	"os"
	"os/exec"
	"strings"

	"github.com/dadosjusbr/coletores"
	"github.com/gocarina/gocsv"
)

// servant_E.go parse all servants.pdf from the following months:
// 2020: May
// Will be used as default for the next months.

type servantMay struct { // Our example struct, you can use "-" to ignore a field
	Name             string   `csv:"name"`
	Role             string   `csv:"role"`
	Workplace        string   `csv:"workplace"`
	Wage             *float64 `csv:"wage"`
	PersonalBenefits *float64 `csv:"personalBenefits"`
	PositionOfTrust  *float64 `csv:"positionOfTrust"`
	Perks            *float64 `csv:"perks"`
	EventualBenefits *float64 `csv:"eventualBenefits"`
	Gratification    *float64 `csv:"gratification"`
	TotalIncome      *float64 `csv:"totalIncome"`
	PrevContribution *float64 `csv:"prevContribution"`
	IncomeTax        *float64 `csv:"incomeTax"`
	OthersDisc       *float64 `csv:"othersDisc"`
	CeilRetention    *float64 `csv:"ceilRetention"`
	TotalDisc        *float64 `csv:"totalDisc"`
	IncomeFinal      *float64 `csv:"incomeFinal"`
	OriginPosition   *float64 `csv:"originPosition"`
	Daily            *float64 `csv:"daily"`
}

func parserServerE(path string) ([]coletores.Employee, error) {
	templateArea := []string{"92.085,16.838,559.351,102.083",
		"93.137,102.083,541.46,211.532",
		"94.19,209.428,547.774,824.029",
		"94.19,360.973,548.827,818.767"}
	var csvByte [][]byte
	csvFinal := headersServMay()
	for i, templ := range templateArea {
		//This cmd execute a tabula script(https://github.com/tabulapdf/tabula-java)
		//where tmpl is the template area, which corresponds to the coordinates (x1,2,y1,2) of
		//one or more columns in the table.
		cmdList := strings.Split(fmt.Sprintf(`java -jar tabula-1.0.3-jar-with-dependencies.jar -t -a %v -p all %v`, templ, path), " ")
		cmd := exec.Command(cmdList[0], cmdList[1:]...)
		var outb, errb bytes.Buffer
		cmd.Stdout = &outb
		cmd.Stderr = &errb
		if err := cmd.Run(); err != nil {
			logError("Error executing java cmd: %v", err)
		}
		csvByte = append(csvByte, outb.Bytes())
		reader := gocsv.DefaultCSVReader(&outb)
		rows, err := reader.ReadAll()
		if err != nil {
			logError("Error reading rows from stdout: %v", err)
			os.Exit(1)
		}
		if i == 2 {
			// Pass rows and a knew invariable and non-empty column pos.
			rows = treatDoubleLines(rows, 2)
		}
		if i == 3 {
			rows = fixNumberColumns(rows)
		}
		csvFinal = appendCSVColumns(csvFinal, rows)
	}
	fileName := strings.Replace(path, ".pdf", ".csv", 1)
	if err := createCsv(fileName, csvFinal); err != nil {
		logError("Error creating csv: %v, error : %v", fileName, err)
		os.Exit(1)
	}
	servMay, err := csvToStructServMay(fileName)
	if err != nil {
		logError("Error creating csv: %v, error : %v", fileName, err)
		os.Exit(1)
	}
	employees := toEmployeeServMay(servMay)
	return employees, nil
}

//csvToStructServMay parse csv into []servantMay struct.
func csvToStructServMay(fileName string) ([]servantMay, error) {
	//TODO uses status lib to format errors.
	servEmps, err := os.OpenFile(fileName, os.O_RDWR|os.O_CREATE, os.ModePerm)
	if err != nil {
		return nil, fmt.Errorf("Error oppening csv: %v, error: %v", fileName, err)
	}
	defer servEmps.Close()
	servantMay := []servantMay{}
	//TODO uses status lib to format errors.
	if err := gocsv.UnmarshalFile(servEmps, &servantMay); err != nil { // Load Employees from file
		return nil, fmt.Errorf("Error Unmarshalling CSV to servant may csv: %v, error: %v", fileName, err)
	}
	return servantMay, nil
}

//setHeaders Set headers to CSV based on his pdf template.
func headersServMay() [][]string {
	var csvFinal [][]string
	headers := []string{"name", "role", "workplace", "wage", "personalBenefits", "positionOfTrust",
		"perks", "eventualBenefits", "gratification", "totalIncome", "prevContribution", "incomeTax",
		"othersDisc", "ceilRetention", "totalDisc", "incomeFinal", "originPosition", "daily"}
	return append(csvFinal, headers)
}

//toEmployee Receives a []servantMay and transform it into a []coletores.Employee
func toEmployeeServMay(servMay []servantMay) []coletores.Employee {
	var empSet []coletores.Employee
	for i := range servMay {
		var emp = coletores.Employee{}
		emp.Name = servMay[i].Name
		emp.Role = servMay[i].Role
		emp.Type = "servidor"
		emp.Workplace = servMay[i].Workplace
		emp.Active = employeeActive(servMay[i].Role)
		emp.Income = employeeIncomeServMay(servMay[i])
		emp.Discounts = employeeDiscServMay(servMay[i])
		empSet = append(empSet, emp)
	}
	return empSet
}

//employeeDiscountInfo receives a servantMay, create a coletores.Discount, match fields and return.
func employeeDiscServMay(emp servantMay) *coletores.Discount {
	var d coletores.Discount
	d.CeilRetention = emp.CeilRetention
	d.IncomeTax = emp.IncomeTax
	d.PrevContribution = emp.PrevContribution
	d.Total = *emp.TotalDisc
	d.Others = make(map[string]float64)
	d.Others["Descontos Diversos"] = *emp.OthersDisc
	return &d
}

//employeeIncome receives a servantMay, create a coletores.IncomeDetails, match fields and return.
func employeeIncomeServMay(emp servantMay) *coletores.IncomeDetails {
	in := coletores.IncomeDetails{}
	perks := coletores.Perks{}
	other := coletores.Funds{}
	in.Wage = emp.Wage
	perks.Total = *emp.Perks
	other.PositionOfTrust = emp.PositionOfTrust
	other.PersonalBenefits = emp.PersonalBenefits
	other.Gratification = emp.Gratification
	other.Daily = emp.Daily
	other.EventualBenefits = emp.EventualBenefits
	other.OriginPosition = emp.OriginPosition
	other.Total = *other.PositionOfTrust + *other.PersonalBenefits + *other.Gratification + *other.Daily + *other.EventualBenefits + *other.OriginPosition
	in.Perks = &perks
	in.Other = &other
	in.Total = *in.Wage + in.Other.Total + in.Perks.Total
	return &in
}
