package crawler

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"sync"
)

// IndenizacoesEOutrasRemuneracoes wraps category and year codes
type IndenizacoesEOutrasRemuneracoes struct {
	category  string
	yearCodes map[int]int
}

func newIndemnityAndOtherPayments() IndenizacoesEOutrasRemuneracoes {
	return IndenizacoesEOutrasRemuneracoes{
		category: "verbas-indenizatorias-e-outras-remuneracoes-temporarias",
		yearCodes: map[int]int{
			2018: 415,
			2019: 451,
			2020: 510,
		},
	}
}

func (c IndenizacoesEOutrasRemuneracoes) crawl(outputPath string, month, year int, wg *sync.WaitGroup) (string, error) {
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

func (c IndenizacoesEOutrasRemuneracoes) getURLForYear(year int) string {
	code := c.yearCodes[year]
	return fmt.Sprintf("%s%d-%s", baseURL, code, c.category)
}

func (c IndenizacoesEOutrasRemuneracoes) getPatternToSearch(month, year int) string {
	correctMonth := months[month]

	return fmt.Sprintf(":virt-%s-%d", correctMonth, year)
}

func (c IndenizacoesEOutrasRemuneracoes) getURLToDownloadSheet(year int, fileCode string) string {
	yearCode := c.yearCodes[year]
	return fmt.Sprintf("%s%d-%s?download=%s", baseURL, yearCode, c.category, fileCode)
}

func (c IndenizacoesEOutrasRemuneracoes) getFileName(outputFolder string, month, year int) string {
	correctMonth := ""

	if month < 10 {
		correctMonth = fmt.Sprintf("0%d", month)
	} else {
		correctMonth = fmt.Sprintf("%d", month)
	}

	return fmt.Sprintf("%s/%s-%s-%d.xlsx", outputFolder, c.category, correctMonth, year)
}
