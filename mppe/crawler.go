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
	"sync"
)

type pathResolver func(int, int) string

type fileStructure struct {
	category     string
	pathResolver pathResolver
	yearCodes    map[int]int
}

/*
 *	All '...Pathresolver' functions has the aim to
 * create a pattern to be searched on the HTML file of
 * year pages in order to get a specif number that actualy
 * helps us to download the file.
 *
 *	At every HMLT there are some patter like:
 *
 *	download=${4 DIGITS HERE}:${SOME TEXT WITH MONTH AND YEAR}
 *
 * so what all these below functions do is just create
 * the string for the appropriate situation.
 *
 */

/*
 *	Active members path resolver
 *
 * 	This function has a particular case for the year 2017,
 * where we need to change the pattern string.
 */
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

/*
 *	Inactive members path resolver
 *
 * 	This function has a particular case for months greater
 * than 1 in 2014 in such a way the year on HTML page is
 * 2015.
 */
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

/*
 *	Active Employees path resolver
 *
 * 	This function has no particular cases for its path.
 */
func activeEmployeesPathResolver(month, year int) string {
	var correctMonth string
	if month < 10 {
		correctMonth = fmt.Sprintf("0%d", month)
	} else {
		correctMonth = fmt.Sprintf("%d", month)
	}
	return fmt.Sprintf(":servidores-ativos-%s-%d", correctMonth, year)
}

/*
 *	Inactive Employees path resolver
 *
 * 	This function has no particular cases for its path.
 */
func inactiveEmployeesPathResolver(month, year int) string {
	var correctMonth string
	if month < 10 {
		correctMonth = fmt.Sprintf("0%d", month)
	} else {
		correctMonth = fmt.Sprintf("%d", month)
	}
	return fmt.Sprintf(":servidores-inativos-%s-%d", correctMonth, year)
}

/*
 *	Pensioners path resolver
 *
 * 	This function has no particular cases for its path.
 */
func pensionersPathResolver(month, year int) string {
	var correctMonth string
	if month < 10 {
		correctMonth = fmt.Sprintf("0%d", month)
	} else {
		correctMonth = fmt.Sprintf("%d", month)
	}
	return fmt.Sprintf(":pensionistas-%s-%d", correctMonth, year)
}

/*
 *	Parteners path resolver
 *
 * 	This function has no particular cases for its path.
 */
func partnersPathResolver(month, year int) string {
	correctMonth := months[month]
	return fmt.Sprintf(":contracheque-valores-percebidos-colaboradores-%s", correctMonth)
}

/*
 *	Previous years path resolver
 *
 * 	This function has no particular cases for its path.
 */
func previousYearsPatternToSearch(month, year int) string {
	var correctMonth string
	if month < 10 {
		correctMonth = fmt.Sprintf("0%d", month)
	} else {
		correctMonth = fmt.Sprintf("%d", month)
	}
	return fmt.Sprintf(":dea-%s%d", correctMonth, year)
}

/*
 *	Indenity and other payments  path resolver
 *
 * 	This function has no particular cases for its path.
 */
func indemnityAndOtherPaymentsPatternToSearch(month, year int) string {
	correctMonth := months[month]
	return fmt.Sprintf(":virt-%s-%d", correctMonth, year)
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
		"pensionistas": {
			category:     "valores-percebidos-por-todos-os-pensionistas",
			pathResolver: pensionersPathResolver,
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
		},
		"colaboradores": {
			category:     "valores-percebidos-por-todos-os-colaboradores",
			pathResolver: partnersPathResolver,
			yearCodes: map[int]int{
				2016: 365,
				2017: 366,
				2018: 410,
				2019: 450,
				2020: 496,
			},
		},
		"exerciciosAnteriores": {
			category:     "verbas-referentes-a-exercicios-anteriores",
			pathResolver: previousYearsPatternToSearch,
			yearCodes: map[int]int{
				2016: 348,
				2017: 349,
				2018: 411,
				2019: 461,
				2020: 509,
			},
		},
		"indenizacoesEOutrosPagamentos": {
			category:     "verbas-indenizatorias-e-outras-remuneracoes-temporarias",
			pathResolver: indemnityAndOtherPaymentsPatternToSearch,
			yearCodes: map[int]int{
				2018: 415,
				2019: 451,
				2020: 510,
			},
		},
	}
)

// Crawl download all files related to the MPPE salaries and return their local paths
func Crawl(outputPath string, month, year int) ([]string, error) {
	paths := make([]string, 8)

	pathChannel := make(chan string, 8)

	errChannel := make(chan error, 8)

	var wg sync.WaitGroup

	for _, member := range members {
		wg.Add(1)
		go func(member fileStructure, month, year int) {
			defer wg.Done()
			link := getURLForYear(year, member.category, member.yearCodes)
			resp, err := http.Get(link)
			if err != nil {
				errChannel <- fmt.Errorf("error getting downloading main html file :%q", err)
			}
			defer resp.Body.Close()
			b, err := ioutil.ReadAll(resp.Body)
			if err != nil {
				errChannel <- fmt.Errorf("error reading response body: %q", err)
			}
			htmlAsString := string(b)
			pattern := member.pathResolver(month, year)
			fileCode, err := findFileIdentifier(htmlAsString, pattern)
			if err != nil {
				errChannel <- err
			}
			urlToDownload := getURLToDownloadSheet(year, member.category, fileCode, member.yearCodes)
			filePath := getFileName(member.category, outputPath, month, year)
			desiredFile, err := os.Create(filePath)
			if err != nil {
				errChannel <- fmt.Errorf("error creating sheet file:%q", err)
			}
			defer desiredFile.Close()
			err = donwloadFile(urlToDownload, desiredFile)
			if err != nil {
				errChannel <- fmt.Errorf("error downloading main file: %s %q", filePath, err)
			}
			pathChannel <- filePath
		}(member, month, year)
	}

	go func() {
		wg.Wait()
		close(errChannel)
		close(pathChannel)
	}()

	for err := range errChannel {
		if err != nil {
			return nil, err
		}
	}

	for path := range pathChannel {
		paths = append(paths, path)
	}

	return paths, nil
}

// it returns the url for a specific year webpage to do crawling
func getURLForYear(year int, category string, yearCodes map[int]int) string {
	code := yearCodes[year]
	return fmt.Sprintf("%s%d-%s", baseURL, code, category)
}

// it gets a HTML file as a string and searchs inside of it a pattern
// with only numbers
func findFileIdentifier(htmlAsString, pattern string) (string, error) {
	indexOfPattern := strings.Index(htmlAsString, pattern)
	nPreviousChars, err := strconv.Atoi(os.Getenv("PREVIOUS_N_CHARS"))
	if err != nil {
		return "nil", fmt.Errorf("not possible to get previous n chars from environment %q", err)
	}
	if indexOfPattern > 0 {
		substringWithFileIdentifier := htmlAsString[indexOfPattern-nPreviousChars : indexOfPattern]
		possibleMatches := regexp.MustCompile("[0-9]+").FindAllString(substringWithFileIdentifier, -1)
		if len(possibleMatches) == 0 {
			return "nil", fmt.Errorf("was not possible to get file indetifier")
		}
		fileIdentifier := possibleMatches[0]
		return fileIdentifier, nil
	}
	return "nil", fmt.Errorf("was not found anny pattern")
}

// returns the URL to download the file
func getURLToDownloadSheet(year int, category, fileCode string, yearCodes map[int]int) string {
	yearCode := yearCodes[year]
	return fmt.Sprintf("%s%d-%s?download=%s", baseURL, yearCode, category, fileCode)
}

// it just returns the name of xlsx to be saved
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
