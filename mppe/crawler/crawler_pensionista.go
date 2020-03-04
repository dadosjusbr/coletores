package crawler

//pensioner

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"sync"
)

//Pensionista wraps category and year codes
type Pensionista struct {
	category  string
	yearCodes map[int]int
}

func newPensioner() Pensionista {
	return Pensionista{
		category: "valores-percebidos-por-todos-os-pensionistas",
		yearCodes: map[int]int{
			2011: 303,
			2012: 304,
			2013: 305,
			2014: 306,
			2015: 307,
			2016: 308,
			2017: 346,
			2018: 409,
			2019: 449,
			2020: 508,
		},
	}
}

func (c Pensionista) crawl(outputPath string, month, year int, wg *sync.WaitGroup) (string, error) {
	link := c.getURLForYear(year)

	htmlPath := fmt.Sprintf("%s/%s_index.html", outputPath, c.category)

	f, err := os.Create(htmlPath)
	if err != nil {
		return "nil", fmt.Errorf("Error creating file: %q", err)
	}
	defer f.Close()

	resp, err := http.Get(link)
	if err != nil {
		return "nil", fmt.Errorf("Error getting downloading main html file :%q", err)
	}

	defer resp.Body.Close()

	if _, err := io.Copy(f, resp.Body); err != nil {
		return "nil", fmt.Errorf("Error copying response content:%q", err)
	}

	fileAsHTML, err := fileToString(htmlPath)

	if err != nil {
		return "nil", err
	}

	pattern := c.getPatternToSearch(month, year)

	fileCode, err := findFileIdentifier(fileAsHTML, pattern)
	if err != nil {
		return "nil", err
	}

	urlToDownload := c.getURLToDownloadSheet(year, fileCode)

	filePath := c.getFileName(outputPath, month, year)

	desiredFile, err := os.Create(filePath)

	if err != nil {
		return "nil", fmt.Errorf("Error creating sheet file:%q", err)
	}

	defer desiredFile.Close()

	err = donwloadFile(urlToDownload, desiredFile)
	if err != nil {
		return "nil", fmt.Errorf("Error downloading main file:%q", err)
	}

	err = os.Remove(htmlPath)
	if err != nil {
		return "nil", fmt.Errorf("Error deleting html file: %q", err)
	}

	defer wg.Done()

	return filePath, nil
}

func (c Pensionista) getURLForYear(year int) string {
	code := c.yearCodes[year]
	return fmt.Sprintf("%s%d-%s", baseURL, code, c.category)
}

func (c Pensionista) getPatternToSearch(month, year int) string {
	var correctMonth string

	if month < 10 {
		correctMonth = fmt.Sprintf("0%d", month)
	} else {
		correctMonth = fmt.Sprintf("%d", month)
	}

	return fmt.Sprintf(":pensionistas-%s-%d", correctMonth, year)
}

func (c Pensionista) getURLToDownloadSheet(year int, fileCode string) string {
	yearCode := c.yearCodes[year]
	return fmt.Sprintf("%s%d-%s?download=%s", baseURL, yearCode, c.category, fileCode)
}

func (c Pensionista) getFileName(outputFolder string, month, year int) string {
	correctMonth := ""

	if month < 10 {
		correctMonth = fmt.Sprintf("0%d", month)
	} else {
		correctMonth = fmt.Sprintf("%d", month)
	}

	return fmt.Sprintf("%s/%s-%s-%d.xlsx", outputFolder, c.category, correctMonth, year)
}
