package main

import (
	"bytes"
	"fmt"
	"os"
	"os/exec"
	"strings"

	"github.com/dadosjusbr/coletores"
)

// servant_B.go parse all servants.pdf from the following months:
// 2018: Mar, July
// 2019: December.
// 2020: Jan, Fev

func parserServB(path string) ([]coletores.Employee, error) {
	// We generate this template using release 1.2.1 of https://github.com/tabulapdf/tabula
	templateArea := []string{"94.545,16.83,582.615,105.93",
		"94.545,102.96,578.655,215.82",
		"94.545,216.81,574.695,540.54",
		"93.555,369.27,569.745,389.07",
		"95.535,399.96,576.675,787.05"}
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
