package main

import (
	"bytes"
	"encoding/csv"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/dadosjusbr/storage"
)

func parserServerMay(path string) ([]storage.Employee, error) {
	templateArea := []string{"88.928,16.838,557.246,102.083",
		"88.928,97.873,546.722,213.637",
		"89.98,207.323,557.246,360.973",
		"93.137,358.868,557.246,815.61"}
	var csvByte [][]byte
	var csvFinal [][]string
	for _, templ := range templateArea {
		cmdList := strings.Split(fmt.Sprintf(`java -jar tabula-1.0.3-jar-with-dependencies.jar -a %v -p all %v`, templ, filepath.Base(path)), " ")
		cmd := exec.Command(cmdList[0], cmdList[1:]...)
		var outb, errb bytes.Buffer
		cmd.Stdout = &outb
		cmd.Stderr = &errb
		cmd.Run()
		csvByte = append(csvByte, outb.Bytes())
		reader := csv.NewReader(&outb)
		rows, err := reader.ReadAll()
		if err != nil {
			//TODO CHECK ERROR
			os.Exit(1)
		}
		if len(rows[0]) > 1 {
			rows = fixNumberColumns(rows)
		}
		csvFinal = appendCSVColumns(csvFinal, rows)
	}
	file, err := os.Create(strings.Replace(filepath.Base(path), ".pdf", ".csv", 1))
	if err != nil {
		logError("Error creating csv: %q", err)
	}
	defer file.Close()
	writer := csv.NewWriter(file)
	defer writer.Flush()
	writer.WriteAll(csvFinal)
	return []storage.Employee{}, nil
}

//TODO UNIT TEST
//appendCSVColumns receives a base csv and append columns of a new csv to the right.
func appendCSVColumns(baseCSV, newCols [][]string) [][]string {
	if len(baseCSV) == 0 {
		baseCSV = newCols
	} else {
		for i := 0; i < len(newCols); i++ {
			var newElement []string
			newElement = append(newElement, newCols[i]...)
			baseCSV[i] = append(baseCSV[i], newElement...)
		}
	}
	return baseCSV
}

//TODO Unit Test
//fixNumberColumns fix and formats columns that should only contain numbers.
func fixNumberColumns(rows [][]string) [][]string {
	reg := regexp.MustCompile(`[a-zA-Z_  /]`)
	for i := range rows {
		for j := range rows[i] {
			rows[i][j] = reg.ReplaceAllString(rows[i][j], "${1}")
		}
	}
	return rows
}
