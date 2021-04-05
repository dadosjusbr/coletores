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

	"github.com/dadosjusbr/coletores/status"
)

var re = regexp.MustCompile("\\b\\d{4}\\b")

// it wraps data about a employee category, where category
// is the category name and yearCodes is a map that
// translates the desired year of search to a number that
// represents the desired file, like an id, on the MPPE system.
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
				2018: 405,
				2019: 445,
				2020: 504,
			},
		},
)

// Crawl download all files related to the MPPE salaries and return their local paths
func Crawl(outputPath string, month, year int, host string) ([]string, error) {
	var paths []string
	for _, member := range members {
		/*Aqui basta montar a requisição para Membros Ativos*/ 
	return paths, nil
}
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
	switch member {
	case "remuneracao-de-todos-os-membros-ativos":
		return fmt.Sprintf(":membros-ativos-%s-%d", fmt.Sprintf("%02d", month), year)
	default:
		return fmt.Sprintf(":virt-%s-%d", months[month], year)
	}
}
