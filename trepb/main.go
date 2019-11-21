package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"time"

	storage "github.com/dadosjusbr/storage"
	"github.com/joho/godotenv"
)

var gitCommit string

func main() {
	if err := godotenv.Load(); err != nil {
		log.Fatal("Error loading .env file")
	}

	month := flag.Int("mes", 0, "Mês a ser analisado")
	year := flag.Int("ano", 0, "Ano a ser analisado")
	name := os.Getenv("NAME")
	cpf := os.Getenv("CPF")
	outputFolder := os.Getenv("OUTPUT_FOLDER")
	flag.Parse()
	if *month == 0 || *year == 0 {
		fatalError("Month or year not provided. Please provide those to continue. --mes={} --ano={}\n")
	}
	if outputFolder == "" {
		outputFolder = "./output"
	}

	if err := os.Mkdir(outputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		fatalError("Error creating output folder(%s): %q", outputFolder, err)
	}

	filePath := filePath(outputFolder, *month, *year)
	if err := crawl(filePath, name, cpf, *month, *year); err != nil {
		fatalError("Crawler error(%02d-%04d): %q", *month, *year, err)
	}

	f, err := os.Open(filePath)
	if err != nil {
		log.Fatalf("error opening file (%s): %q", filePath, err)
	}
	defer f.Close()

	table, err := loadTable(f)
	if err != nil {
		log.Fatalf("error while loading data table from %s: %q", filePath, err)
	}

	records, err := employeeRecords(table)
	if err != nil {
		log.Fatalf("error while parsing data from table (%s): %q", filePath, err)
	}

	cr := newCrawlingResult(records, filePath, *month, *year)

	crJSON, err := json.MarshalIndent(cr, "", "  ")
	if err != nil {
		fatalError("JSON marshaling error: %q", err)
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

// fatalError prints to Stderr and calls exit(0)
func fatalError(format string, args ...interface{}) {
	time := fmt.Sprintf("%s: ", time.Now().Format(time.RFC3339))
	fmt.Fprintf(os.Stderr, time+format, args...)
	os.Exit(1)
}
