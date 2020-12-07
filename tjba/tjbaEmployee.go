package main

type tjbaEmployee struct {
	Reg                   int     `json:"matricula"`
	Name                  string  `json:"nome"`
	Workplace             string  `json:"lotacao"`
	Role                  string  `json:"cargo"`
	Status                string  `json:"status"`
	EmployeeType          string  `json:"tipoServidor"`
	Wage                  float64 `json:"valorParadigma"` // ?
	PersonalBenefitsValue float64 `json:"valorVantagemPessoal"`
	ComissionValue        float64 `json:"valorComissao"`
	PerksValue            float64 `json:"valorIndenizacao"`
	EventualBenefitsValue float64 `json:"valorVantagemEventual"`
	CreditTotal           float64 `json:"totalCredito"`
	PrevContribution      float64 `json:"valorPrevidencia"`
	IncomeTax             float64 `json:"valorIR"`
	Sundry                float64 `json:"valorDescontoDiverso"`
	RetantionValue        float64 `json:"valorRetencaoTeto"`
	DebtTotal             float64 `json:"totalDebito"`
	Value                 float64 `json:"valorLiquido"`
	WageOriginValue       float64 `json:"valorRemuneracaoOrigem"`
	Daily                 float64 `json:"valorDiaria"`
	Gratification         float64 `json:"valorGratificacao"`
}
