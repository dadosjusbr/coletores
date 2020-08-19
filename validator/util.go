package main

import (
	"fmt"
	"os"
	"strings"
	"time"

	"github.com/dadosjusbr/storage"
)

type employees struct {
	Aid                 string
	Year                int
	Month               int
	Reg                 string
	Name                string
	Role                string
	Type                string
	Workplace           string
	Active              bool
	IncomeTotal         float64
	Wage                float64
	PerksTotal          float64
	PerksFood           float64
	PerksTranport       float64
	PerksPreSchool      float64
	PerksHealth         float64
	PerksBirthAid       float64
	PerksHousingAid     float64
	PerksSubsistence    float64
	PerksOthers         float64
	OthersTotal         float64
	OthersPersonalBenef float64
	OthersEventualBenef float64
	OthersPosOfTrust    float64
	OthersDaily         float64
	OthersGrat          float64
	OthersOriPos        float64
	OthersOthers        float64
	DiscountsTotal      float64
	DiscountsPrevContr  float64
	DiscountsCeilRet    float64
	DiscountsIncomeTax  float64
	DiscountsOthers     float64
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
	//Change ',' for '-' to avoid unexpected split, changing csv columns
	basicInfo := fmt.Sprintf("%q, %q, %q, %q, %q, %t,", e.Reg, strings.ReplaceAll(e.Name, ",", "-"), strings.ReplaceAll(e.Role, ",", "-"), e.Type, strings.ReplaceAll(e.Workplace, ",", "-"), e.Active)
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
