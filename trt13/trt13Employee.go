package main

type trt13Employee struct {
	Reg            string        `json:"matricula"`
	Name           string        `json:"nome"`
	Workplace      string        `json:"lotacao"`
	Role           string        `json:"cargo"`
	Income         trt13Income   `json:"rendimentos"`
	Discount       trt13Discount `json:"descontos"`
	OriginPosition float64       `json:"remuneracaoOrgaoOrigem"`
	Daily          float64       `json:"diarias"`
}

type trt13Income struct {
	Wage             float64 `json:"remuneracaoParadigma"`
	PersonalBenefits float64 `json:"vantagensPessoais"`
	EventualBenefits float64 `json:"vantagensEventuais"`
	Subsidio         float64 `json:"subsidio"`
	Gratification    float64 `json:"gratificacao"`
	Perks            float64 `json:"indenizacoes"`
}

type trt13Discount struct {
	PrevContribution float64 `json:"previdenciaPublica"`
	IncomeTax        float64 `json:"impostoRenda"`
	Sundry           float64 `json:"descontosDiversos"`
	CeilRetantion    float64 `json:"retencaoTeto"`
}
