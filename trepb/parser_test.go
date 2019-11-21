package main

import (
	"bytes"
	"reflect"
	"strings"
	"testing"

	"github.com/antchfx/htmlquery"
	"github.com/dadosjusbr/storage"
	"github.com/stretchr/testify/assert"
	"golang.org/x/net/html"
)

const tableSample = `<table id="tblDetalhamentoFolhaPagamentoPessoal">
	<tr class="fundo0">
		<td class="c01">Zulmira De Jesus Guimaraes Mendes     </td>
		<td class="c03 capitalize">inativo </td>
		<td class="c02">Inativo </td>
		<td class="c04" nowrap="" title="Remuneração paradigma">16.902,00 </td>
		<td class="c05" nowrap="" title="Vantagens pessoais">7.475,71 </td>
		<td class="c17" nowrap="" title="Subsídios, FC e CJ">5.990,88 </td>
		<td class="c06" nowrap="" title="Indenizações">0,00 </td>
		<td class="c07" nowrap="" title="Vantagens eventuais">0,00 </td>
		<td class="c08" nowrap="" title="Gratificações">0,00 </td>
		<td class="c09" nowrap="" title="Total de créditos">30.368,59 </td>
		<td class="c10" nowrap="" title="Previdência pública">-2.719,50 </td>
		<td class="c11" nowrap="" title="Imposto de renda">-6.158,41 </td>
		<td class="c12" nowrap="" title="Descontos diversos">0,00 </td>
		<td class="c13" nowrap="" title="Retenção pelo teto constitucional">0,00 </td>
		<td class="c14" nowrap="" title="Total de débitos">-8.877,91 </td>
		<td class="c15" nowrap="" title="Rendimento líquido">21.490,68 </td>
		<td class="c16" nowrap="" title="Remuneração de origem">0,00 </td>
		<!-- <td class="c17" nowrap title="Diárias"                          >0,00 </td>-->	 
	</tr>
</table>`

//Retrieve a row for testing purposes
func row() (*html.Node, error) {
	doc, err := htmlquery.Parse(strings.NewReader(tableSample))
	if err != nil {
		return nil, err
	}
	row, err := htmlquery.Query(doc, "//tr")
	if row != nil || err != nil {
		return row, err
	}
	return nil, nil
}

// expectedEmployee auxiliary function to create the expected employee struct.
func expectedEmployee() storage.Employee {
	zero := 0.0
	pb := 7475.71
	pt := 5990.88
	expectedOthers := storage.Funds{Total: 13466.59, PersonalBenefits: &pb, EventualBenefits: &zero, PositionOfTrust: &pt, Gratification: &zero, OriginPosition: &zero}
	expectedPerks := storage.Perks{Total: 0}

	wg := 16902.0
	expectedIncome := storage.IncomeDetails{Total: 30368.59, Wage: &wg, Perks: &expectedPerks, Other: &expectedOthers}

	prev := 2719.5
	it := 6158.41
	others := make(map[string]float64)
	others["Sundry"] = 0
	expectedDiscount := storage.Discount{Total: 8877.91, PrevContribution: &prev, CeilRetention: &zero, IncomeTax: &it, Others: others}
	expected := storage.Employee{Name: "Zulmira De Jesus Guimaraes Mendes", Role: "Inativo", Workplace: "inativo", Active: false, Income: &expectedIncome,
		Discounts: &expectedDiscount}
	return expected
}

// Test if newEmployee is creating a new employee from a row with correct information.
func Test_newEmployee(t *testing.T) {
	row, err := row()
	assert.NoError(t, err)
	assert.NotNil(t, row)

	e, err := newEmployee(row)

	assert.NoError(t, err)
	assert.Equal(t, expectedEmployee(), e)
}

func Test_totalDiscounts(t *testing.T) {
	row, err := row()
	assert.NoError(t, err)
	assert.NotNil(t, row)

	assert.Equal(t, 8877.91, totalDiscounts(*expectedEmployee().Discounts))
}

func Test_totalIncome(t *testing.T) {
	row, err := row()
	assert.NoError(t, err)
	assert.NotNil(t, row)

	assert.Equal(t, 30368.59, totalIncome(*expectedEmployee().Income))
}

// Test if employeeIncome is collecting correct information from the row.
func Test_employeeIncome(t *testing.T) {
	row, err := row()
	assert.NoError(t, err)
	assert.NotNil(t, row)

	var i = storage.IncomeDetails{Perks: &storage.Perks{}, Other: &storage.Funds{}}
	assert.NoError(t, employeeIncome(row, &i))
	assert.Equal(t, *expectedEmployee().Income, i)
}

// Test if employeeIncomeOthers is collecting correct information from the row.
func Test_employeeIncomeOthers(t *testing.T) {
	row, err := row()
	assert.NoError(t, err)
	assert.NotNil(t, row)

	var o = storage.Funds{}
	assert.NoError(t, employeeIncomeOthers(row, &o))
	assert.Equal(t, *expectedEmployee().Income.Other, o)
}

// Test if employeeBasicInfo is collecting correct information from the row.
func Test_employeeBasicInfo(t *testing.T) {
	row, err := row()
	assert.NoError(t, err)
	assert.NotNil(t, row)

	var e = storage.Employee{}
	assert.NoError(t, employeeBasicInfo(row, &e))
	assert.Equal(t, storage.Employee{Name: "Zulmira De Jesus Guimaraes Mendes", Role: "Inativo", Workplace: "inativo", Active: false}, e)
}

// Test if employeeDiscounts is collecting correct information from the row.
func Test_employeeDiscounts(t *testing.T) {
	row, err := row()
	assert.NoError(t, err)
	assert.NotNil(t, row)

	var d = storage.Discount{}
	assert.NoError(t, employeeDiscounts(row, &d))
	assert.Equal(t, *expectedEmployee().Discounts, d)
}

// Test if loadTable is loading the correct html table from reader.
func Test_loadTable(t *testing.T) {
	tests := []struct {
		name    string
		arg     string // Will be transformed in reader
		wantErr bool
	}{
		{"Table present", `<table id="tblDetalhamentoFolhaPagamentoPessoal"></table>`, false},
		{"Wrong table present", "<table></table>", true},
		{"No table", "", true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := loadTable(strings.NewReader(tt.arg))
			if err != nil {
				if tt.wantErr {
					return
				}
				t.Errorf("loadTable() error = %v, wantErr %v", err, tt.wantErr)
			}

			var gotBuf bytes.Buffer
			err = html.Render(&gotBuf, got)
			assert.NoError(t, err)

			if !reflect.DeepEqual(gotBuf.String(), tt.arg) {
				t.Errorf("loadTable() = %v, want %v", gotBuf.String(), tt.arg)
			}

		})
	}
}
