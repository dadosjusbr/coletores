package main

import (
	"bytes"
	"encoding/csv"
	"fmt"
	"os"
	"os/exec"
	"strings"

	"github.com/dadosjusbr/storage"
)

// magistrate_B.go parse all magistrate.pdf from the following months:
// 2018: Mar, July
// 2019: December.
// 2020: Jan, Fev

func parserMagB(path string) ([]storage.Employee, error) {
	// We generate this template using release 1.2.1 of https://github.com/tabulapdf/tabula
	templateArea := []string{"102.465,37.62,559.845,129.69",
		"103.455,128.7,563.805,234.63",
		"101.475,231.66,559.845,560.34",
		"103.455,368.28,558.855,390.06",
		"103.455,405.9,559.845,748.44"}
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
