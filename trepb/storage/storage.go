package storage

import "time"

// Agency Struct containing the main descriptions of each Agency.
type Agency struct {
	ID        interface{} `json:"id" bson:"_id,omitempty"`
	ShortName string      `json:"short_name" bson:"short_name,omitempty"` // 'trt13'
	Name      string      `json:"name" bson:"name,omitempty"`             // 'Tribunal Regional do Trabalho 13° Região'
	Type      string      `json:"type" bson:"type,omitempty"`             // "R" for Regional, "M" for Municipal, "F" for Federal, "E" for State.
	Entity    string      `json:"entity" bson:"entity,omitempty"`         // "J" For Judiciário, "M" for Ministério Público, "P" for Procuradorias and "D" for Defensorias.
	UF        string      `json:"uf" bson:"uf,omitempty"`                 // Short code for federative unity.
}

// AgencyMonthlyInfo Struct containing a snapshot of a agency in a month.
type AgencyMonthlyInfo struct {
	AgencyID string     `json:"id" bson:"_id,omitempty"`
	Storage  []Metadata `json:"storage" bson:"storage,omitempty"`
	Month    int        `json:"month" bson:"month,omitempty"`
	Year     int        `json:"year" bson:"year,omitempty"`
	Summary  Summary    `json:"sumarry" bson:"summary,omitempty"`
	Employee []Employee `json:"employee" bson:"employee,omitempty"`
	Metadata Metadata   `json:"metadata" bson:"metadata,omitempty"`
}

// Metadata Struct containing metadatas about crawler commit
type Metadata struct {
	Timestamp      time.Time `json:"metadata" bson:"metadata,omitempty"`     // Time the crawler sent it
	CrawlerID      string    `json:"crawl_id" bson:"crawl_id,omitempty"`     // The directory of the collector's crawler
	CrawlerVersion string    `json:"crawl_vers" bson:"crawl_vers,omitempty"` // Last Commit of the repository
}

// FileBackup Struct containing URL to download a file and a hash to track if in the future will be changes in the file.
type FileBackup struct {
	URL  string `json:"url" bson:"url,omitempty"`
	Hash string `json:"hash" bson:"hash,omitempty"`
}

// Summary Struct containing summarized  information about a agency/month stats
type Summary struct {
	Count  int         `json:"count" bson:"count,omitempty"`   // Number of employees
	Wage   DataSummary `json:"wage" bson:"wage,omitempty"`     //  Statistics (Max, Min, Median, Total)
	Perks  DataSummary `json:"perks" bson:"perks,omitempty"`   //  Statistics (Max, Min, Median, Total)
	Others DataSummary `json:"others" bson:"others,omitempty"` //  Statistics (Max, Min, Median, Total)
}

// DataSummary Summary with statistics.
type DataSummary struct {
	Max   float64 `json:"max" bson:"max,omitempty"`
	Min   float64 `json:"min" bson:"min,omitempty"`
	Mean  float64 `json:"mean" bson:"mean,omitempty"`
	Total float64 `json:"total" bson:"total,omitempty"`
}

// Employee Struct that reflets a employee snapshot, containing all relative data about a employee
type Employee struct {
	Reg       string         `json:"reg,omitempty" bson:"reg,omitempty"` // Register number
	Name      string         `json:"name,omitempty" bson:"name,omitempty"`
	Role      string         `json:"role,omitempty" bson:"role,omitempty"`
	Type      string         `json:"type,omitempty" bson:"type,omitempty"`           // servidor, membro, pensionista or indefinido
	Workplace string         `json:"workplace,omitempty" bson:"workplace,omitempty"` // 'Lotacao' Like '10° Zona eleitoral'
	Active    bool           `json:"active,omitempty" bson:"active,omitempty"`       // 'Active' Or 'Inactive'
	Income    *IncomeDetails `json:"income,omitempty" bson:"income,omitempty"`
	Discounts *Discount      `json:"discounts,omitempty" bson:"discounts,omitempty"`
}

// IncomeDetails Struct that details an employee's income.
type IncomeDetails struct {
	Total float64  `json:"total" bson:"total,omitempty"`
	Wage  *float64 `json:"wage,omitempty" bson:"wage,omitempty"`
	Perks *Perks   `json:"perks" bson:"perks,omitempty"`
	Other *Funds   `json:"other" bson:"other,omitempty"` // other funds that make up the total income of the employee. further details explained below
}

// Perks Struct that details perks that complements an employee's wage.
type Perks struct {
	Total         float64            `json:"total" bson:"total,omitempty"`
	Food          *float64           `json:"food,omitempty" bson:"food,omitempty"` // Food Aid
	Tranportation *float64           `json:"transportation,omitempty" bson:"transportation,omitempty"`
	PreSchool     *float64           `json:"pre_school,omitempty" bson:"pre_school,omitempty"` // Assistance provided before the child enters school.
	Health        *float64           `json:"health,omitempty" bson:"health,omitempty"`
	BirthAid      *float64           `json:"birth_aid,omitempty" bson:"birth_aid,omitempty"`     // 'Auxílio Natalidade'
	HousingAid    *float64           `json:"housing_aid,omitempty" bson:"housing_aid,omitempty"` // 'Auxílio Moradia'
	Subsistence   *float64           `json:"subsistence,omitempty" bson:"subsistence,omitempty"` // 'Ajuda de Custo'
	Others        map[string]float64 `json:"others,omitempty" bson:"others,omitempty"`           // Any other kind of perk that does not have a pattern among the Agencys.
}

// Funds Struct that details that make up the employee income.
type Funds struct {
	Total            float64            `json:"total" bson:"total,omitempty"`
	PersonalBenefits *float64           `json:"person_benefits,omitempty" bson:"person_benefits,omitempty"`     // Permanent Allowance, VPI, Benefits adquired thought judicial demand and others personal.
	EventualBenefits *float64           `json:"eventual_benefits,omitempty" bson:"eventual_benefits,omitempty"` // Holidays, Others Temporary Wage,  Christmas bonus and some others eventual.
	PositionOfTrust  *float64           `json:"trust_position,omitempty" bson:"trust_position,omitempty"`       // Income given for the importance of the position held.
	Daily            *float64           `json:"daily,omitempty" bson:"daily,omitempty"`                         // Employee reimbursement for eventual expenses when working in a different location than usual.
	Gratification    *float64           `json:"gratific,omitempty" bson:"gratific,omitempty"`                   //
	OriginPosition   *float64           `json:"origin_pos,omitempty" bson:"origin_pos,omitempty"`               // Wage received from other Agency, transfered employee.
	Others           map[string]float64 `json:"others,omitempty" bson:"others,omitempty"`                       // Any other kind of income that does not have a pattern among the Agencys.
}

// Discount Struct that details all discounts that must be applied to the employee's income.
type Discount struct {
	Total            float64            `json:"total" bson:"total,omitempty"`
	PrevContribution *float64           `json:"prev_contribution,omitempty" bson:"prev_contribution,omitempty"` // 'Contribuição Previdenciária'
	CeilRetention    *float64           `json:"ceil_retention,omitempty" bson:"ceil_retention,omitempty"`       // 'Retenção de teto'
	IncomeTax        *float64           `json:"income_tax,omitempty" bson:"income_tax,omitempty"`               // 'Imposto de renda'
	Others           map[string]float64 `json:"sundry,omitempty" bson:"sundry,omitempty"`                       // 'Diversos'
}
