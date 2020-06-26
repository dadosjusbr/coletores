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
	templateArea := []string{"92.085,16.838,559.351,102.083",
		"93.137,102.083,541.46,211.532",
		"94.19,209.428,547.774,824.029",
		"94.19,360.973,548.827,818.767"}
	var csvByte [][]byte
	var csvFinal [][]string
	for i, templ := range templateArea {
		cmdList := strings.Split(fmt.Sprintf(`java -jar tabula-1.0.3-jar-with-dependencies.jar -t -a %v -p all %v`, templ, filepath.Base(path)), " ")
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
		if i == 2 {
			rows = treatDoubleLines(rows)
		}
		if i == 3 {
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
func appendCSVColumns(mountedCsv, csv [][]string) [][]string {
	if len(mountedCsv) == 0 {
		for i := range csv {
			if strings.Contains(csv[i][0], "Legenda das") {
				break
			}
			mountedCsv = append(mountedCsv, csv[i])
		}
	} else {
		for i := 0; i < len(mountedCsv); i++ {
			var newElement []string
			newElement = append(newElement, csv[i]...)
			mountedCsv[i] = append(mountedCsv[i], newElement...)
		}
	}
	return mountedCsv
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

//TODO Unit Test
//treatDoubleLines fix cels widh double lines based in other colunm without double line.
func treatDoubleLines(rows [][]string) [][]string {
	reg := regexp.MustCompile(`(\d+)( *[\.,]( *\d*( *\d))| +)+`)
	var fixedCsv [][]string
	for i := range rows {
		rows[i][0] = reg.ReplaceAllString(rows[i][0], "")
		fmt.Println(rows[i][0])
		rowFixed := []string{}
		if strings.Contains(rows[i][0], "ras desta natureza") {
			return fixedCsv
		}
		fmt.Println(i)
		if rows[i][2] == "" {
			rows[i+1][0] = rows[i][0] + rows[i+1][0]
			continue
		}
		fmt.Println(i)
		rowFixed = append(rowFixed, rows[i][0])
		fixedCsv = append(fixedCsv, rowFixed)
	}
	return fixedCsv
}
