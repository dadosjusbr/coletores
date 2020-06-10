package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strconv"
	"time"

	"github.com/dadosjusbr/coletores/status"
	"github.com/dadosjusbr/storage"
	"github.com/joho/godotenv"
)

var gitCommit string

func main() {
	if err := godotenv.Load(); err != nil {
		log.Println("No .env file to load.")
	}
	month, err := strconv.Atoi(os.Getenv("MONTH"))
	if err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Invalid month (\"%s\"): %q", os.Getenv("MONTH"), err)))
	}
	year, err := strconv.Atoi(os.Getenv("YEAR"))
	if err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Invalid year (\"%s\"): %q", os.Getenv("YEAR"), err)))
	}
	name := os.Getenv("NAME")
	if name == "" {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Empty name, please set a name before start")))
	}
	cpf := os.Getenv("CPF")
	if cpf == "" {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Invalid cpf, please set a name before start")))
	}
	outputFolder := os.Getenv("OUTPUT_FOLDER")
	if outputFolder == "" {
		outputFolder = "./output"
	}
	if err := os.Mkdir(outputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		status.ExitFromError(status.NewError(status.SystemError, fmt.Errorf("Error creating output folder(%s): %q", outputFolder, err)))
	}

	filePath := filePath(outputFolder, month, year)
	if err := crawl(filePath, name, cpf, month, year); err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Crawler error(%02d-%04d): %q", month, year, err)))
	}

	f, err := os.Open(filePath)
	if err != nil {
		status.ExitFromError(status.NewError(status.SystemError, fmt.Errorf("error opening file (%s): %q", filePath, err)))
	}
	defer f.Close()

	table, err := loadTable(f)
	if err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("error while loading data table from %s: %q", filePath, err)))
	}

	records, err := employeeRecords(table)
	if err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Parsing error (%02d-%04d):\n%s", month, year, err)))
	}
	cr := newCrawlingResult(records, filePath, month, year)
	crJSON, err := json.MarshalIndent(cr, "", "  ")
	if err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("JSON marshaling error: %q", err)))
	}
	fmt.Printf("%s", string(crJSON))
}

func newCrawlingResult(emps []storage.Employee, filePath string, month, year int) storage.CrawlingResult {
	crawlerInfo := storage.Crawler{
		CrawlerID:      "trepb",
		CrawlerVersion: gitCommit,
	}
	cr := storage.CrawlingResult{
		AgencyID:  "trepb",
		Month:     month,
		Year:      year,
		Files:     []string{filePath},
		Employees: emps,
		Crawler:   crawlerInfo,
		Timestamp: time.Now(),
	}
	return cr
}
