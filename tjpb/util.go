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

type monthYear struct {
	month int
	year  int
}

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

// checkTemplate returns the caracter of which template should be used.
func checkTemplate(month, year int) (string, error) {
	templates := getTemplate()
	check := monthYear{month: month, year: year}
	for k, v := range templates {
		if contains(v, check) {
			return k, nil
		}
	}
	return "", fmt.Errorf("Tuple month and year was not found in any template.")
}

// getTemplate returns tuple of (month, year) in their adequated templates.
func getTemplate() map[string][]monthYear {
	A := []monthYear{
		{month: 4, year: 2018},
		{month: 4, year: 2019},
		{month: 3, year: 2019},
		{month: 2, year: 2019},
		{month: 1, year: 2019},
		{month: 12, year: 2018},
		{month: 11, year: 2018},
		{month: 10, year: 2018},
		{month: 9, year: 2018},
		{month: 8, year: 2018},
		{month: 6, year: 2018},
		{month: 5, year: 2018},
		{month: 2, year: 2018},
		{month: 11, year: 2019},
		{month: 9, year: 2019},
		{month: 8, year: 2019},
		{month: 7, year: 2019},
		{month: 6, year: 2019},
		{month: 5, year: 2019},
		{month: 4, year: 2020},
	}
	B := []monthYear{
		{month: 1, year: 2020},
		{month: 2, year: 2020},
		{month: 12, year: 2019},
		{month: 7, year: 2018},
		{month: 3, year: 2018},
	}
	C := []monthYear{
		{month: 1, year: 2018},
	}
	D := []monthYear{
		{month: 3, year: 2020},
	}
	E := []monthYear{
		{month: 5, year: 2020},
	}

	templates := map[string][]monthYear{
		"A": A,
		"B": B,
		"C": C,
		"D": D,
		"E": E,
	}
	return templates
}

// Check if a value contains in a array of monthYear.
func contains(s []monthYear, e monthYear) bool {
	for _, a := range s {
		if a == e {
			return true
		}
	}
	return false
}
