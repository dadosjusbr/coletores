package main

import (
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
	}
	outputFolder := os.Getenv("OUTPUT_FOLDER")
	if outputFolder == "" {
		outputFolder = "./output"
	}

	month := flag.Int("mes", 0, "Mês a ser analisado")
	year := flag.Int("ano", 0, "Ano a ser analisado")
	flag.Parse()

	if *month == 0 || *year == 0 {
		logError("Month or year not provided. Please provide those to continue. --mes={} --ano={}\n")
		os.Exit(1)
	}

	if err := os.Mkdir(outputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		logError("Error creating output folder(%s): %q", outputFolder, err)
		os.Exit(1)
	}

	files, err := crawl(outputFolder, *month, *year)
	if err != nil {
		logError("Crawl(%d,%d) error: %q", *month, *year, outputFolder, err)
		os.Exit(1)
	}
	fmt.Println(files)
	teste := []string{"sample.pdf"}
	parser(teste)

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
