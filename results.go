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
	Type      *string        `json:"type" bson:"type,omitempty" tableheader:"type" csv:"type"`                     // servidor, membro, pensionista or indefinido
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
//  Confused? Our Dictonary:
// 	Name           |       Pt-BR             | Description | About
//  Perks          | 'Indenizações'         | Is the amount of compensation or reparation for acts that result in damages to the employee | https://www.jusbrasil.com.br/topicos/290794/indenizacao
//	Food           | 'Auxílio Alimentação'  | Purpose of subsidizing meal expenses.  | https://www.progpe.ufscar.br/servicos/adicionais-auxilios-e-beneficios-1/auxilio-alimentacao
//	Vacations      | 'Férias Indenizadas'   | Equivalent to the period not taken when terminating an employment contract, or those not taken during the term of the contract. | http://www.guiatrabalhista.com.br/guia/ferias-indenizadas.htm
//	Transportation | 'Auxílio Transporte'   | Intended to partially cover the expenses incurred with municipal, intercity or interstate public transportation in the travels made by the employee of his residence to the workplace and vice versa. | https://progep.ufes.br/manual-servidor/auxilio-transporte
//	PreSchool      | 'Auxílio Creche        | Assistance provided before the child enters school | https://viacarreira.com/auxilio-creche/
//	Health         | 'Auxílio Saúde'        | Partial reimbursement of the amount spent by the employee, active or inactive, and their dependents or pensioners with private health care plans.  | https://ww2.uft.edu.br/index.php/progedep/acesso-rapido/servicos/15928-auxilio-saude
//	BirthAid       | 'Auxílio Natalidade'   | Granted for the reason of the birth of a child in an amount equivalent to the lowest salary of the public service.     |  https://progep.ufes.br/aux%C3%ADlio-natalidade
//	HousingAid     | 'Auxílio Moradia'| Reimbursement of expenses incurred with renting a house or with accommodation managed by a hotel company, to a Employee who has undergone a change of address due to appointment to a management position or a trust function. |  http://portal2.trtrio.gov.br:7777/pls/portal/PORTAL.wwv_media.show?p_id=14107300&p_settingssetid=381905&p_settingssiteid=73&p_siteid=73&p_type=basetext&p_textid=14107301
//	Subsistence    | 'Ajuda de Custo' | Paid only once or eventually, to cover travel expenses incurred by him, such as: transfer expenses, monitoring of internal or external customers a professional events etc. |  https://www.arabello.com.br/ajuda-de-custo-a-funcionario-uso-transporte-proprio/#:~:text=Ajuda%20de%20custo%20%C3%A9%20o,externos%20a%20eventos%20profissionais%20etc.
//	CompensatoryLeave  | 'Licença Compensatória' | 'Compensation to the server for any acquired right.' | http://ampern.org.br/pgj-defere-requerimento-da-ampern-e-altera-a-resolucao-que-disciplina-a-licenca-compensatoria
//	Pecuniary      | 'Pecunia' | 'payment of any advantage or right of the public servant' | https://www.acheconcursos.com.br/artigos/o-que-e-pecunia-45290
//	VacationPecuniary | 'Pecunia de férias' | 'It consists of exchanging a few days of the vacation period for receiving an extra amount. | https://anape.org.br/site/wp-content/uploads/2014/01/004_046_Raimilan_Seneterri_da_Silva_Rodrigues_11082009-23h36m.pdf
//	FurnitureTransport | 'Transporte Mobiliário' | 'Amount related to the payment of the transportation of the employee's furniture in case of change' |
//	PremiumLicensePecuniary | 'Licença Prêmio'  | award to the assiduous and disciplined public employee, guaranteeing him the right to leave the public service for a period, without reducing his wages. | 'https://juridicocerto.com/p/zereshenrique/artigos/conversao-de-licenca-premio-em-pecunia-1675'
type Perks struct {
	Total                   float64  `json:"total" bson:"total,omitempty" tableheader:"perks_total" csv:"perks_total"`
	Food                    *float64 `json:"food" bson:"food,omitempty" tableheader:"perks_food" csv:"perks_food"`                                                                                     // Food Aid
	Vacations               *float64 `json:"vacation" bson:"vacation,omitempty" tableheader:"perks_vacation" csv:"perks_vacation"`                                                                     // Férias Indenizatórias - Vacation perk
	Transportation          *float64 `json:"transportation" bson:"transportation,omitempty" tableheader:"perks_transportation" csv:"perks_transportation"`                                             // 'Auxílio Transporte'.
	PreSchool               *float64 `json:"pre_school" bson:"pre_school,omitempty" tableheader:"perks_pre_school" csv:"perks_pre_school"`                                                             // Assistance provided before the child enters school.
	Health                  *float64 `json:"health" bson:"health,omitempty" tableheader:"perks_health" csv:"perks_health"`                                                                             // 'Auxílio Saúde'
	BirthAid                *float64 `json:"birth_aid" bson:"birth_aid,omitempty" tableheader:"perks_birth" csv:"perks_birth"`                                                                         // 'Auxílio Natalidade'
	HousingAid              *float64 `json:"housing_aid" bson:"housing_aid,omitempty" tableheader:"perks_housing" csv:"perks_housing"`                                                                 // 'Auxílio Moradia'
	Subsistence             *float64 `json:"subsistence" bson:"subsistence,omitempty" tableheader:"perks_subsistence" csv:"perks_subsistence"`                                                         // 'Ajuda de Custo'
	CompensatoryLeave       *float64 `json:"compensatory_leave" bson:"compensatory_leave,omitempty" tableheader:"perks_compensatory_leave" csv:"perks_compensatory_leave"`                             // 'Licença Compensatória'
	Pecuniary               *float64 `json:"pecuniary" bson:"pecuniary,omitempty" tableheader:"perks_pecuniary" csv:"perks_pecuniary"`                                                                 // 'Pecunia'
	VacationPecuniary       *float64 `json:"vacation_pecuniary" bson:"vacation_pecuniary,omitempty" tableheader:"perks_vacation_pecuniary" csv:"perks_vacation_pecuniary"`                             // 'Pecunia de férias'
	FurnitureTransport      *float64 `json:"furniture_transport" bson:"furniture_transport,omitempty" tableheader:"perks_furniture_transport" csv:"perks_furniture_transport"`                         // 'Transporte Mobiliário'
	PremiumLicensePecuniary *float64 `json:"premium_license_pecuniary" bson:"premium_license_pecuniary,omitempty" tableheader:"perks_premium_license_pecuniary" csv:"perks_premium_license_pecuniary"` // 'Licença prêmio em pecúnia (Geralmente as que nao foram gozadas, passam pros sucessores)'
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

// Discount a Struct that details all discounts that must be applied to the employee's income.
type Discount struct {
	Total               float64            `json:"total" bson:"total,omitempty" tableheader:"discounts_total" csv:"discounts_total"`
	PrevContribution    *float64           `json:"prev_contribution" bson:"prev_contribution,omitempty" tableheader:"discounts_prev_contribution" csv:"discount_prev_contribution"` // 'Contribuição Previdenciária'
	CeilRetention       *float64           `json:"ceil_retention" bson:"ceil_retention,omitempty" tableheader:"discounts_ceil_retention" csv:"discounts_ceil_retention"`            // 'Retenção de teto'
	IncomeTax           *float64           `json:"income_tax" bson:"income_tax,omitempty" tableheader:"discounts_income_tax" csv:"discounts_income_tax"`                            // 'Imposto de renda'
	OtherDiscountsTotal *float64           `json:"others_total" bson:"others_total,omitempty" tableheader:"discounts_others_total" csv:"discounts_others_total"`                    // Total of Any other kind of income that does not have a pattern among the Agencys.
	Others              map[string]float64 `json:"other" bson:"other,omitempty" csv:"-"`                                                                                            // Any other kind of discount that does not have a pattern among the Agencys.
}
