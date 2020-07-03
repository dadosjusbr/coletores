package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/gocarina/gocsv"
)

// logError prints to Stderr
func logError(format string, args ...interface{}) {
	time := fmt.Sprintf("%s: ", time.Now().Format(time.RFC3339))
	fmt.Fprintf(os.Stderr, time+format+"\n", args...)
}

//TODO UNIT TEST
//appendCSVColumns receives a base csv and append columns of a new csv to the right.
func appendCSVColumns(baseCSV, newColumns [][]string) [][]string {
	if len(baseCSV) == 1 {
		for i := range newColumns {
			if strings.Contains(newColumns[i][0], "Legenda das") {
				break
			}
			baseCSV = append(baseCSV, newColumns[i])
		}
	} else {
		for i := 0; i < len(baseCSV)-1; i++ {
			var newElement []string
			newElement = append(newElement, newColumns[i]...)
			baseCSV[i+1] = append(baseCSV[i+1], newElement...)
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
			var aux float64
			aux, _ = parseFloat(reg.ReplaceAllString(rows[i][j], "${1}"))
			rows[i][j] = fmt.Sprintf("%v", aux)
		}
	}
	return rows
}

// TODO Unit Test
// BEGINNING
// "CENTRAL DA" , ""  ,"", ""
// "INFORMACAO" , "7342,32", "123,21", "123,21"
// MIDDLE
//	"CENTRAL DA INFORMACAO","7342,32", "123,21", "123,21"
// END
// "CENTRAL DA INFORMACAO"
//treatDoubleLines fix cels with double lines based in other colunm without double line.
func treatDoubleLines(rows [][]string, col int) [][]string {
	reg := regexp.MustCompile(`(\d+)( *[\.,]( *\d*( *\d))| +)+`)
	var fixedCsv [][]string
	for i := range rows {
		rows[i][0] = reg.ReplaceAllString(rows[i][0], "")
		rowFixed := []string{}
		if strings.Contains(rows[i][0], "ras desta natureza") {
			return fixedCsv
		}
		if rows[i][col] == "" {
			rows[i+1][0] = rows[i][0] + rows[i+1][0]
			continue
		}
		rowFixed = append(rowFixed, rows[i][0])
		fixedCsv = append(fixedCsv, rowFixed)
	}
	return fixedCsv
}

// parseFloat makes the string with format "xx.xx,xx" able to be parsed by the strconv.ParseFloat and return it parsed.
func parseFloat(s string) (float64, error) {
	s = strings.Trim(s, " ")
	s = strings.Replace(s, ".", "", -1)
	s = strings.Replace(s, ",", ".", -1)
	return strconv.ParseFloat(s, 64)
}

// employeeActive Checks if a role of a employee has words that indicate that the servant is inactive
func employeeActive(cargo string) bool {
	return !strings.Contains(cargo, "Inativos") && !strings.Contains(cargo, "aposentados")
}

// createCsv receive a fileName and a csv as [][]string, and creates a fileName.csv
func createCsv(fileName string, csvFinal [][]string) error {
	file, err := os.Create(fileName)
	if err != nil {
		return fmt.Errorf("Error creating csv: %v, error: %v", fileName, err)
	}
	defer file.Close()
	writer := gocsv.DefaultCSVWriter(file)
	defer writer.Flush()
	writer.WriteAll(csvFinal)
	return nil
}

func checkYM(month, year int) bool {
	if month >= 5 && year >= 2020 {
		return true
	}
	return false
}
