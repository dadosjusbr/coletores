package main

import (
	"fmt"
	"io"
	"math"
	"os"
	d "trepb/storage"

	"github.com/antchfx/htmlquery"
	"golang.org/x/net/html"
)

const (
	// Basic info
	name      = `//*[@class="c01"]`
	role      = `//*[@class="c02"]`
	workplace = `//*[@class="c03 capitalize"]`
	// Income
	wage  = `//*[@class="c04"]`
	perks = `//*[@class="c06"]`
	// Income.Others
	personalBenefits = `//*[@class="c05"]`
	positionOfTrust  = `//*[@class="c17"]`
	eventualBenefits = `//*[@class="c07"]`
	gratification    = `//*[@class="c08"]`
	// Discount
	prevContribution = `//*[@class="c10"]`
	ceilRetention    = `//*[@class="c13"]`
	incomeTax        = `//*[@class="c11"]`
	sundry           = `//*[@class="c12"]`
	// Origin Position
	originPosition = `//*[@class="c16"]`
)

// parser will return a slice of employees for a given month and year
func parser(month, year int) ([]d.Employee, error) {
	fileName := fmt.Sprintf("./output/remuneracoes-trepb-%02d-%04d.html", month, year)
	f, err := os.Open(fileName)
	if err != nil {
		return nil, fmt.Errorf("error opening file (%s): %q", fileName, err)
	}

	table, err := loadTable(f)
	if err != nil {
		return nil, fmt.Errorf("error while loading data table from %s: %q", fileName, err)
	}

	e, err := employeeRecords(table)
	if err != nil {
		return nil, fmt.Errorf("error while parsing data from table (%s): %q", fileName, err)
	}

	return e, nil
}

// loadTable will load a the correct data table from an io.Reader that should hold an html page.
func loadTable(r io.Reader) (*html.Node, error) {
	doc, err := htmlquery.Parse(r)
	if err != nil {
		return nil, fmt.Errorf("error parsing file html tree: %q", err)
	}

	tableXPath := `//*[@id="tblDetalhamentoFolhaPagamentoPessoal"]`
	table, err := htmlquery.Query(doc, tableXPath)
	if err != nil {
		return nil, fmt.Errorf("error making xpathquery(%s) in file: %q", tableXPath, err)
	}
	if table == nil {
		return nil, fmt.Errorf("error finding data table in file: %q", err)
	}

	return table, nil
}

// employeeRecords will retrieve a list of employees from the data table
func employeeRecords(table *html.Node) ([]d.Employee, error) {
	records, err := htmlquery.QueryAll(table, "//tr")
	if err != nil {
		return nil, fmt.Errorf("error while querying data table for tr elements: %q", err)
	}

	employees := make([]d.Employee, 0)

	for i, row := range records[1:] {
		e, err := newEmployee(row)
		if err != nil {
			return nil, fmt.Errorf("error trying to parse employee columns(position %d): %q", i, err)
		}
		employees = append(employees, e)
	}
	return employees, nil
}

// newEmployee will create a new employee from a row.
func newEmployee(row *html.Node) (d.Employee, error) {
	// Creating employee struct as needed.
	var e d.Employee
	e.Income = &d.IncomeDetails{Other: &d.Funds{}, Perks: &d.Perks{}}
	e.Discounts = &d.Discount{}

	if err := employeeBasicInfo(row, &e); err != nil {
		return e, fmt.Errorf("error retrieving employee basic info: %q", err)
	}
	if err := employeeIncome(row, e.Income); err != nil {
		return e, fmt.Errorf("error retrieving employee income info: %q", err)
	}
	if err := employeeDiscounts(row, e.Discounts); err != nil {
		return e, fmt.Errorf("error retrieving employee discounts info: %q", err)
	}
	return e, nil
}

// employeeBasicInfo will fetch basic info from the rows.
func employeeBasicInfo(row *html.Node, e *d.Employee) error {
	if err := retrieveString(row, &e.Name, name); err != nil {
		return fmt.Errorf("error retrieving name: %q", err)
	}
	if err := retrieveString(row, &e.Role, role); err != nil {
		return fmt.Errorf("error retrieving role: %q", err)
	}
	if err := retrieveString(row, &e.Workplace, workplace); err != nil {
		return fmt.Errorf("error retrieving workplace: %q", err)
	}
	e.Active = active(e.Role)
	return nil
}

// employeeIncome will fetch Income info from the rows.
func employeeIncome(row *html.Node, i *d.IncomeDetails) error {
	if err := retrieveFloat(row, &i.Wage, wage); err != nil {
		return fmt.Errorf("error retrieving Wage: %q", err)
	}
	if err := retrieveFloat(row, &i.Perks.Total, perks); err != nil {
		return fmt.Errorf("error retrieving perks: %q", err)
	}
	if err := employeeIncomeOthers(row, i.Other); err != nil {
		return fmt.Errorf("error retrieving other incomes: %q", err)
	}
	i.Total = grossIncome(*i)
	return nil
}

// employeeIncomeOthers will fetch other incomes info from the rows.
func employeeIncomeOthers(row *html.Node, o *d.Funds) error {
	if err := retrieveFloat(row, &o.PersonalBenefits, personalBenefits); err != nil {
		return fmt.Errorf("error retrieving personal benefits: %q", err)
	}
	if err := retrieveFloat(row, &o.EventualBenefits, eventualBenefits); err != nil {
		return fmt.Errorf("error retrieving eventual benefits: %q", err)
	}
	if err := retrieveFloat(row, &o.PositionOfTrust, positionOfTrust); err != nil {
		return fmt.Errorf("error retrieving position of trust: %q", err)
	}
	if err := retrieveFloat(row, &o.Gratification, gratification); err != nil {
		return fmt.Errorf("error retrieving gratification: %q", err)
	}
	if err := retrieveFloat(row, &o.OriginPosition, originPosition); err != nil {
		return fmt.Errorf("error retrieving origin position: %q", err)
	}
	return nil
}

// employeeDiscount will fetch discounts info from the row.
func employeeDiscounts(row *html.Node, d *d.Discount) error {
	if err := retrieveFloat(row, &d.PrevContribution, prevContribution); err != nil {
		return fmt.Errorf("error retrieving PrevContribution: %q", err)
	}
	if err := retrieveFloat(row, &d.CeilRetention, ceilRetention); err != nil {
		return fmt.Errorf("error retrieving ceilRetention: %q", err)
	}
	if err := retrieveFloat(row, &d.IncomeTax, incomeTax); err != nil {
		return fmt.Errorf("error retrieving incomeTax: %q", err)
	}
	var sundryV float64
	if err := retrieveFloat(row, &sundryV, sundry); err != nil {
		return fmt.Errorf("error retrieving incomeTax: %q", err)
	}
	d.Others = make(map[string]float64)
	d.Others["Sundry"] = sundryV
	d.Total = totalDiscounts(*d)
	return nil
}

// active returns a boolean representing if the employee is active or not.
func active(role string) bool {
	return role != "Inativo"
}

// grossIncome returns the sum of incomes.
func grossIncome(in d.IncomeDetails) float64 {
	o := *in.Other
	totalOthers := getValue(o.PersonalBenefits) + getValue(o.EventualBenefits) +
		getValue(o.PositionOfTrust) + getValue(o.Daily) + getValue(o.Gratification) + sumMapValues(o.Others)
	total := getValue(in.Wage) + in.Perks.Total + totalOthers
	return math.Round(total*100) / 100
}

// totalDiscounts returns the sum of discounts.
func totalDiscounts(d d.Discount) float64 {
	total := *d.PrevContribution + *d.CeilRetention + *d.IncomeTax + sumMapValues(d.Others)
	return math.Round(total*100) / 100
}
