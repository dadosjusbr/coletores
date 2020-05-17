package main

import (
	"archive/zip"
	"bytes"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/dadosjusbr/storage"
)

type dataPackage struct {
	AgencyID string
	Year     int
	Month    int
	Schema   map[string]interface{}
}

func main() {
	path := os.Getenv("OUTPUT_FOLDER")
	var cr storage.CrawlingResult
	crIN, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		logError("error reading crawling result: %q", err)
		os.Exit(1)
	}
	err = json.Unmarshal(crIN, &cr)
	if err != nil {
		logError("error getting crawling result: %q", err)
		os.Exit(1)
	}
	var bufCsv bytes.Buffer
	csvwriter := csv.NewWriter(&bufCsv)
	csvContent, err := writeAgencyMonthlyInfo(cr)
	if err != nil {
		logError("error logging agency: %q", err)
		os.Exit(1)
	}
	err = csvwriter.WriteAll(csvContent)
	if err != nil {
		logError("An error encountered while writing csv content %q", err)
		os.Exit(1)
	}
	buf := new(bytes.Buffer)
	w := zip.NewWriter(buf)
	schema, err := os.Open("schema.json")
	if err != nil {
		logError("error openning schema: %q", err)
		os.Exit(1)
	}
	defer schema.Close()
	byteSchema, err := ioutil.ReadAll(schema)
	if err != nil {
		logError("error reading schema: %q", err)
		os.Exit(1)
	}
	d := make(map[string]interface{})
	if err := json.Unmarshal(byteSchema, &d); err != nil {
		logError("Error unmarshaling schema: %q", err)
		os.Exit(1)
	}
	dtpBytes, err := json.Marshal(
		dataPackage{
			AgencyID: cr.AgencyID,
			Year:     cr.Year,
			Month:    cr.Month,
			Schema:   d,
		},
	)
	if err != nil {
		logError("Error getting DataPackage as bytes: %q", err)
		os.Exit(1)
	}
	addFileToZip(w, "data.csv", bufCsv.Bytes())
	addFileToZip(w, "datapackage.json", dtpBytes)
	w.Close()
	fileName := fmt.Sprintf("%s-%d-%d.zip", cr.AgencyID, cr.Year, cr.Month)
	filePath := filepath.Join(path, fileName)
	ioutil.WriteFile(filePath, buf.Bytes(), 0777)
	fmt.Print(filePath)
}

func addFileToZip(w *zip.Writer, name string, contents []byte) error {
	f, err := w.Create(name)
	if err != nil {
		return err
	}
	_, err = f.Write(contents)
	if err != nil {
		return err
	}
	return nil
}

// writeAgencyMonthlyInfo will take a AgencyMonthlyInfo and prints to stdout all the employees as csv lines.
func writeAgencyMonthlyInfo(cr storage.CrawlingResult) ([][]string, error) {
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
	return csvContent, nil
}

// empInfo returns the employee as a csv line.
func empInfo(e storage.Employee) string {
	basicInfo := fmt.Sprintf("%q, %q, %q, %q, %q, %t,", e.Reg, e.Name, e.Role, e.Type, e.Workplace, e.Active)
	income := incomeInfo(e.Income)
	discounts := discountInfo(e.Discounts)
	line := basicInfo + income + discounts
	return line
}

// incomeInfo generates the IncomeDetails as a csv line
func incomeInfo(i *storage.IncomeDetails) string {
	if i == nil {
		return ",,,,,,,,,,,,,,,,,,,,,"
	}
	result := fmt.Sprintf("%.2f,", i.Total) + getFloatValues(i.Wage)
	// Perks
	if i.Perks == nil {
		result += ",,,,,,,,,,"
	} else {
		result += fmt.Sprintf("%.2f,", i.Perks.Total) +
			getFloatValues(i.Perks.Food, i.Perks.Transportation, i.Perks.PreSchool, i.Perks.Health, i.Perks.BirthAid, i.Perks.HousingAid, i.Perks.Subsistence) +
			getMapTotal(i.Perks.Others)
	}
	// Others
	if i.Other == nil {
		result += ",,,,,,,,,"
	} else {
		result += fmt.Sprintf("%.2f,", i.Other.Total) +
			getFloatValues(i.Other.PersonalBenefits, i.Other.EventualBenefits, i.Other.PositionOfTrust, i.Other.Daily, i.Other.Gratification, i.Other.OriginPosition) +
			getMapTotal(i.Other.Others)
	}
	return result
}

// discountInfo generates discount info as a csv line.
func discountInfo(d *storage.Discount) string {
	if d == nil {
		return ",,,,,"
	}
	result := fmt.Sprintf("%.2f,", d.Total) + getFloatValues(d.PrevContribution, d.CeilRetention, d.IncomeTax) + getMapTotal(d.Others)
	return result
}

// getFloatValues takes a list of float pointers and returns them as a string for csv.
func getFloatValues(floats ...*float64) string {
	result := ""
	for _, p := range floats {
		if p == nil {
			result += ","
		} else {
			result += fmt.Sprintf("%.2f,", *p)
		}
	}
	return result
}

// getMapTotal returns sum of map values as a csv field("%.2f,").
func getMapTotal(m map[string]float64) string {
	total := 0.
	for _, v := range m {
		total += v
	}
	return fmt.Sprintf("%.2f,", total)
}

// logError prints to Stderr
func logError(format string, args ...interface{}) {
	time := fmt.Sprintf("%s: ", time.Now().Format(time.RFC3339))
	fmt.Fprintf(os.Stderr, time+format+"\n", args...)
}
