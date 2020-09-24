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

// magistrate_C.go parse all magistrate.pdf from the following months:
// 2018: Jan

func parserMagC(path string) ([]coletores.Employee, error) {
	// We generate this template using release 1.2.1 of https://github.com/tabulapdf/tabula
	templateArea := []string{"247.5,89.342,1396.868,311.488",
		"247.5,311.488,1428.258,560.196",
		"247.5,557.781,1396.868,847.538",
		"249.915,876.513,1392.038,932.05",
		"247.5,910.318,1377.551,1820.637"}
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

		// When the templ refers to column of numbers, treating cels to format numbers and
		// remove characters.
		if i == 3 {
			rows = fixNumberColumns(rows)
		}
		if i == 4 {
			// Tabula exports a empty first row of each page.
			for i := range rows {
				rows[i] = rows[i][1:]
			}
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
