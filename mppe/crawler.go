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

type employeeDescriptor struct {
	category  string
	yearCodes map[int]int
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

	members = map[string]employeeDescriptor{
		"membrosAtivos": {
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
		},
		"membrosInativos": {
			category: "proventos-de-todos-os-membros-inativos",
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
			category: "remuneracao-de-todos-os-servidores-atuvos",
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
		},
		"pensionistas": {
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
		},
		"colaboradores": {
			category: "valores-percebidos-por-todos-os-colaboradores",
			yearCodes: map[int]int{
				2016: 365,
				2017: 366,
				2018: 410,
				2019: 450,
				2020: 496,
			},
		},
		"exerciciosAnteriores": {
			category: "verbas-referentes-a-exercicios-anteriores",
			yearCodes: map[int]int{
				2016: 348,
				2017: 349,
				2018: 411,
				2019: 461,
				2020: 509,
			},
		},
		"indenizacoesEOutrosPagamentos": {
			category: "verbas-indenizatorias-e-outras-remuneracoes-temporarias",
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
		go func(member employeeDescriptor, month, year int) {
			defer wg.Done()
			link := fmt.Sprintf("%s%d-%s", baseURL, member.yearCodes[year], member.category)
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
			pattern := pathResolver(month, year, member.category)
			fileCode, err := findFileIdentifier(htmlAsString, pattern)
			if err != nil {
				errChannel <- err
			}
			urlToDownload := fmt.Sprintf("%s%d-%s?download=%s", baseURL, member.yearCodes[year], member.category, fileCode)
			filePath := fmt.Sprintf("%s/%s-%s-%d.xlsx", outputPath, member.category, fmt.Sprintf("%02d", month), year)
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
		close(pathChannel)
		close(errChannel)
	}()
	for path := range pathChannel {
		paths = append(paths, path)
	}
	return paths, nil
}

// it gets a HTML file as a string and searchs inside of it a pattern
// with only numbers
func findFileIdentifier(htmlAsString, pattern string) (string, error) {
	indexOfPattern := strings.Index(htmlAsString, pattern)
	nPreviousChars, err := strconv.Atoi(os.Getenv("PREVIOUS_N_CHARS"))
	if err != nil {
		nPreviousChars = 10
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

// download a file and writes on the given writer
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

// it returns the proper search path for a given member
func pathResolver(month, year int, member string) string {
	if member == "remuneracao-de-todos-os-membros-ativos" {
		if year != 2017 {
			return fmt.Sprintf(":membros-ativos-%s-%d", fmt.Sprintf("%02d", month), year)
		}
		return fmt.Sprintf(":quadro-de-membros-ativos-%s-%d", months[month], year)
	}
	if member == "proventos-de-todos-os-membros-inativos" {
		if year == 2014 && month != 1 {
			return fmt.Sprintf(":membros-inativos-%s-%d", fmt.Sprintf("%02d", month), year+1)
		}
		return fmt.Sprintf(":membros-inativos-%s-%d", fmt.Sprintf("%02d", month), year)
	}
	if member == "remuneracao-de-todos-os-servidores-atuvos" {
		return fmt.Sprintf(":servidores-ativos-%s-%d", fmt.Sprintf("%02d", month), year)
	}
	if member == "proventos-de-todos-os-servidores-inativos" {
		return fmt.Sprintf(":servidores-inativos-%s-%d", fmt.Sprintf("%02d", month), year)
	}
	if member == "valores-percebidos-por-todos-os-pensionistas" {
		return fmt.Sprintf(":pensionistas-%s-%d", fmt.Sprintf("%02d", month), year)
	}
	if member == "valores-percebidos-por-todos-os-colaboradores" {
		return fmt.Sprintf(":contracheque-valores-percebidos-colaboradores-%s", months[month])
	}
	if member == "verbas-referentes-a-exercicios-anteriores" {
		return fmt.Sprintf(":dea-%s%d", fmt.Sprintf("%02d", month), year)
	}
	return fmt.Sprintf(":virt-%s-%d", months[month], year)
}
