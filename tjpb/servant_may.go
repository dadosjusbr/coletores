package main

import (
	"bytes"
	"encoding/csv"
	"fmt"
	"math"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/dadosjusbr/storage"
)

var headersMap = map[string]int{
	"NOME":                           0,
	"CARGO":                          1,
	"LOTAÇÃO":                        2,
	"REMUNERAÇÃO PARADIGMA":          3,
	"VANTAGENS PESSOAIS":             4,
	"FUNÇÃO DE CONFIANÇA":            5,
	"INDENIZAÇÕES":                   6,
	"VANTAGENS EVENTUAIS":            7,
	"GRATIFICACOES":                  8,
	"TOTAL CREDITOS":                 9,
	"PREVIDENCIA PUBLICA":            10,
	"IMPOSTO DE RENDA":               11,
	"DESCONTOS DIVERSOS":             12,
	"RETENÇÃO":                       13,
	"TOTAL DEBITOS":                  14,
	"RENDIMENTO LIQUIDO":             15,
	"REMUNERACAO DO ORGAO DE ORIGEM": 16,
	"DIARIAS":                        17,
}

func parserServerMay(path string) ([]storage.Employee, error) {
	templateArea := []string{"92.085,16.838,559.351,102.083",
		"93.137,102.083,541.46,211.532",
		"94.19,209.428,547.774,824.029",
		"94.19,360.973,548.827,818.767"}
	var csvByte [][]byte
	var csvFinal [][]string
	for i, templ := range templateArea {
		//This cmd execute a tabula script(https://github.com/tabulapdf/tabula-java)
		//where tmpl is the template area, which corresponds to the coordinates (x1,2,y1,2) of
		//one or more columns in the table.
		cmdList := strings.Split(fmt.Sprintf(`java -jar tabula-1.0.3-jar-with-dependencies.jar -t -a %v -p all %v`, templ, filepath.Base(path)), " ")
		cmd := exec.Command(cmdList[0], cmdList[1:]...)
		var outb, errb bytes.Buffer
		cmd.Stdout = &outb
		cmd.Stderr = &errb
		cmd.Run()
		csvByte = append(csvByte, outb.Bytes())
		reader := csv.NewReader(&outb)
		rows, err := reader.ReadAll()
		if err != nil {
			//TODO CHECK ERROR
			os.Exit(1)
		}
		if i == 2 {
			rows = treatDoubleLines(rows)
		}
		if i == 3 {
			rows = fixNumberColumns(rows)
		}
		csvFinal = appendCSVColumns(csvFinal, rows)
	}
	employees, err := genEmpSlice(csvFinal)
	if err != nil {
		return []storage.Employee{}, fmt.Errorf("Error generating  Employee slice %v", err)
	}
	file, err := os.Create(strings.Replace(filepath.Base(path), ".pdf", ".csv", 1))
	if err != nil {
		logError("Error creating csv: %q", err)
	}
	defer file.Close()
	writer := csv.NewWriter(file)
	defer writer.Flush()
	writer.WriteAll(csvFinal)
	return employees, nil
}

func genEmpSlice(empCSV [][]string) ([]storage.Employee, error) {
	var empSet []storage.Employee
	var err error
	for i := range empCSV {
		var emp = storage.Employee{}
		emp.Name = empCSV[i][0]
		emp.Role = empCSV[i][1]
		emp.Type = "servidor"
		emp.Workplace = empCSV[i][2]
		emp.Active = employeeActive(empCSV[i][1])
		emp.Income, err = employeeIncome(empCSV[i])
		if err != nil {
			return []storage.Employee{}, fmt.Errorf("Error generating income of Employee slice %v", err)
		}
		emp.Discounts, err = employeeDiscountInfo(empCSV[i])
		if err != nil {
			return []storage.Employee{}, fmt.Errorf("Error generating Discounts of Employee slice %v", err)
		}
		empSet = append(empSet, emp)
	}
	return empSet, nil
}

func employeeDiscountInfo(emp []string) (*storage.Discount, error) {
	var d storage.Discount
	if err := retrieveFloat64(&d.PrevContribution, emp, 10); err != nil {
		return nil, fmt.Errorf("error retrieving discounts(regNum: %s): %q", emp[0], err)
	}
	if err := retrieveFloat64(&d.CeilRetention, emp, 13); err != nil {
		return nil, fmt.Errorf("error retrieving discounts(regNum: %s): %q", emp[0], err)
	}
	if err := retrieveFloat64(&d.IncomeTax, emp, 11); err != nil {
		return nil, fmt.Errorf("error retrieving discounts(regNum: %s): %q", emp[0], err)
	}
	if err := retrieveFloat64(&d.Total, emp, 14); err != nil {
		return nil, fmt.Errorf("error retrieving discounts(regNum: %s): %q", emp[0], err)
	}
	var diversos float64
	if err := retrieveFloat64(&diversos, emp, 12); err != nil {
		return nil, fmt.Errorf("error retrieving discounts(regNum: %s): %q", emp[0], err)
	}
	d.Others = map[string]float64{"Descontos Diversos": diversos}
	return &d, nil
}

func retrieveFloat64(v interface{}, emp []string, key int) error {
	var err error
	var value float64
	valueStr := emp[key]
	if valueStr == "" {
		value = 0.0
	} else {
		value, err = parseFloat(valueStr)
		if err != nil {
			return fmt.Errorf("error retrieving float %v from %v: %v", key, emp, err)
		}
	}
	if v, ok := v.(**float64); ok {
		*v = &value
		return nil
	}
	if v, ok := v.(*float64); ok {
		*v = value
		return nil
	}
	return fmt.Errorf("error retrieving float %v: %v must be *float64 or **float64", key, emp)
}

// parseFloat makes the string with format "xx.xx,xx" able to be parsed by the strconv.ParseFloat and return it parsed.
func parseFloat(s string) (float64, error) {
	s = strings.Trim(s, " ")
	s = strings.Replace(s, ",", ".", 1)
	if n := strings.Count(s, "."); n > 1 {
		s = strings.Replace(s, ".", "", n-1)
	}
	return strconv.ParseFloat(s, 64)
}

// getValue takes a list of float64 pointers and returns it's sum, 0 if nil
func getFloat64Value(pointers ...*float64) float64 {
	var total float64
	for _, p := range pointers {
		if p == nil {
			total += 0
			continue
		}
		total += *p
	}
	return math.Round(total*100) / 100.0
}

func employeeActive(cargo string) bool {
	return (strings.Contains(cargo, "Inativos") || strings.Contains(cargo, "aposentados")) == false
}

func employeeIncome(emp []string) (*storage.IncomeDetails, error) {
	var err error
	var in storage.IncomeDetails
	if err = retrieveFloat64(&in.Wage, emp, 3); err != nil {
		return nil, fmt.Errorf("error retrieving employee income info: %q", err)
	}
	if in.Perks, err = employeePerks(emp); err != nil {
		return nil, fmt.Errorf("error retrieving employee perks: %q", err)
	}
	if in.Other, err = employeeIncomeFunds(emp); err != nil {
		return nil, fmt.Errorf("error retrieving employee funds: %q", err)
	}
	in.Total = totalIncome(in)
	return &in, nil
}

func employeePerks(emp []string) (*storage.Perks, error) {
	var inPerks storage.Perks

	if err := retrieveFloat64(&inPerks.Total, emp, 6); err != nil {
		return nil, fmt.Errorf("error retrieving perks(regNum: %s): %q", emp[0], err)
	}
	return &inPerks, nil
}

func employeeIncomeFunds(emp []string) (*storage.Funds, error) {
	var o storage.Funds
	if err := retrieveFloat64(&o.PositionOfTrust, emp, 5); err != nil {
		return nil, fmt.Errorf("error retrieving funds(regNum: %s): %q", emp[0], err)
	}
	if err := retrieveFloat64(&o.PersonalBenefits, emp, 4); err != nil {
		return nil, fmt.Errorf("error retrieving funds(regNum: %s): %q", emp[0], err)
	}
	if err := retrieveFloat64(&o.EventualBenefits, emp, 7); err != nil {
		return nil, fmt.Errorf("error retrieving funds(regNum: %s): %q", emp[0], err)
	}
	if err := retrieveFloat64(&o.Gratification, emp, 8); err != nil {
		return nil, fmt.Errorf("error retrieving funds(regNum: %s): %q", emp[0], err)
	}
	if err := retrieveFloat64(&o.OriginPosition, emp, 16); err != nil {
		return nil, fmt.Errorf("error retrieving funds(regNum: %s): %q", emp[0], err)
	}
	if err := retrieveFloat64(&o.Daily, emp, 17); err != nil {
		return nil, fmt.Errorf("error retrieving funds(regNum: %s): %q", emp[0], err)
	}
	o.Total = *o.PositionOfTrust + *o.EventualBenefits + *o.Gratification + *o.PersonalBenefits + *o.Daily + *o.OriginPosition
	return &o, nil
}

func totalIncome(in storage.IncomeDetails) float64 {
	total := getFloat64Value(in.Wage)
	if in.Other != nil {
		total += in.Other.Total
	}
	if in.Perks != nil {
		total += in.Perks.Total
	}
	return math.Round(total*100) / 100
}
