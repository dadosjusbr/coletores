package coletores

import (
	"time"

	"github.com/dadosjusbr/storage"
)

// ExecutionResult collects the results of the whole dadosjusbr execution pipeline.
type ExecutionResult struct {
	Pr storage.PackagingResult `json:"pr,omitempty"`
	Cr storage.CrawlingResult  `json:"cr,omitempty"`
}

// PackagingResult stores the result of the package step, which creates the datapackage.
type PackagingResult struct {
	ProcInfo storage.ProcInfo `json:"procinfo,omitempty"` // Information about the process execution
	Package  string           `json:"package"`            // Local file path of the package created by the step
}

// CrawlingResult stores the result of a crawler-parser ("coletor") run.
type CrawlingResult struct {
	AgencyID  string             `json:"aid"`
	Month     int                `json:"month"`
	Year      int                `json:"year"`
	Crawler   storage.Crawler    `json:"crawler"`
	Files     []string           `json:"files"`
	Employees []storage.Employee `json:"employees"`
	Timestamp time.Time          `json:"timestamp"`
	ProcInfo  storage.ProcInfo   `json:"procinfo,omitempty"`
}
