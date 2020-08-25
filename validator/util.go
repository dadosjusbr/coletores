package main

import (
	"fmt"
	"os"
	"strings"
	"time"

	"github.com/dadosjusbr/storage"
)

type employees struct {
	Aid                 string  `tableheader:"aid"`
	Year                int     `tableheader:"year"`
	Month               int     `tableheader:"month"`
	Reg                 string  `tableheader:"name"`
	Name                string  `tableheader:"role"`
	Role                string  `tableheader:"reg"`
	Type                string  `tableheader:"type"`
	Workplace           string  `tableheader:"workplace"`
	Active              bool    `tableheader:"active"`
	IncomeTotal         float64 `tableheader:"income_total"`
	Wage                float64 `tableheader:"wage"`
	PerksTotal          float64 `tableheader:"perks_total"`
	PerksFood           float64 `tableheader:"perks_food"`
	PerksTranport       float64 `tableheader:"perks_transportation"`
	PerksPreSchool      float64 `tableheader:"perks_preschool"`
	PerksHealth         float64 `tableheader:"perks_health"`
	PerksBirthAid       float64 `tableheader:"perks_birthaid"`
	PerksHousingAid     float64 `tableheader:"perks_housingaid"`
	PerksSubsistence    float64 `tableheader:"perks_subsistence"`
	PerksOthers         float64 `tableheader:"perks_others"`
	OthersTotal         float64 `tableheader:"others_total"`
	OthersPersonalBenef float64 `tableheader:"others_personalbenefits"`
	OthersEventualBenef float64 `tableheader:"others_eventualbenefits"`
	OthersPosOfTrust    float64 `tableheader:"others_positionoftrust"`
	OthersDaily         float64 `tableheader:"others_daily"`
	OthersGrat          float64 `tableheader:"others_gratification"`
	OthersOriPos        float64 `tableheader:"others_originposition"`
	OthersOthers        float64 `tableheader:"others_others"`
	DiscountsTotal      float64 `tableheader:"discounts_total"`
	DiscountsPrevContr  float64 `tableheader:"discounts_prevcontribution"`
	DiscountsCeilRet    float64 `tableheader:"discounts_ceilretention"`
	DiscountsIncomeTax  float64 `tableheader:"discounts_incometax"`
	DiscountsOthers     float64 `tableheader:"discounts_others"`
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
			result += "0.00,"
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
