package main

import (
	"fmt"
	"os"
	"regexp"
	"strings"
	"time"
)

// logError prints to Stderr
func logError(format string, args ...interface{}) {
	time := fmt.Sprintf("%s: ", time.Now().Format(time.RFC3339))
	fmt.Fprintf(os.Stderr, time+format+"\n", args...)
}

//TODO UNIT TEST
//appendCSVColumns receives a base csv and append columns of a new csv to the right.
func appendCSVColumns(baseCSV, newColumns [][]string) [][]string {
	if len(baseCSV) == 0 {
		for i := range newColumns {
			if strings.Contains(newColumns[i][0], "Legenda das") {
				break
			}
			baseCSV = append(baseCSV, newColumns[i])
		}
	} else {
		for i := 0; i < len(baseCSV); i++ {
			var newElement []string
			newElement = append(newElement, newColumns[i]...)
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

// TODO Unit Test
// BEGINNING
// "CENTRAL DA" , ""  ,"", ""
// "INFORMACAO" , "7342,32", "123,21", "123,21"
// MIDDLE
//	"CENTRAL DA INFORMACAO","7342,32", "123,21", "123,21"
// END
// "CENTRAL DA INFORMACAO"
//treatDoubleLines fix cels with double lines based in other colunm without double line.
func treatDoubleLines(rows [][]string) [][]string {
	reg := regexp.MustCompile(`(\d+)( *[\.,]( *\d*( *\d))| +)+`)
	var fixedCsv [][]string
	for i := range rows {
		rows[i][0] = reg.ReplaceAllString(rows[i][0], "")
		rowFixed := []string{}
		if strings.Contains(rows[i][0], "ras desta natureza") {
			return fixedCsv
		}
		if rows[i][2] == "" {
			rows[i+1][0] = rows[i][0] + rows[i+1][0]
			continue
		}
		rowFixed = append(rowFixed, rows[i][0])
		fixedCsv = append(fixedCsv, rowFixed)
	}
	return fixedCsv
}
