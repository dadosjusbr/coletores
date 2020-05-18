package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"time"

	"github.com/dadosjusbr/storage"
	"github.com/joho/godotenv"
	"github.com/kelseyhightower/envconfig"
)

type config struct {
	Month int
	Year  int
	// MONGO CONF
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

var c config

func init() {
	if err := godotenv.Load(); err != nil {
		logError("Error loading .env file")
		os.Exit(1)
	}
	if err := envconfig.Process("", &c); err != nil {
		logError("Error loading config values from .env: %q", err.Error())
		os.Exit(1)
	}
	fmt.Printf("%v\n", c)
}

func main() {
	client, err := newClient()
	if err != nil {
		logError("newClient() error: %s", err)
		os.Exit(1)
	}
	var er executionResult
	erIN, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		logError("error reading execution result: %q", err)
		os.Exit(1)
	}
	err = json.Unmarshal(erIN, &er)
	if err != nil {
		logError("error getting execution result: %q", err)
		os.Exit(1)
	}
	summary := summary(er.Cr.Employees)
	packBackup := 
	backup, err := client.Bc.Backup(er.Cr.Files)
	if err != nil {
		logError("error trying to get Backup files: %v, error: %q", er.Cr.Files, err)
		os.Exit(1)
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
	}
	if er.Cr.ProcInfo.ExitStatus != 0 {
		agmi.ProcInfo = &er.Cr.ProcInfo
	}

	err = client.Store(agmi)
	if err != nil {
		logError("error trying to store agmi: %q", err)
		os.Exit(1)
	}
	fmt.Println("Store Executed...")
}

// fatalError prints to Stderr
func logError(format string, args ...interface{}) {
	time := fmt.Sprintf("%s: ", time.Now().Format(time.RFC3339))
	fmt.Fprintf(os.Stderr, time+format+"\n", args...)
}

// log prints to Stdout
func log(format string, args ...interface{}) {
	time := fmt.Sprintf("%s: ", time.Now().Format(time.RFC3339))
	fmt.Fprintf(os.Stdout, time+format+"\n", args...)
}

// newClient Creates client to connect with DB and Cloud5
func newClient() (*storage.Client, error) {
	db, err := storage.NewDBClient(c.MongoURI, c.DBName, c.MongoMICol, c.MongoAgCol)
	if err != nil {
		return nil, fmt.Errorf("error creating DB client: %q", err)
	}
	db.Collection(c.MongoMICol)
	bc := storage.NewBackupClient(c.SwiftUsername, c.SwiftAPIKey, c.SwiftAuthURL, c.SwiftDomain, c.SwiftContainer)
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
