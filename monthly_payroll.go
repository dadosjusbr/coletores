package coletores

import (
	"fmt"
	"os"

	"github.com/dadosjusbr/storage"
	"github.com/gocarina/gocsv"
)

// MonthlyPayrollItem represents each employee on the payroll.
type MonthlyPayrollItem struct {
	AgencyID string `tableheader:"aid" tableheader:"aid" csv:"aid"`
	Month    int    `tableheader:"month" csv:"month"`
	Year     int    `tableheader:"year" tableheader:"year" csv:"year"`
	storage.Employee
}

// MonthlyPayroll stores the data about the payroll of a certain agency.
type MonthlyPayroll []MonthlyPayrollItem

// NewMonthlyPayroll instantiates a MonthlyPayroll
func NewMonthlyPayroll(aid string, month, year int, emps []storage.Employee) MonthlyPayroll {
	var p MonthlyPayroll
	for _, e := range emps {
		p = append(p, MonthlyPayrollItem{
			Employee: e,
			AgencyID: aid,
			Month:    month,
			Year:     year,
		})
	}
	return p
}

// ToCSVFile dumps the payroll into a file using the CSV format.
func (m *MonthlyPayroll) ToCSVFile(path string) error {
	f, err := os.Create(path)
	if err != nil {
		return fmt.Errorf("Error creating CSV file(%s):%q", path, err)
	}
	defer f.Close()
	return gocsv.MarshalFile(m, f)
}
