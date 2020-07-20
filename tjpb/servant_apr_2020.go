package main

import (
	"bytes"
	"fmt"
	"os"
	"os/exec"
	"strings"

	"github.com/dadosjusbr/storage"
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

func parserServApr2020(path string) ([]storage.Employee, error) {
	// We generate this template using release 1.2.1 of https://github.com/tabulapdf/tabula
	templateArea := []string{"94.19,13.681,545.669,109.45",
		"94.19,106.292,545.669,228.371",
		"96.295,226.266,544.617,499.89",
		"94.19,387.283,545.669,814.558"}
	csvFinal := headersServBefMay()
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
		reader := setCSVReader(&outb)
		rows, err := reader.ReadAll()
		if err != nil {
			logError("Error reading rows from stdout: %v", err)
			os.Exit(1)
		}
		// When the templ refers to worksplace Column, treating double lines is necessary
		if i == 2 {
			// Pass rows and a knew invariable and non-empty column pos.
			rows = treatDoubleLines(rows, 2)
		}
		// When the templ refers to column of numbers, treating cels to format numbers and
		// remove characters.
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
	//TODO uses status lib to format errors.
	servBefMay, err := csvToStructServBefMay(fileName)
	if err != nil {
		logError("Error parsing to servBefMay struct the csv: %v, error : %v", fileName, err)
		os.Exit(1)
	}
	employees := toEmployeeServBefMay(servBefMay)
	return employees, nil
}
