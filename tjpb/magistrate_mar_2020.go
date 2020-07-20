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

// magistrate_bef_may.go parse all servants.pdf before may/2020.

func parserMagMar2020(path string) ([]storage.Employee, error) {
	// We generate this template using release 1.2.1 of https://github.com/tabulapdf/tabula
	templateArea := []string{"105.751,37.881,539.278,137.845",
		"104.699,135.74,541.383,246.226",
		"106.803,246.226,541.383,499.819",
		"107.856,388.28,540.33,416.691",
		"105.751,429.318,540.33,795.501"}
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
		fmt.Println(len(rows))
		fmt.Println(rows)
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
