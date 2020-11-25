package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"time"

	"github.com/dadosjusbr/coletores"
)

var gitCommit string

func main() {
	outputFolder := os.Getenv("OUTPUT_FOLDER")
	month, err := strconv.Atoi(os.Getenv("MONTH"))
	if err != nil {
		logError("Invalid month (\"%s\"): %q", os.Getenv("MONTH"), err)
		os.Exit(1)
	}
	year, err := strconv.Atoi(os.Getenv("YEAR"))
	if err != nil {
		logError("Invalid year (\"%s\"): %q", os.Getenv("YEAR"), err)
		os.Exit(1)
	}
	if outputFolder == "" {
		outputFolder = "./output"
	}

	if err := os.Mkdir(outputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		logError("Error creating output folder(%s): %q", outputFolder, err)
		os.Exit(1)
	}

	files, err := Crawl(outputFolder, month, year)
	if err != nil {
		logError("Crawler error: %q", err)
		os.Exit(1)
	}

	var emps []coletores.Employee
	var parseErr error
	if emps, parseErr = Parse(files); parseErr != nil {
		logError("Parsing error: %q", parseErr)
		os.Exit(1)
	}

	er := coletores.ExecutionResult{Cr: newCrawlingResult(emps, files, month, year)}
	b, err := json.MarshalIndent(er, "", "  ")
	if err != nil {
		logError("JSON marshaling error: %q", err)
		os.Exit(1)
	}
	fmt.Printf("%s", string(b))
}

func newCrawlingResult(emps []coletores.Employee, files []string, month, year int) coletores.CrawlingResult {
	crawlerInfo := coletores.Crawler{
		CrawlerID:      "mppb",
		CrawlerVersion: gitCommit,
	}
	cr := coletores.CrawlingResult{
		AgencyID:  "mppb",
		Month:     month,
		Year:      year,
		Files:     files,
		Employees: emps,
		Crawler:   crawlerInfo,
		Timestamp: time.Now(),
	}
	return cr
}
