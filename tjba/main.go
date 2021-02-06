package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"time"

	"github.com/dadosjusbr/coletores"
	"github.com/dadosjusbr/coletores/status"
)

var gitCommit string

func main() {
	month := flag.Int("mes", 0, "Mês a ser analisado")
	year := flag.Int("ano", 0, "Ano a ser analisado")
	flag.Parse()
	outputFolder := os.Getenv("OUTPUT_FOLDER")
	if outputFolder == "" {
		outputFolder = "./output"
	}

	if err := os.Mkdir(outputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		status.ExitFromError(status.NewError(status.SystemError, fmt.Errorf("Error creating output folder(%s): %q", outputFolder, err)))
	}

	filePath := fmt.Sprintf("%s/remuneracoes-tjba-%02d-%04d.json", outputFolder, *month, *year)

	if err := crawl(filePath, *month, *year); err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Crawler error(%02d-%04d): %q", *month, *year, err)))
	}

	records, err := parse(filePath)
	if err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Parser error(%02d-%04d) - %s: %q", *month, *year, filePath, err)))
	}
	er := coletores.ExecutionResult{Cr: newCrawlingResult(records, filePath, *month, *year)}
	b, err := json.MarshalIndent(er, "", "  ")
	if err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("JSON marshaling error: %q", err)))
	}
	fmt.Println(string(b))
}

func newCrawlingResult(emps []coletores.Employee, filePath string, month, year int) coletores.CrawlingResult {
	return coletores.CrawlingResult{
		AgencyID:  "tjba",
		Month:     month,
		Year:      year,
		Files:     []string{filePath},
		Employees: emps,
		Crawler: coletores.Crawler{
			CrawlerID:      "tjba",
			CrawlerVersion: gitCommit,
		},
		Timestamp: time.Now(),
	}
}
