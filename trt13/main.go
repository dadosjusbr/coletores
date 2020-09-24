package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strconv"
	"time"

	"github.com/dadosjusbr/coletores"
	"github.com/dadosjusbr/coletores/status"
	"github.com/joho/godotenv"
)

var gitCommit string

func main() {
	if err := godotenv.Load(); err != nil {
		log.Println("No .env to read.")
	}
	month, err := strconv.Atoi(os.Getenv("MONTH"))
	if err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Invalid month (\"%s\"): %q", os.Getenv("MONTH"), err)))
	}
	year, err := strconv.Atoi(os.Getenv("YEAR"))
	if err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Invalid year (\"%s\"): %q", os.Getenv("YEAR"), err)))
	}
	outputFolder := os.Getenv("OUTPUT_FOLDER")
	if outputFolder == "" {
		outputFolder = "./output"
	}
	if err := os.Mkdir(outputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		status.ExitFromError(status.NewError(status.SystemError, fmt.Errorf("Error creating output folder(%s): %q", outputFolder, err)))
	}
	filePath := fmt.Sprintf("%s/remuneracoes-trt13-%02d-%04d.json", outputFolder, month, year)

	if err := crawl(filePath, month, year); err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Crawler error(%02d-%04d): %q", month, year, err)))
	}

	records, err := parse(filePath)
	if err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Parser error(%02d-%04d) - %s: %q", month, year, filePath, err)))
	}
	cr := newCrawlingResult(records, filePath, month, year)
	crJSON, err := json.MarshalIndent(cr, "", "  ")
	if err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("JSON marshaling error: %q", err)))
	}
	fmt.Printf("%s", string(crJSON))
}

func newCrawlingResult(emps []coletores.Employee, filePath string, month, year int) coletores.CrawlingResult {
	crawlerInfo := coletores.Crawler{
		CrawlerID:      "trt13",
		CrawlerVersion: gitCommit,
	}
	cr := coletores.CrawlingResult{
		AgencyID:  "trt13",
		Month:     month,
		Year:      year,
		Files:     []string{filePath},
		Employees: emps,
		Crawler:   crawlerInfo,
		Timestamp: time.Now(),
	}
	return cr
}
