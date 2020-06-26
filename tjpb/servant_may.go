package main

import (
	"bytes"
	"encoding/csv"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
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
		//This cmd execute a tabula script(https://github.com/tabulapdf/tabula-java)
		//where tmpl is the template area, which corresponds to the coordinates (x1,2,y1,2) of
		//one or more columns in the table.
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
