package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"strings"

	"github.com/dadosjusbr/coletores/status"
	"github.com/dadosjusbr/storage"
	"github.com/frictionlessdata/tableschema-go/schema"
	"github.com/frictionlessdata/tableschema-go/table"
)

type executionResult struct {
	Pr storage.PackagingResult `json:"pr,omitempty"`
	Cr storage.CrawlingResult  `json:"cr,omitempty"`
}

type dataExport struct {
	csv   [][]string
	dtpck map[string]interface{}
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
	csvContent := mountCSV(er.Cr)
	for i := range csvContent {
		csvContent[i][8] = strings.TrimSpace(csvContent[i][8])
	}
	table := table.FromSlices(csvContent[0], csvContent[1:])
	dtpckg := mountDtPckg(er.Cr)
	sch := mountSchema(dtpckg)
	var emp []employees
	if err := sch.CastTable(table, &emp); err != nil {
		fmt.Println(err)
	}
	var v dataExport
	v.csv = csvContent
	v.dtpck = dtpckg
	fmt.Println(v)
}

//mountCSV receives a CR and returns header and content of a csv.
func mountCSV(cr storage.CrawlingResult) [][]string {
	var csvContent [][]string
	headers := []string{"aid", "year", "month",
		"reg", "name", "role", "type", "workplace", "active", "income_total", "wage",
		"perks_total", "perks_food", "perks_transportation", "perks_preschool", "perks_health", "perks_birthaid", "perks_housingaid", "perks_subsistence", "perks_others",
		"others_total", "others_personalbenefits", "others_eventualbenefits", "others_positionoftrust", "others_daily", "others_gratification", "others_originposition", "others_others",
		"discounts_total", "discounts_prevcontribution", "discounts_ceilretention", "discounts_incometax", "discounts_others"}
	csvContent = append(csvContent, headers)
	for _, e := range cr.Employees {
		basicInfo := fmt.Sprintf("%q, %d, %d,", cr.AgencyID, cr.Year, cr.Month)
		empInfo := empInfo(e)
		content := basicInfo + empInfo[:len(empInfo)-1]
		csvContent = append(csvContent, strings.Split(content, ","))
	}
	return csvContent
}

//mountDtPckg returns DataPackage mounted.
func mountDtPckg(cr storage.CrawlingResult) map[string]interface{} {
	sc, err := os.Open("schema.json")
	if err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("Error openning schema: %q", err)))
	}
	defer sc.Close()
	schemaContent, err := ioutil.ReadAll(sc)
	if err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("Error reading schema: %q", err)))
	}
	s := make(map[string]interface{})
	if err := json.Unmarshal(schemaContent, &s); err != nil {
		status.ExitFromError(status.NewError(5, fmt.Errorf("Error unmarshaling schema: %q", err)))
	}
	s["aid"] = cr.AgencyID
	s["year"] = cr.Year
	s["month"] = cr.Month
	return s
}

func mountSchema(dtpckg map[string]interface{}) *schema.Schema {
	schemaFields, ok := dtpckg["resources"].([]interface{})[0].(map[string]interface{})["schema"]
	if !ok {
		logError("Error getting fields of schema")
		os.Exit(1)
	}
	schJSON, err := json.Marshal(schemaFields)
	if err != nil {
		logError("Error getting schema fields to JSON")
		os.Exit(1)
	}
	var schemaF schema.Schema
	if err := schemaF.UnmarshalJSON(schJSON); err != nil {
		logError("Error getting schema fields to JSON")
		os.Exit(1)
	}
	return &schemaF
}
