package main

import (
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"os"
	"time"

	"github.com/dadosjusbr/coletores/status"
	"github.com/dadosjusbr/storage"
)

var gitCommit string

func main() {
	month := flag.Int("mes", 0, "Mês a ser analisado")
	year := flag.Int("ano", 0, "Ano a ser analisado")
	flag.Parse()
	if *month == 0 || *year == 0 {
		e := status.NewError(status.InvalidParameters, errors.New("month or year not provided. Please provide those to continue. --mes={} --ano={}"))
		status.ExitFromError(e)
	}
	if *year < 2011 {
		e := status.NewError(status.InvalidParameters, errors.New("years before 2011 are not supported yet :("))
		status.ExitFromError(e)
	}
	if *month < 1 || *month > 12 || *month <= 0 {
		e := status.NewError(status.InvalidParameters, errors.New("invalid month value. Give values between 1 and 12"))
		status.ExitFromError(e)
	}
	if *year <= 0 {
		e := status.NewError(status.InvalidParameters, errors.New("invalid year value. Give years from and above 2011"))
		status.ExitFromError(e)
	}
	outputFolder := os.Getenv("OUTPUT_FOLDER")
	if outputFolder == "" {
		outputFolder = "./output"
	}
	if err := os.Mkdir(outputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		e := status.NewError(status.SystemError, fmt.Errorf("error creating output folder(%s): %q", outputFolder, err))
		status.ExitFromError(e)
	}
	// paths, err := Crawl(outputFolder, *month, *year, baseURL)
	// if err != nil {
	// 	status.ExitFromError(err)
	// }
	paths := []string{"./output/psit.xlsx"}
	employees, err := Parse(paths)
	if err != nil {
		status.ExitFromError(err)
	}
	cr := storage.CrawlingResult{
		AgencyID:  "mppe",
		Month:     *month,
		Year:      *year,
		Files:     paths,
		Employees: employees,
		Crawler: storage.Crawler{
			CrawlerID:      "mppe",
			CrawlerVersion: gitCommit,
		},
		Timestamp: time.Now(),
	}
	crJSON, err := json.MarshalIndent(cr, "", "  ")
	if err != nil {
		e := status.NewError(status.InvalidParameters, fmt.Errorf("JSON marshaling error: %q", err))
		status.ExitFromError(e)
	}
	fmt.Printf("%s", string(crJSON))
}
