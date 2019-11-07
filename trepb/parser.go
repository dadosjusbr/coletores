package main

import (
	"fmt"
	"os"
	d "trepb/datastructures"

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
	table, err := loadTable(month, year)
	if err != nil {
		return nil, fmt.Errorf("error while loading data table: %q", err)
	}

	e, err := employeeRecords(table)
	if err != nil {
		return nil, fmt.Errorf("error while loading data table: %q", err)
	}

	return e, nil
}

// loadTable will load a table of a specific month and year that should be in the output/ directory
func loadTable(month, year int) (*html.Node, error) {
	fileName := fmt.Sprintf("./output/remuneracoes-trepb-%02d-%04d.html", month, year)
	f, err := os.Open(fileName)
	if err != nil {
		return nil, fmt.Errorf("error opening file (%s): %q", fileName, err)
	}

	doc, err := htmlquery.Parse(f)
	if err != nil {
		return nil, fmt.Errorf("error parsing file html tree (%s): %q", fileName, err)
	}

	table, err := htmlquery.Query(doc, `//*[@id="tblDetalhamentoFolhaPagamentoPessoal"]`)
	if err != nil {
		return nil, fmt.Errorf("error finding data table in file (%s): %q", fileName, err)
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
	var e d.Employee
	if err := employeeBasicInfo(row, &e); err != nil {
		return e, fmt.Errorf("error retrieving employee basic info: %q", err)
	}
	if err := employeeIncome(row, &e.Income); err != nil {
		return e, fmt.Errorf("error retrieving employee income info: %q", err)
	}
	if err := employeeDiscounts(row, &e.Discounts); err != nil {
		return e, fmt.Errorf("error retrieving employee discounts info: %q", err)
	}
	e.GrossIncome = grossIncome(e.Income)
	e.TotalDiscounts = totalDiscounts(e.Discounts)
	e.NetIncome = netIncome(e)
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
func employeeIncome(row *html.Node, i *d.Income) error {
	if err := retrieveFloat(row, &i.Wage, wage); err != nil {
		return fmt.Errorf("error retrieving Wage: %q", err)
	}
	if err := retrieveFloat(row, &i.Perks, perks); err != nil {
		return fmt.Errorf("error retrieving perks: %q", err)
	}
	if err := employeeIncomeOthers(row, &i.Other); err != nil {
		return fmt.Errorf("error retrieving other incomes: %q", err)
	}
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
	if err := retrieveFloat(row, &d.Sundry, sundry); err != nil {
		return fmt.Errorf("error retrieving sundry: %q", err)
	}
	return nil
}

// active returns a boolean representing if the employee is active or not.
func active(role string) bool {
	return role != "Inativo"
}

// grossIncome returns the sum of incomes.
func grossIncome(in d.Income) float64 {
	o := in.Other
	// Not accounted: Origin Position
	totalOthers := o.PersonalBenefits + o.EventualBenefits +
		o.PositionOfTrust + o.Daily + o.Gratification + o.Others
	return in.Wage + in.Perks + totalOthers
}

// totalDiscounts returns the sum of discounts.
func totalDiscounts(d d.Discount) float64 {
	return d.PrevContribution + d.CeilRetention + d.IncomeTax + d.Sundry
}

// netIncome returns the net income for the employee.
func netIncome(e d.Employee) float64 {
	return e.GrossIncome - e.TotalDiscounts
}
