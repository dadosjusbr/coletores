package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"time"

	"github.com/dadosjusbr/storage"
	"github.com/joho/godotenv"
)

var gitCommit string

func main() {
	if err := godotenv.Load(); err != nil {
		logError("Error loading .env file")
	}
	outputFolder := os.Getenv("OUTPUT_FOLDER")
	if outputFolder == "" {
		outputFolder = "./output"
	}
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

	if err := os.Mkdir(outputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		logError("Error creating output folder(%s): %q", outputFolder, err)
		os.Exit(1)
	}

	files, err := crawl(outputFolder, month, year)
	if err != nil {
		logError("Error crawling (%d,%d,%s) error: %q", month, year, outputFolder, err)
		os.Exit(1)
	}
	//TODO - Check MOnth And Year
	fmt.Println(files)
	//teste := "transparencia_202005_servidores2_0.pdf"
	//teste2 := "transparencia_202004_servidores_0_0.pdf"
	teste3 := "remuneracoes-magistrados-tjpb-01-2020.pdf"
	emps, err := parserMagBefMay(teste3)
	if err != nil {
		logError("error parsing servant may: %q", err)
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
		CrawlerID:      "tjpb",
		CrawlerVersion: gitCommit,
	}
	cr := storage.CrawlingResult{
		AgencyID:  "tjpb",
		Month:     month,
		Year:      year,
		Files:     files,
		Employees: emps,
		Crawler:   crawlerInfo,
		Timestamp: time.Now(),
	}
	return cr
}
