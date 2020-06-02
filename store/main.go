package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
	"os"

	"github.com/dadosjusbr/coletores/status"
	"github.com/dadosjusbr/storage"
	"github.com/joho/godotenv"
	"github.com/kelseyhightower/envconfig"
)

type config struct {
	MongoURI   string `envconfig:"MONGODB_URI"`
	DBName     string `envconfig:"MONGODB_DBNAME"`
	MongoMICol string `envconfig:"MONGODB_MICOL"`
	MongoAgCol string `envconfig:"MONGODB_AGCOL"`
	// Swift Conf
	SwiftUsername  string `envconfig:"SWIFT_USERNAME"`
	SwiftAPIKey    string `envconfig:"SWIFT_APIKEY"`
	SwiftAuthURL   string `envconfig:"SWIFT_AUTHURL"`
	SwiftDomain    string `envconfig:"SWIFT_DOMAIN"`
	SwiftContainer string `envconfig:"SWIFT_CONTAINER"`
}

type executionResult struct {
	Pr storage.PackagingResult
	Cr storage.CrawlingResult
}

func main() {
	if err := godotenv.Load(); err != nil {
		status.ExitFromError(status.NewError(4, fmt.Errorf("Eror .env to read.")))
	}
	var c config
	if err := envconfig.Process("", &c); err != nil {
		status.ExitFromError(status.NewError(4, fmt.Errorf("Error loading config values from .env: %v", err.Error())))
	}

	client, err := newClient(c)
	if err != nil {
		status.ExitFromError(status.NewError(3, fmt.Errorf("newClient() error: %s", err)))
	}
	var er executionResult
	erIN, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("error reading execution result: %v", err)))
	}
	if err = json.Unmarshal(erIN, &er); err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("error reading execution result: %v", err)))
	}

	summary := summary(er.Cr.Employees)
	packBackup, err := client.Cloud.UploadFile(er.Pr.Package)
	if err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("error trying to get Backup package files: %v, error: %v", er.Pr.Package, err)))
	}
	backup, err := client.Cloud.Backup(er.Cr.Files)
	if err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("error trying to get Backup files: %v, error: %v", er.Cr.Files, err)))
	}
	agmi := storage.AgencyMonthlyInfo{
		AgencyID:          er.Cr.AgencyID,
		Month:             er.Cr.Month,
		Year:              er.Cr.Year,
		Crawler:           er.Cr.Crawler,
		Employee:          er.Cr.Employees,
		Summary:           summary,
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
func summary(Employees []storage.Employee) storage.Summaries {
	general := storage.Summary{}
	memberActive := storage.Summary{}
	memberInactive := storage.Summary{}
	servantActive := storage.Summary{}
	servantInactive := storage.Summary{}
	for _, emp := range Employees {
		updateSummary(&general, emp)
		switch {
		case emp.Type == "membro" && emp.Active:
			updateSummary(&memberActive, emp)
		case emp.Type == "membro" && !emp.Active:
			updateSummary(&memberInactive, emp)
		case emp.Type == "servidor" && emp.Active:
			updateSummary(&servantActive, emp)
		case emp.Type == "servidor" && !emp.Active:
			updateSummary(&servantInactive, emp)
		}
	}
	if general.Count == 0 {
		return storage.Summaries{}
	}
	return storage.Summaries{
		General:         general,
		MemberActive:    memberActive,
		MemberInactive:  memberInactive,
		ServantActive:   servantActive,
		ServantInactive: servantInactive,
	}
}

//updateSummary auxiliary function that updates the summary data at each employee value
func updateSummary(s *storage.Summary, emp storage.Employee) {
	s.Count++
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
	updateData(&s.Wage, *emp.Income.Wage, s.Count)
	updateData(&s.Perks, emp.Income.Perks.Total, s.Count)
	updateData(&s.Others, emp.Income.Other.Total, s.Count)
}
