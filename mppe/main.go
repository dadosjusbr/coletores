package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"time"

	"github.com/dadosjusbr/storage"
)

var gitCommit string

func main() {
	month := flag.Int("mes", 0, "Mês a ser analisado")
	year := flag.Int("ano", 0, "Ano a ser analisado")
	flag.Parse()
	if *month == 0 || *year == 0 {
		logError("month or year not provided. Please provide those to continue. --mes={} --ano={}\n")
		os.Exit(1)
	}
	if *year < 2011 {
		logError("years before 2011 are not supported yet :(")
		os.Exit(1)
	}
	if *month < 1 || *month > 12 || *month <= 0 {
		logError("invalid month value. Give values between 1 and 12")
		os.Exit(1)
	}
	if *year <= 0 {
		logError("invalid year value. Give years from and above 2011")
		os.Exit(1)
	}
	outputFolder := os.Getenv("OUTPUT_FOLDER")
	if outputFolder == "" {
		outputFolder = "./output"
	}
	if err := os.Mkdir(outputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		logError("error creating output folder(%s): %q", outputFolder, err)
		os.Exit(1)
	}
	paths, err := Crawl(outputFolder, *month, *year, baseURL)
	if err != nil {
		logError("error on crawling: ", err.Error())
		os.Exit(1)
	}
	employees, err := Parse(paths)
	if err != nil {
		logError("error on parsing: ", err.Error())
		os.Exit(1)
	}
	crawlingResult := newCrawlingResult(employees, paths, *month, *year)
	crJSON, err := json.MarshalIndent(crawlingResult, "", "  ")
	if err != nil {
		logError("JSON marshaling error: %q", err)
		os.Exit(1)
	}
	fmt.Printf("%s", string(crJSON))
	fmt.Println(len(employees))
}

func newCrawlingResult(emps []storage.Employee, files []string, month, year int) storage.CrawlingResult {
	crawlerInfo := storage.Crawler{
		CrawlerID:      "mppe",
		CrawlerVersion: gitCommit,
	}
	cr := storage.CrawlingResult{
		AgencyID:  "mppe",
		Month:     month,
		Year:      year,
		Files:     files,
		Employees: emps,
		Crawler:   crawlerInfo,
		Timestamp: time.Now(),
	}
	return cr
}

func logError(format string, args ...interface{}) {
	time := fmt.Sprintf("%s: ", time.Now().Format(time.RFC3339))
	fmt.Fprintf(os.Stderr, time+format+"\n", args...)
}
