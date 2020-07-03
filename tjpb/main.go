package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
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
	files, allEmployees, err := genEmployees(files, outputFolder, month, year)
	if err != nil {
		logError("Error generating employees, error: %v", err)
		os.Exit(1)
	}
	//teste := "transparencia_202005_servidores2_0.pdf"
	//teste2 := "transparencia_202004_servidores_0_0.pdf"
	//teste3 := "remuneracoes-magistrados-tjpb-01-2020.pdf"
	cr := newCrawlingResult(allEmployees, files, month, year)
	crJSON, err := json.MarshalIndent(cr, "", "  ")
	if err != nil {
		logError("JSON marshaling error: %v", err)
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

// genEmployees navigate
func genEmployees(files []string, outputFolder string, month, year int) ([]string, []storage.Employee, error) {
	var allEmployees []storage.Employee
	var pathFixed []string
	for i, f := range files {
		pathFixed = append(pathFixed, fmt.Sprintf("%v/%v", outputFolder, filepath.Base(f)))
		switch {
		case strings.Contains(f, "magistrados") && checkYM(month, year):
			emps, err := parserMagMay(pathFixed[i])
			if err != nil {
				return nil, nil, fmt.Errorf("error parsing magistrate may: %v", err)
			}
			allEmployees = append(allEmployees, emps...)
		case strings.Contains(f, "servidores") && checkYM(month, year):
			emps, err := parserServerMay(pathFixed[i])
			if err != nil {
				return nil, nil, fmt.Errorf("error parsing servant may: %v", err)
			}
			allEmployees = append(allEmployees, emps...)
		case strings.Contains(f, "magistrados") && !checkYM(month, year):
			emps, err := parserMagBefMay(pathFixed[i])
			if err != nil {
				return nil, nil, fmt.Errorf("error parsing magistrate before may: %v", err)
			}
			allEmployees = append(allEmployees, emps...)
		default:
			emps, err := parserServBefMay(pathFixed[i])
			if err != nil {
				return nil, nil, fmt.Errorf("error parsing servant before may: %v", err)
			}
			allEmployees = append(allEmployees, emps...)
		}
		files = append(files, strings.Replace(f, ".pdf", ".csv", 1))
	}
	return files, allEmployees, nil
}
