package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
	"os"

	"github.com/dadosjusbr/coletores"
	"github.com/dadosjusbr/coletores/status"
	"github.com/dadosjusbr/storage"
	"github.com/kelseyhightower/envconfig"
)

type config struct {
	MongoURI   string `envconfig:"MONGODB_URI" required:"true"`
	DBName     string `envconfig:"MONGODB_DBNAME" required:"true"`
	MongoMICol string `envconfig:"MONGODB_MICOL" required:"true"`
	MongoAgCol string `envconfig:"MONGODB_AGCOL" required:"true"`
	// Swift Conf
	SwiftUsername  string `envconfig:"SWIFT_USERNAME" required:"true"`
	SwiftAPIKey    string `envconfig:"SWIFT_APIKEY" required:"true"`
	SwiftAuthURL   string `envconfig:"SWIFT_AUTHURL" required:"true"`
	SwiftDomain    string `envconfig:"SWIFT_DOMAIN" required:"true"`
	SwiftContainer string `envconfig:"SWIFT_CONTAINER" required:"true"`
}

func main() {
	var c config
	if err := envconfig.Process("", &c); err != nil {
		status.ExitFromError(status.NewError(4, fmt.Errorf("Error loading config values from .env: %v", err.Error())))
	}

	client, err := newClient(c)
	if err != nil {
		status.ExitFromError(status.NewError(3, fmt.Errorf("newClient() error: %s", err)))
	}
	var er coletores.ExecutionResult
	erIN, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("error reading execution result: %v", err)))
	}
	if err = json.Unmarshal(erIN, &er); err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("error reading execution result: %v", err)))
	}

	// Package.
	if er.Pr.Package == "" {
		status.ExitFromError(status.NewError(status.InvalidInput, fmt.Errorf("there is no package to store. PackageResult:%+v", er.Pr)))
	}
	packBackup, err := client.Cloud.UploadFile(er.Pr.Package, er.Cr.AgencyID)
	if err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("error trying to get Backup package files: %v, error: %v", er.Pr.Package, err)))
	}

	// Backup.
	if len(er.Cr.Files) == 0 {
		status.ExitFromError(status.NewError(2, fmt.Errorf("no backup files found: CrawlingResult:%+v", er.Cr)))
	}
	backup, err := client.Cloud.Backup(er.Cr.Files, er.Cr.AgencyID)
	if err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("error trying to get Backup files: %v, error: %v", er.Cr.Files, err)))
	}
	agmi := storage.AgencyMonthlyInfo{
		AgencyID:          er.Cr.AgencyID,
		Month:             er.Cr.Month,
		Year:              er.Cr.Year,
		Crawler:           er.Cr.Crawler,
		Summary:           summary(er.Cr.Employees),
		Backups:           backup,
		CrawlingTimestamp: er.Cr.Timestamp,
		Package:           packBackup,
	}
	if er.Cr.ProcInfo.ExitStatus != 0 {
		agmi.ProcInfo = &er.Cr.ProcInfo
	}
	if err = client.Store(agmi); err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("error trying to store agmi: %v", err)))
	}
	fmt.Println("Store Executed...")
}

// newClient Creates client to connect with DB and Cloud5
func newClient(conf config) (*storage.Client, error) {
	db, err := storage.NewDBClient(conf.MongoURI, conf.DBName, conf.MongoMICol, conf.MongoAgCol)
	if err != nil {
		return nil, fmt.Errorf("error creating DB client: %q", err)
	}
	db.Collection(conf.MongoMICol)
	bc := storage.NewCloudClient(conf.SwiftUsername, conf.SwiftAPIKey, conf.SwiftAuthURL, conf.SwiftDomain, conf.SwiftContainer)
	client, err := storage.NewClient(db, bc)
	if err != nil {
		return nil, fmt.Errorf("error creating storage.client: %q", err)
	}
	return client, nil
}

// summary aux func to make all necessary calculations to DataSummary Struct
func summary(employees []coletores.Employee) storage.Summaries {
	general := storage.Summary{}
	memberActive := storage.Summary{}
	for _, emp := range employees {
		// checking if the employee instance has the required data to build the summary
		switch {
		case emp.Income == nil:
			status.ExitFromError(status.NewError(status.InvalidInput, fmt.Errorf("employee %+v is invalid. It does not have 'income' field", emp)))
		case emp.Income.Wage == nil:
			status.ExitFromError(status.NewError(status.InvalidInput, fmt.Errorf("employee %+v is invalid. It does not have 'income.wage' field", emp)))
		case emp.Type == nil:
			status.ExitFromError(status.NewError(status.InvalidInput, fmt.Errorf("employee %+v is invalid. It does not have 'type' field", emp)))
		}
		updateSummary(&general, emp)
		// NOTE: Keeping this condition because we are not updating all colletors to consider only members.
		// We will do the latter on demmand.
		if *emp.Type == "membro" && emp.Active {
			updateSummary(&memberActive, emp)
		}
	}
	if general.Count == 0 {
		return storage.Summaries{}
	}
	return storage.Summaries{
		General:      general,
		MemberActive: memberActive,
	}
}

//updateSummary auxiliary function that updates the summary data at each employee value
func updateSummary(s *storage.Summary, emp coletores.Employee) {
	updateData := func(d *storage.DataSummary, value float64, count int) {
		if count == 1 {
			d.Min = value
			d.Max = value
		} else {
			d.Min = math.Min(d.Min, value)
			d.Max = math.Max(d.Max, value)
		}
		d.Total += value
		d.Average = d.Total / float64(count)
	}

	// Income histogram.
	s.Count++
	salary := emp.Income.Total
	var salaryRange int
	if salary <= 10000 {
		salaryRange = 10000
	} else if salary <= 20000 {
		salaryRange = 20000
	} else if salary <= 30000 {
		salaryRange = 30000
	} else if salary <= 40000 {
		salaryRange = 40000
	} else if salary <= 50000 {
		salaryRange = 50000
	} else {
		salaryRange = -1 // -1 is maker when the salary is over 50000
	}
	s.IncomeHistogram[salaryRange]++

	updateData(&s.Wage, *emp.Income.Wage, s.Count)
	// There are employees with no perks.
	if emp.Income.Perks != nil {
		updateData(&s.Perks, emp.Income.Perks.Total, s.Count)
	}
	if emp.Income.Other != nil {
		updateData(&s.Others, emp.Income.Other.Total, s.Count)
	}
}
