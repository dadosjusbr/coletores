package coletores

import (
	"time"
)

// ExecutionResult collects the results of the whole dadosjusbr execution pipeline.
type ExecutionResult struct {
	Pr PackagingResult `json:"pr,omitempty"`
	Cr CrawlingResult  `json:"cr,omitempty"`
}

// ProcInfo stores information about a process execution.
//
// NOTE 1: It could be used by any process in the data consolidation pipeline (i.e. validation) and should not contain information specific to a step.
// NOTE 2: Due to storage restrictions, as of 04/2020, we are only going to store process information when there is a failure. That allow us to make the consolidation simpler by storing the full
// stdout, stderr and env instead of backing everything up and storing links.
type ProcInfo struct {
	Stdin      string   `json:"stdin" bson:"stdin,omitempty"`             // String containing the standard input of the process.
	Stdout     string   `json:"stdout" bson:"stdout,omitempty"`           // String containing the standard output of the process.
	Stderr     string   `json:"stderr" bson:"stderr,omitempty"`           // String containing the standard error of the process.
	Cmd        string   `json:"cmd" bson:"cmd,omitempty"`                 // Command that has been executed
	CmdDir     string   `json:"cmddir" bson:"cmdir,omitempty"`            // Local directory, in which the command has been executed
	ExitStatus int      `json:"status,omitempty" bson:"status,omitempty"` // Exit code of the process executed
	Env        []string `json:"env,omitempty" bson:"env,omitempty"`       // Copy of strings representing the environment variables in the form ke=value
}

// PackagingResult stores the result of the package step, which creates the datapackage.
type PackagingResult struct {
	ProcInfo ProcInfo `json:"procinfo,omitempty"` // Information about the process execution
	Package  string   `json:"package"`            // Local file path of the package created by the step
}

// Crawler keeps information about the crawler.
type Crawler struct {
	CrawlerID      string `json:"id" bson:"id,omitempty"`           // Convention: crawler the directory
	CrawlerVersion string `json:"version" bson:"version,omitempty"` // Convention: crawler commit id
}

// CrawlingResult stores the result of a crawler-parser ("coletor") run.
type CrawlingResult struct {
	AgencyID  string     `json:"aid"`
	Month     int        `json:"month"`
	Year      int        `json:"year"`
	Crawler   Crawler    `json:"crawler"`
	Files     []string   `json:"files"`
	Employees []Employee `json:"employees"`
	Timestamp time.Time  `json:"timestamp"`
	ProcInfo  ProcInfo   `json:"procinfo,omitempty"`
}

// Employee a Struct that reflets a employee snapshot, containing all relative data about a employee
type Employee struct {
	Reg       string         `json:"reg" bson:"reg,omitempty" tableheader:"reg" csv:"reg"` // Register number
	Name      string         `json:"name" bson:"name,omitempty" tableheader:"name" csv:"name"`
	Role      string         `json:"role" bson:"role,omitempty" tableheader:"role" csv:"role"`
	Type      string         `json:"type" bson:"type,omitempty" tableheader:"type" csv:"type"`                     // servidor, membro, pensionista or indefinido
	Workplace string         `json:"workplace" bson:"workplace,omitempty" tableheader:"workplace" csv:"workplace"` // 'Lotacao' Like '10° Zona eleitoral'
	Active    bool           `json:"active" bson:"active,omitempty" tableheader:"active" csv:"active"`             // 'Active' Or 'Inactive'
	Income    *IncomeDetails `json:"income" bson:"income,omitempty" csv:"-"`
	Discounts *Discount      `json:"discounts" bson:"discounts,omitempty" csv:"-"`
}

// IncomeDetails a Struct that details an employee's income.
type IncomeDetails struct {
	Total float64  `json:"total" bson:"total,omitempty" tableheader:"income_total" csv:"income_total"`
	Wage  *float64 `json:"wage" bson:"wage,omitempty" tableheader:"wage" csv:"wage"`
	Perks *Perks   `json:"perks" bson:"perks,omitempty" csv:"-"`
	Other *Funds   `json:"other" bson:"other,omitempty" csv:"-"` // other funds that make up the total income of the employee. further details explained below
}

// Perks a Struct that details perks that complements an employee's wage.
type Perks struct {
	Total           float64            `json:"total" bson:"total,omitempty" tableheader:"perks_total" csv:"perks_total"`
	Food            *float64           `json:"food" bson:"food,omitempty" tableheader:"perks_food" csv:"perks_food"` // Food Aid
	Transportation  *float64           `json:"transportation" bson:"transportation,omitempty" tableheader:"perks_transportation" csv:"perks_transportation"`
	PreSchool       *float64           `json:"pre_school" bson:"pre_school,omitempty" tableheader:"perks_pre_school" csv:"perks_pre_school"` // Assistance provided before the child enters school.
	Health          *float64           `json:"health" bson:"health,omitempty" tableheader:"perks_health" csv:"perks_health"`
	BirthAid        *float64           `json:"birth_aid" bson:"birth_aid,omitempty" tableheader:"perks_birth" csv:"perks_birth"`                     // 'Auxílio Natalidade'
	HousingAid      *float64           `json:"housing_aid" bson:"housing_aid,omitempty" tableheader:"perks_housing" csv:"perks_housing"`             // 'Auxílio Moradia'
	Subsistence     *float64           `json:"subsistence" bson:"subsistence,omitempty" tableheader:"perks_subsistence" csv:"perks_subsistence"`     // 'Ajuda de Custo'
	OtherPerksTotal *float64           `json:"others_total" bson:"others_total,omitempty" tableheader:"perks_others_total" csv:"perks_others_total"` // Total de outras ajudas (descritas no mapa Others)
	Others          map[string]float64 `json:"others" bson:"others,omitempty" csv:"-"`                                                               // Any other kind of perk that does not have a pattern among the Agencys.
}

// Funds a Struct that details that make up the employee income.
type Funds struct {
	Total            float64            `json:"total" bson:"total,omitempty" tableheader:"funds_total" csv:"funds_total"`
	PersonalBenefits *float64           `json:"personal_benefits" bson:"personal_benefits,omitempty" tableheader:"funds_personal_benefits" csv:"funds_personal_benefits"` // Permanent Allowance, VPI, Benefits adquired thought judicial demand and others personal.
	EventualBenefits *float64           `json:"eventual_benefits" bson:"eventual_benefits,omitempty" tableheader:"funds_eventual_benefits" csv:"funds_eventual_benefits"` // Holidays, Others Temporary Wage,  Christmas bonus and some others eventual.
	PositionOfTrust  *float64           `json:"trust_position" bson:"trust_position,omitempty" tableheader:"funds_trust_position" csv:"funds_trust_position"`             // Income given for the importance of the position held.
	Daily            *float64           `json:"daily" bson:"daily,omitempty" tableheader:"funds_daily" csv:"funds_daily"`                                                 // Employee reimbursement for eventual expenses when working in a different location than usual.
	Gratification    *float64           `json:"gratification" bson:"gratification,omitempty" tableheader:"funds_gratification" csv:"funds_gratification"`                 //
	OriginPosition   *float64           `json:"origin_pos" bson:"origin_pos,omitempty"  tableheader:"funds_origin_pos" csv:"funds_origin_pos"`                            // Wage received from other Agency, transfered employee.
	OtherFundsTotal  *float64           `json:"others_total" bson:"others_total,omitempty" tableheader:"funds_others_total" csv:"funds_others_total"`                     // Total of Any other kind of income that does not have a pattern among the Agencys.
	Others           map[string]float64 `json:"others" bson:"others,omitempty" csv:"-"`                                                                                   // Any other kind of income that does not have a pattern among the Agencys.
}

// Discount a Struct that details all discounts (represented as a non-negative number) that must be applied to the employee's income.
type Discount struct {
	Total               float64            `json:"total" bson:"total,omitempty" tableheader:"discounts_total" csv:"discounts_total"`
	PrevContribution    *float64           `json:"prev_contribution" bson:"prev_contribution,omitempty" tableheader:"discounts_prev_contribution" csv:"discount_prev_contribution"` // 'Contribuição Previdenciária'
	CeilRetention       *float64           `json:"ceil_retention" bson:"ceil_retention,omitempty" tableheader:"discounts_ceil_retention" csv:"discounts_ceil_retention"`            // 'Retenção de teto'
	IncomeTax           *float64           `json:"income_tax" bson:"income_tax,omitempty" tableheader:"discounts_income_tax" csv:"discounts_income_tax"`                            // 'Imposto de renda'
	OtherDiscountsTotal *float64           `json:"others_total" bson:"others_total,omitempty" tableheader:"discounts_others_total" csv:"discounts_others_total"`                    // Total of Any other kind of income that does not have a pattern among the Agencys.
	Others              map[string]float64 `json:"other" bson:"other,omitempty" csv:"-"`                                                                                            // Any other kind of discount that does not have a pattern among the Agencys.
}
