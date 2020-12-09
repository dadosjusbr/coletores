package main

type tjbaEmployee struct {
	Reg                 int     `json:"matricula"`
	Name                string  `json:"nome"`
	Workplace           string  `json:"lotacao"`
	Role                string  `json:"cargo"`
	Active              string  `json:"status"`
	Type                string  `json:"tipoServidor"`
	Wage                float64 `json:"valorParadigma"`
	PersonalBenefits    float64 `json:"valorVantagemPessoal"`
	PositionOfTrust     float64 `json:"valorComissao"`
	PerksTotal          float64 `json:"valorIndenizacao"`
	EventualBenefits    float64 `json:"valorVantagemEventual"`
	IncomeTotal         float64 `json:"totalCredito"`
	PrevContribution    float64 `json:"valorPrevidencia"`
	IncomeTax           float64 `json:"valorIR"`
	OtherDiscountsTotal float64 `json:"valorDescontoDiverso"`
	CeilRetention       float64 `json:"valorRetencaoTeto"`
	DiscountTotal       float64 `json:"totalDebito"`
	FundsTotal          float64 `json:"valorLiquido"`
	OriginPosition      float64 `json:"valorRemuneracaoOrigem"`
	Daily               float64 `json:"valorDiaria"`
	Gratification       float64 `json:"valorGratificacao"`
}
