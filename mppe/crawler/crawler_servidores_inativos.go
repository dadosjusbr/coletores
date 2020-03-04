package crawler

import (
	"fmt"
	"io"
	"net/http"
	"os"
)

//ServidoresInativos wraps category and year codes
type ServidoresInativos struct {
	category  string
	yearCodes map[int]int
}

func newInactiveEmployees() ServidoresInativos {
	return ServidoresInativos{
		category: "proventos-de-todos-os-servidores-inativos",
		yearCodes: map[int]int{
			2011: 297,
			2012: 298,
			2013: 299,
			2014: 300,
			2015: 301,
			2016: 302,
			2017: 345,
			2018: 408,
			2019: 448,
			2020: 507,
		},
	}
}

func (c ServidoresInativos) crawl(outputPath string, month, year int) (string, error) {
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

	return filePath, nil
}

func (c ServidoresInativos) getURLForYear(year int) string {
	code := c.yearCodes[year]
	return fmt.Sprintf("%s%d-%s", baseURL, code, c.category)
}

func (c ServidoresInativos) getPatternToSearch(month, year int) string {
	var correctMonth string

	if month < 10 {
		correctMonth = fmt.Sprintf("0%d", month)
	} else {
		correctMonth = fmt.Sprintf("%d", month)
	}

	return fmt.Sprintf(":servidores-inativos-%s-%d", correctMonth, year)
}

func (c ServidoresInativos) getURLToDownloadSheet(year int, fileCode string) string {
	yearCode := c.yearCodes[year]
	return fmt.Sprintf("%s%d-%s?download=%s", baseURL, yearCode, c.category, fileCode)
}

func (c ServidoresInativos) getFileName(outputFolder string, month, year int) string {
	correctMonth := ""

	if month < 10 {
		correctMonth = fmt.Sprintf("0%d", month)
	} else {
		correctMonth = fmt.Sprintf("%d", month)
	}

	return fmt.Sprintf("%s/%s-%s-%d.xlsx", outputFolder, c.category, correctMonth, year)
}
