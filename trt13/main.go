package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"time"

	"github.com/dadosjusbr/storage"
	"github.com/joho/godotenv"
)

var gitCommit string

func main() {
	if err := godotenv.Load(); err != nil {
		logError("Error loading .env file")
		os.Exit(1)
	}

	month := flag.Int("mes", 0, "Mês a ser analisado")
	year := flag.Int("ano", 0, "Ano a ser analisado")

	outputFolder := os.Getenv("OUTPUT_FOLDER")
	flag.Parse()
	if *month == 0 || *year == 0 {
		logError("Month or year not provided. Please provide those to continue. --mes={} --ano={}\n")
		os.Exit(1)
	}
	if outputFolder == "" {
		outputFolder = "./output"
	}

	if err := os.Mkdir(outputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		logError("Error creating output folder(%s): %q", outputFolder, err)
		os.Exit(1)
	}
	filePath := fmt.Sprintf("%s/remuneracoes-trt13-%02d-%04d.json", outputFolder, *month, *year)

	if err := crawl(filePath, *month, *year); err != nil {
		logError("Crawler error(%02d-%04d): %q", *month, *year, err)
		os.Exit(1)
	}

	records, parsingErr := parse(filePath)
	if parsingErr != nil {
		logError("Parser error(%02d-%04d) - %s: %q", *month, *year, filePath, parsingErr)
	}

	cr := newCrawlingResult(records, filePath, *month, *year)
	crJSON, err := json.MarshalIndent(cr, "", "  ")
	if err != nil {
		logError("JSON marshaling error: %q", err)
		os.Exit(1)
	}
	fmt.Printf("%s", string(crJSON))
	if parsingErr != nil {
		os.Exit(1)
	}
}

func newCrawlingResult(emps []storage.Employee, filePath string, month, year int) storage.CrawlingResult {
	crawlerInfo := storage.Crawler{
		CrawlerID:      "trt13",
		CrawlerVersion: gitCommit,
	}
	cr := storage.CrawlingResult{
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
