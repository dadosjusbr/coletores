package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"

	"github.com/dadosjusbr/coletores"
	"github.com/dadosjusbr/coletores/status"
	"github.com/dadosjusbr/storage"
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
	Pr coletores.PackagingResult
	Cr coletores.CrawlingResult
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
	var er executionResult
	erIN, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("error reading execution result: %v", err)))
	}
	if err = json.Unmarshal(erIN, &er); err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("error reading execution result: %v", err)))
	}

	agmi := storage.AgencyMonthlyInfo{
		AgencyID: er.Cr.AgencyID,
		Month:    er.Cr.Month,
		Year:     er.Cr.Year,
	}
	var packBackup *storage.Backup
	var backup []storage.Backup
	if er.Pr.Package != "" {
		packBackup, err = client.Cloud.UploadFile(er.Pr.Package)
		if err != nil {
			status.ExitFromError(status.NewError(2, fmt.Errorf("error trying to get Backup package files: %v, error: %v", er.Pr.Package, err)))
		}
		agmi.Package = packBackup
	}
	if er.Cr.Files != nil {
		backup, err = client.Cloud.Backup(er.Cr.Files)
		if err != nil {
			status.ExitFromError(status.NewError(2, fmt.Errorf("error trying to get Backup files: %v, error: %v", er.Cr.Files, err)))
		}
		agmi.Backups = backup
	}

	if er.Cr.ProcInfo.ExitStatus != 0 {
		agmi.ProcInfo = &er.Cr.ProcInfo
	} else {
		agmi.ProcInfo = &er.Pr.ProcInfo
	}

	if err = client.Store(agmi); err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("error trying to store agmi: %v", err)))
	}
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
