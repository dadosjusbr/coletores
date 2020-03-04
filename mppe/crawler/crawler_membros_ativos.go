package crawler

import (
	"fmt"
	"io"
	"net/http"
	"os"
)

// MembrosAtivos wraps category and year codes
type MembrosAtivos struct {
	category  string
	yearCodes map[int]int
}

func newActiveMembers() MembrosAtivos {
	return MembrosAtivos{
		category: "remuneracao-de-todos-os-membros-ativos",
		yearCodes: map[int]int{
			2011: 280,
			2012: 281,
			2013: 309,
			2014: 282,
			2015: 283,
			2016: 284,
			2017: 324,
			2018: 405,
			2019: 445,
			2020: 504,
		},
	}
}

func (c MembrosAtivos) crawl(outputPath string, month, year int) (string, error) {
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

func (c MembrosAtivos) getURLForYear(year int) string {
	code := c.yearCodes[year]
	return fmt.Sprintf("%s%d-%s", baseURL, code, c.category)
}

func (c MembrosAtivos) getPatternToSearch(month, year int) string {
	var correctMonth string

	if month < 10 {
		correctMonth = fmt.Sprintf("0%d", month)
	} else {
		correctMonth = fmt.Sprintf("%d", month)
	}

	if year != 2017 {
		return fmt.Sprintf(":membros-ativos-%s-%d", correctMonth, year)
	}

	correctMonth = months[month]
	return fmt.Sprintf(":quadro-de-membros-ativos-%s-%d", correctMonth, year)
}

func (c MembrosAtivos) getURLToDownloadSheet(year int, fileCode string) string {
	yearCode := c.yearCodes[year]
	return fmt.Sprintf("%s%d-%s?download=%s", baseURL, yearCode, c.category, fileCode)
}

func (c MembrosAtivos) getFileName(outputFolder string, month, year int) string {
	correctMonth := ""

	if month < 10 {
		correctMonth = fmt.Sprintf("0%d", month)
	} else {
		correctMonth = fmt.Sprintf("%d", month)
	}

	return fmt.Sprintf("%s/%s-%s-%d.xlsx", outputFolder, c.category, correctMonth, year)
}
