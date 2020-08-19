package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"

	"github.com/dadosjusbr/coletores/status"
	"github.com/dadosjusbr/storage"
)

type executionResult struct {
	Pr storage.PackagingResult `json:"pr,omitempty"`
	Cr storage.CrawlingResult  `json:"cr,omitempty"`
}

type dataExport struct {
	csv   [][]string
	dtpck dtpackage
}

type dtpackage struct {
	Aid    string `json:"aid,omitempty"`
	Month  int    `json:"month,omitempty"`
	Year   int    `json:"year,omitempty"`
	Schema Sch
}

//Sch is part of DataPackage that correspond mainly info about data.
type Sch struct {
	Profile      string         `json:"profile"`
	Resources    []Resources    `json:"resources"`
	Keywords     []string       `json:"keywords"`
	Name         string         `json:"name"`
	Title        string         `json:"title"`
	Description  string         `json:"description"`
	Homepage     string         `json:"homepage"`
	Version      string         `json:"version"`
	Contributors []Contributors `json:"contributors"`
	Licenses     []Licenses     `json:"licenses"`
}

//Resources Contains infos about csv presents on DataPackage.zip
type Resources struct {
	Name    string `json:"name"`
	Path    string `json:"path"`
	Profile string `json:"profile"`
	Schema  Schema `json:"schema"`
}

//Schema represents all the columns of data table
type Schema struct {
	Fields []Fields `json:"fields"`
}

//Fields is a struct corresponding to each column in the data table
type Fields struct {
	Name            string                 `json:"name"`
	Type            string                 `json:"type"`
	Format          string                 `json:"format,omitempty"`
	Title           string                 `json:"title"`
	Description     string                 `json:"description"`
	DescriptionPtbr string                 `json:"description-ptbr"`
	Constraint      map[string]interface{} `json:"constraints,omitempty"`
}

//Contributors contains info about contributor
type Contributors struct {
	Title string `json:"title"`
	Role  string `json:"role"`
}

//Licenses contain infos about project owner
type Licenses struct {
	Name  string `json:"name"`
	Title string `json:"title"`
	Path  string `json:"path"`
}

func main() {
	var er executionResult
	erIN, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		status.ExitFromError(status.NewError(4, fmt.Errorf("Error reading crawling result: %q", err)))
	}
	if err = json.Unmarshal(erIN, &er.Cr); err != nil {
		status.ExitFromError(status.NewError(5, fmt.Errorf("Error unmarshaling crawling resul from STDIN: %q", err)))
		os.Exit(1)
	}
	var v dataExport
	v.csv, v.dtpck = makeData(er.Cr)
	checkData(v)
	fmt.Println(v)
}

//makeData receives a cr and returns the data ready to be checked and packaged.
func makeData(cr storage.CrawlingResult) ([][]string, dtpackage) {
	csvContent, err := writeAgencyMonthlyInfo(cr)
	if err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("Error Writing csv content: %q", err)))
	}
	sc, err := os.Open("schema.json")
	if err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("Error openning schema: %q", err)))
	}
	defer sc.Close()
	schemaContent, err := ioutil.ReadAll(sc)
	if err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("Error reading schema: %q", err)))
	}
	// s := make(map[string]interface{})
	var s Sch
	if err := json.Unmarshal(schemaContent, &s); err != nil {
		status.ExitFromError(status.NewError(5, fmt.Errorf("Error unmarshaling schema: %q", err)))
	}
	var dtpackage dtpackage
	dtpackage.Aid = cr.AgencyID
	dtpackage.Year = cr.Year
	dtpackage.Month = cr.Month
	dtpackage.Schema = s
	return csvContent, dtpackage
}

//checkData iterate over the fields of csv and validate
func checkData(v dataExport) {
	// Converting interfaces resulting from the schema, to workable types.
	/*
		schemaFields, ok := v.dtpck["resources"].([]interface{})[0].(map[string]interface{})["schema"].(map[string]interface{})["fields"].([]interface{})
		if !ok {
			logError("Error getting fields of schema")
			os.Exit(1)
		}
	*/
	for key, value := range v.dtpck.Schema.Resources[0].Schema.Fields {
		for keyCsv, valueCsv := range v.csv {
			if keyCsv != 0 {
				checkType(valueCsv, key, value.Type)
			}
		}
	}
}

//checkType Check if data type correspond to expected data type
func checkType(vCsv []string, key int, value string) {
	switch value {
	case "number":
		if vCsv[key] == "" {
			break
		} else {
			_, err := strconv.ParseFloat(strings.TrimSpace(vCsv[key]), 64)
			if err != nil {
				logError("Field %v is not a float: %q", err)
				os.Exit(1)
			}
		}
	case "integer":
		if vCsv[key] == "" {
			break
		} else {
			_, err := strconv.ParseInt(strings.TrimSpace(vCsv[key]), 10, 0)
			if err != nil {
				logError("Field %v is not a Integer: %q", err)
				os.Exit(1)
			}
		}
	default:
		break
	}
}
