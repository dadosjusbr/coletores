package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strconv"
	"time"

	"github.com/dadosjusbr/storage"
	"github.com/joho/godotenv"
)

var gitCommit string

func main() {
	if err := godotenv.Load(); err != nil {
		log.Println("No .env file to load.")
	}
	outputFolder := os.Getenv("OUTPUT_FOLDER")
	month, err := strconv.Atoi(os.Getenv("MONTH"))
	if err != nil {
		logError("Invalid month (\"%s\"): %q", os.Getenv("MONTH"), err)
		os.Exit(1)
	}
	year, err := strconv.Atoi(os.Getenv("ANO"))
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

	var emps []storage.Employee
	var parseErr error
	if emps, parseErr = Parse(files); parseErr != nil {
		logError("Parsing error: %q", parseErr)
		os.Exit(1)
	}

	cr := newCrawlingResult(emps, files, month, year)
	crJSON, err := json.MarshalIndent(cr, "", "  ")
	if err != nil {
		logError("JSON marshaling error: %q", err)
		os.Exit(1)
	}

	fmt.Printf("%s", string(crJSON))
}

func newCrawlingResult(emps []storage.Employee, files []string, month, year int) storage.CrawlingResult {
	crawlerInfo := storage.Crawler{
		CrawlerID:      "mppb",
		CrawlerVersion: gitCommit,
	}
	cr := storage.CrawlingResult{
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
