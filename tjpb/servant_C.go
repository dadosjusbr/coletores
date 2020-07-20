package main

import (
	"bytes"
	"fmt"
	"os"
	"os/exec"
	"strings"

	"github.com/dadosjusbr/storage"
)

// servant_C.go parse all servants.pdf from the following months:
// 2018: Jan

func parserServC(path string) ([]storage.Employee, error) {
	// We generate this template using release 1.2.1 of https://github.com/tabulapdf/tabula
	templateArea := []string{"242.423,40.615,1483.731,261.462",
		"237.346,261.462,1514.193,548.308",
		"239.885,543.231,1483.731,1436.77",
		"242.423,931.616,1465.962,979.847",
		"244.962,1002.693,1471.039,1969.847"}
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
			rows = treatDoubleLines(rows, 4)
		}
		// When the templ refers to column of numbers, treating cels to format numbers and
		// remove characters.
		if i == 3 || i == 4 {
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
