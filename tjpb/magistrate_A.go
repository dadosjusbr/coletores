package main

import (
	"bytes"
	"encoding/csv"
	"fmt"
	"os"
	"os/exec"
	"strings"

	"github.com/dadosjusbr/coletores"
)

// magistrate_A.go parse all magistrate.pdf from the following months:
// 2018: Fev, Apr, May, June, August, September, Octurbre, November, December
// 2019: Jan, Fev, Mar, Apr, May, June, August, September, November
// 2020: Apr

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

func parserMagA(path string) ([]coletores.Employee, error) {
	// We generate this template using release 1.2.1 of https://github.com/tabulapdf/tabula
	templateArea := []string{"105.781,36.839,583.639,136.831",
		"106.834,136.831,586.797,248.402",
		"105.781,247.349,569.956,587.323",
		"106.834,392.601,547.852,414.705",
		"106.834,435.756,565.746,803.096"}
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
		if err := cmd.Run(); err != nil {
			logError("Error executing java cmd: %v", err)
		}
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
