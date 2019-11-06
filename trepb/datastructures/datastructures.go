package datastructures

// Employee employee
type Employee struct {
	Reg            string // Register number
	Name           string
	Role           string
	Type           string  // servidor, membro or pensionista
	Workplace      string  // 'Lotacao' Like '10° Zona eleitoral'
	Active         bool    // 'Active' Or 'Inactive'
	GrossIncome    float64 // Income received without discounts applied.
	TotalDiscounts float64 // Discounts to be applied in Gross Income
	NetIncome      float64 // Final income received after discounts applied
	Income         Income  //
	Discounts      Discount
}

// Income income
type Income struct {
	Wage  float64
	Perks float64
	Other Funds // other funds that make up the total income of the employee. further details explained below
}

// Funds funds
type Funds struct {
	PersonalBenefits float64 // Permanent Allowance, VPI, Benefits adquired thought judicial demand and others personal.
	EventualBenefits float64 // Holidays, Others Temporary Wage,  Christmas bonus and some others eventual.
	PositionOfTrust  float64 // Income given for the importance of the position held.
	Daily            float64 // Employee reimbursement for eventual expenses when working in a different location than usual.
	Gratification    float64 //
	OriginPosition   float64 // Wage received from other Agency, transfered employee.
	Others           float64 // Any other kind of income that does not have a pattern among the Agencys.
}

// Discount discount
type Discount struct {
	PrevContribution float64 // 'Contribuição Previdenciária'
	CeilRetention    float64 // 'Retenção de teto'
	IncomeTax        float64 // 'Imposto de renda'
	Sundry           float64 // 'Diversos'
}

// StorageInfo info
type StorageInfo struct {
	File         []byte
	FileName     string
	RetrieveDate string
	FileHash     string
}
