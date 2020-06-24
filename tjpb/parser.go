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

var (
	template = map[string]string{
		"name":   " 88.928,16.838,557.246,102.083",
		"func":   "88.928,97.873,546.722,213.637",
		"lot":    "91.575,213.84,574.695,369.27",
		"number": "93.137,358.868,557.246,815.61",
	}
	templateArray = []string{"88.928,16.838,557.246,102.083",
		"88.928,97.873,546.722,213.637",
		"89.98,207.323,557.246,360.973",
		"93.137,358.868,557.246,815.61"}
)

func parser(files []string) ([]storage.Employee, error) {
	var csvFiles [][]byte
	var csvFinal [][][]string
	for _, f := range files {
		for _, templ := range templateArray {
			//output := fmt.Sprintf(`%v.csv`, i)
			cmdList := strings.Split(fmt.Sprintf(`java -jar tabula-1.0.3-jar-with-dependencies.jar -a %v -p all %v`, templ, filepath.Base(f)), " ")
			cmd := exec.Command(cmdList[0], cmdList[1:]...)
			var outb, errb bytes.Buffer
			cmd.Stdout = &outb
			cmd.Stderr = &errb
			cmd.Run()
			csvFiles = append(csvFiles, outb.Bytes())
			reader := csv.NewReader(&outb)
			rows, err := reader.ReadAll()
			if err != nil {
				os.Exit(1)
			}
			csvFinal = append(csvFinal, rows)
		}
		for i := range csvFinal[3] {
			csvFinal[0][i] = append(csvFinal[0][i], csvFinal[1][i][0])
			csvFinal[0][i] = append(csvFinal[0][i], csvFinal[2][i][0])
			//csvFinal[0][i] = append(csvFinal[0][i], csvFinal[3][i]...)
			for j := range csvFinal[3][i] {
				reg := regexp.MustCompile(`[a-zA-Z_ ]`)
				res := reg.ReplaceAllString(csvFinal[3][i][j], "${1}")
				csvFinal[0][i] = append(csvFinal[0][i], res)
			}
		}
		csvFinal[0] = csvFinal[0][:len(csvFinal[3])]
		file, _ := os.Create("result.csv")
		defer file.Close()
		writer := csv.NewWriter(file)
		defer writer.Flush()
		writer.WriteAll(csvFinal[0])
	}
	return []storage.Employee{}, nil
}
