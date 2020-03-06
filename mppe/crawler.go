package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type pathResolver func(int, int) string

type fileStructure struct {
	category     string
	pathResolver pathResolver
	yearCodes    map[int]int
}

// This function returns the correct path to be searched
// on the HTML file for active member.
func activeMembersPathResolver(month, year int) string {
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

// This function returns the correct path to be searched
// on the HTML file for inactive member.
func inactiveMembersPathResolver(month, year int) string {
	var correctMonth string

	if month < 10 {
		correctMonth = fmt.Sprintf("0%d", month)
	} else {
		correctMonth = fmt.Sprintf("%d", month)
	}

	if year == 2014 && month != 1 {
		return fmt.Sprintf(":membros-inativos-%s-%d", correctMonth, year+1)
	}

	return fmt.Sprintf(":membros-inativos-%s-%d", correctMonth, year)
}

func activeEmployeesPathResolver(month, year int) string {
	var correctMonth string

	if month < 10 {
		correctMonth = fmt.Sprintf("0%d", month)
	} else {
		correctMonth = fmt.Sprintf("%d", month)
	}

	return fmt.Sprintf(":servidores-ativos-%s-%d", correctMonth, year)
}

func inactiveEmployeesPathResolver(month, year int) string {
	var correctMonth string

	if month < 10 {
		correctMonth = fmt.Sprintf("0%d", month)
	} else {
		correctMonth = fmt.Sprintf("%d", month)
	}

	return fmt.Sprintf(":servidores-inativos-%s-%d", correctMonth, year)
}

var (
	baseURL = "https://transparencia.mppe.mp.br/contracheque/category/"

	months = map[int]string{
		1:  "janeiro",
		2:  "fevereiro",
		3:  "marco",
		4:  "maio",
		5:  "abril",
		6:  "junho",
		7:  "julho",
		8:  "agosto",
		9:  "setembro",
		10: "outurbo",
		11: "novembro",
		12: "dezembro",
	}

	members = map[string]fileStructure{
		"membrosAtivos": {
			category:     "remuneracao-de-todos-os-membros-ativos",
			pathResolver: activeMembersPathResolver,
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
		},
		"membrosInativos": {
			category:     "proventos-de-todos-os-membros-inativos",
			pathResolver: inactiveMembersPathResolver,
			yearCodes: map[int]int{
				2011: 285,
				2012: 286,
				2013: 287,
				2014: 288,
				2015: 289,
				2016: 290,
				2017: 343,
				2018: 406,
				2019: 447,
				2020: 505,
			},
		},
		"servidoresAtivos": {
			category:     "remuneracao-de-todos-os-servidores-atuvos",
			pathResolver: activeEmployeesPathResolver,
			yearCodes: map[int]int{
				2011: 291,
				2012: 292,
				2013: 293,
				2014: 294,
				2015: 295,
				2016: 296,
				2017: 344,
				2018: 407,
				2019: 446,
				2020: 506,
			},
		},
		"servidoresInativos": {
			category:     "proventos-de-todos-os-servidores-inativos",
			pathResolver: inactiveEmployeesPathResolver,
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
		},
	}
)

// C bla
func C(outputPath string, month, year int) ([]string, error) {
	paths := make([]string, 8)

	for _, member := range members {
		link := getURLForYear(year, member.category, member.yearCodes)

		htmlPath := fmt.Sprintf("%s/%s_index.html", outputPath, member.category)

		f, err := os.Create(htmlPath)
		if err != nil {
			return nil, fmt.Errorf("Error creating file: %q", err)
		}
		defer f.Close()

		resp, err := http.Get(link)
		if err != nil {
			return nil, fmt.Errorf("Error getting downloading main html file :%q", err)
		}

		defer resp.Body.Close()

		if _, err := io.Copy(f, resp.Body); err != nil {
			return nil, fmt.Errorf("Error copying response content:%q", err)
		}

		fileAsHTML, err := fileToString(htmlPath)

		if err != nil {
			return nil, err
		}

		if err != nil {
			return nil, err
		}

		pattern := member.pathResolver(month, year)

		fileCode, err := findFileIdentifier(fileAsHTML, pattern)
		if err != nil {
			return nil, err
		}

		urlToDownload := getURLToDownloadSheet(year, member.category, fileCode, member.yearCodes)

		filePath := getFileName(member.category, outputPath, month, year)

		desiredFile, err := os.Create(filePath)

		if err != nil {
			return nil, fmt.Errorf("Error creating sheet file:%q", err)
		}

		defer desiredFile.Close()

		err = donwloadFile(urlToDownload, desiredFile)
		if err != nil {
			return nil, fmt.Errorf("Error downloading main file:%q", err)
		}

		err = os.Remove(htmlPath)
		if err != nil {
			return nil, fmt.Errorf("Error deleting html file: %q", err)
		}

		paths = append(paths, filePath)
	}
	return paths, nil
}

func getURLForYear(year int, category string, yearCodes map[int]int) string {
	code := yearCodes[year]
	return fmt.Sprintf("%s%d-%s", baseURL, code, category)
}

// it get a path of a file and returns the file content as a string
func fileToString(filePath string) (string, error) {
	bytes, err := ioutil.ReadFile(filePath)
	if err != nil {
		return "nil", fmt.Errorf("Error getting downloaded html as a string")
	}
	return string(bytes), nil
}

// it gets a HMLT file as a string and searchs inside of it a pattern
// with only numbers
func findFileIdentifier(htmlAsString, pattern string) (string, error) {
	indexOfPattern := strings.Index(htmlAsString, pattern)
	nPreviousChars, err := strconv.Atoi(os.Getenv("PREVIOUS_N_CHARS"))
	if err != nil {
		return "nil", fmt.Errorf("Not possible to get previous n chars from environment")
	}
	if indexOfPattern > 0 {
		substringWithFileIdentifier := htmlAsString[indexOfPattern-nPreviousChars : indexOfPattern]
		possibleMatches := regexp.MustCompile("[0-9]+").FindAllString(substringWithFileIdentifier, -1)
		if len(possibleMatches) == 0 {
			return "nil", fmt.Errorf("Was not possible to get file indetifier")
		}
		fileIdentifier := possibleMatches[0]
		return fileIdentifier, nil
	}
	return "nil", fmt.Errorf("Was not found anny pattern")
}

func getURLToDownloadSheet(year int, category, fileCode string, yearCodes map[int]int) string {
	yearCode := yearCodes[year]
	return fmt.Sprintf("%s%d-%s?download=%s", baseURL, yearCode, category, fileCode)
}

func getFileName(category, outputFolder string, month, year int) string {
	correctMonth := ""
	if month < 10 {
		correctMonth = fmt.Sprintf("0%d", month)
	} else {
		correctMonth = fmt.Sprintf("%d", month)
	}
	return fmt.Sprintf("%s/%s-%s-%d.xlsx", outputFolder, category, correctMonth, year)
}

// download a file and put its bytes into a buffer
func donwloadFile(url string, w io.Writer) error {
	resp, err := http.Get(url)
	if err != nil {
		return fmt.Errorf("error downloading file:%q", err)
	}
	defer resp.Body.Close()
	if _, err := io.Copy(w, resp.Body); err != nil {
		return fmt.Errorf("error copying response content:%q", err)
	}
	return nil
}
