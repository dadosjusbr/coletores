package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/dadosjusbr/coletores/status"
	"github.com/dadosjusbr/storage"
	"github.com/joho/godotenv"
	"github.com/kelseyhightower/envconfig"
)

type config struct {
	CollectorDirList []string `envconfig:"COLLECTOR_DIR_LIST"`
	Month            int      `envconfig:"MONTH"`
	Year             int      `envconfig:"YEAR"`
}

type executionResult struct {
	Cr storage.CrawlingResult
	Pr storage.PackagingResult
}

const (
	packagerDir = "../packager"
	storeDir    = "../store"
	storeErrDir = "../store-error"
)

func main() {
	if err := godotenv.Load(); err != nil {
		status.ExitFromError(status.NewError(status.SystemError, fmt.Errorf("Error loading .env file")))
	}

	var conf config
	if err := envconfig.Process("", &conf); err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Error loading config values from .env: %v", err.Error())))
	}
	// Getting commit ID.
	commit := os.Getenv("GIT_COMMIT")
	if commit == "" {
		log.Fatalf("GIT_COMMIT env var can not be empty")
	}

	// Executing pipeline for jobs
	for _, job := range conf.CollectorDirList {
		var er executionResult
		var err error

		// Collect Data
		er.Cr.ProcInfo, err = Build(job, commit, conf)
		if err != nil {
			er.Cr.AgencyID = filepath.Base(job)
			//Store Error
			Build(storeErrDir, commit, conf)
			execStoreErr(er, conf)
			continue
		}
		er.Cr, err = execDataCollector(job, commit, conf)
		if err != nil {
			er.Cr.AgencyID = filepath.Base(job)
			//Store Error
			Build(storeErrDir, commit, conf)
			execStoreErr(er, conf)
			continue
		}

		// Package Data
		Build(packagerDir, commit, conf)
		if err != nil {
			//Store Error
			Build(storeErrDir, commit, conf)
			execStoreErr(er, conf)
			continue
		}
		er.Pr, err = execPackager(er, conf)
		if err != nil {
			//Store Error
			Build(storeErrDir, os.Getenv("GIT_COMMIT"), conf)
			execStoreErr(er, conf)
			continue
		}

		// Store Data
		Build(storeDir, commit, conf)
		execStore(er, conf)
	}
	fmt.Println("Finished.")
}

func execDataCollector(job, commit string, conf config) (storage.CrawlingResult, error) {
	id := fmt.Sprintf("%s-%d-%d", job, conf.Month, conf.Year)
	log.Printf("Executing %s ...\n", id)
	pi, err := execImage(job, executionResult{}, conf)
	if err != nil {
		return storage.CrawlingResult{ProcInfo: *pi}, err
	}
	cr, err := genCR(job, commit, pi, conf)
	if err != nil {
		return storage.CrawlingResult{ProcInfo: *pi}, fmt.Errorf("Error trying to generate crawling result %s:%q", id, err)
	}
	log.Printf("%s executed successfully\n", id)
	return *cr, nil
}

func execPackager(er executionResult, conf config) (storage.PackagingResult, error) {
	id := fmt.Sprintf("packager-%d-%d", conf.Month, conf.Year)
	log.Printf("Executing %s ...\n", id)
	pi, err := execImage(packagerDir, er, conf)
	if err != nil {
		return storage.PackagingResult{ProcInfo: *pi}, err
	}
	log.Printf("%s executed successfully\n", id)
	return storage.PackagingResult{Package: pi.Stdout}, nil
}

func execStore(er executionResult, conf config) {
	id := fmt.Sprintf("store-%d-%d", conf.Month, conf.Year)
	log.Printf("Executing %s ...\n", id)
	pi, err := execImage(storeDir, er, conf)
	if err != nil {
		log.Fatalf("Error executing %s: %q. ProcInfo:%+v", id, err, pi)
	}
	log.Printf("%s executed successfully\n", id)
}

func execStoreErr(er executionResult, conf config) {
	er.Cr.Month = conf.Month
	er.Cr.Year = conf.Year
	id := fmt.Sprintf("storeError-%d-%d", er.Cr.Month, er.Cr.Year)
	log.Printf("Executing %s ...\n", id)
	pi, err := execImage(storeErrDir, er, conf)
	if err != nil {
		log.Fatalf("Error executing %s: %q. ProcInfo:%+v", id, err, pi)
	}
	log.Printf("%s executed successfully\n", id)
	return
}

// Build tries to build a docker image for a job and panics if it can not suceed.
func Build(job, commit string, conf config) (storage.ProcInfo, error) {
	id := fmt.Sprintf("%s-%d-%d", job, conf.Month, conf.Year)
	log.Printf("Building image %s...\n", id)
	pi, err := buildImage(job, commit)
	if err != nil {
		return *pi, fmt.Errorf("Error building DataCollector image %s: %q", id, err)
	} else if status.Code(pi.ExitStatus) != status.OK {
		return *pi, fmt.Errorf("Status code %d(%s) building DataCollector image %s", pi.ExitStatus, status.Text(status.Code(pi.ExitStatus)), id)
	}
	log.Printf("Image %s build sucessfully\n", id)
	return *pi, nil
}

// build runs a go build for each path. It will also insert the value of main.gitCommit in the binaries.
func buildImage(dir, commit string) (*storage.ProcInfo, error) {
	cmdList := strings.Split(fmt.Sprintf("docker build --build-arg GIT_COMMIT=%s -t %s .", commit, filepath.Base(dir)), " ")
	cmd := exec.Command(cmdList[0], cmdList[1:]...)
	cmd.Dir = dir
	var outb, errb bytes.Buffer
	cmd.Stdout = &outb
	cmd.Stderr = &errb
	err := cmd.Run()
	exitStatus := statusCode(err)
	procInfo := storage.ProcInfo{
		Stdout:     string(outb.Bytes()),
		Stderr:     string(errb.Bytes()),
		Cmd:        strings.Join(cmdList, " "),
		CmdDir:     dir,
		ExitStatus: exitStatus,
		Env:        os.Environ(),
	}
	return &procInfo, err
}

// execImage executes the image designed and returns it's stdin, stdout and exit error if any.
func execImage(dir string, er executionResult, conf config) (*storage.ProcInfo, error) {
	erJSON, err := json.Marshal(er)
	if err != nil {
		return nil, fmt.Errorf("Error trying to marshal er %s", erJSON)
	}
	cmdList := []string{
		"run",
		"-i",
		"-v", "dadosjusbr:/output",
		"--rm",
		filepath.Base(dir),
	}
	cmd := exec.Command("docker", cmdList...)
	cmd.Dir = dir
	cmd.Stdin = strings.NewReader(string(erJSON))
	var outb, errb bytes.Buffer
	cmd.Stdout = &outb
	cmd.Stderr = &errb
	err = cmd.Run()
	exitStatus := statusCode(err)
	procInfo := storage.ProcInfo{
		Stdin:      string(erJSON),
		Stdout:     string(outb.Bytes()),
		Stderr:     string(errb.Bytes()),
		Cmd:        strings.Join(cmdList, " "),
		CmdDir:     cmd.Dir,
		ExitStatus: exitStatus,
		Env:        os.Environ(),
	}
	return &procInfo, err
}

// genCR creates a crawling result
func genCR(job, commit string, pi *storage.ProcInfo, conf config) (*storage.CrawlingResult, error) {
	var cr storage.CrawlingResult
	if status.Code(pi.ExitStatus) != status.OK {
		crawlerInfo := storage.Crawler{
			CrawlerID:      strings.Split(job, "/")[1],
			CrawlerVersion: commit,
		}
		cr = storage.CrawlingResult{
			AgencyID:  strings.Split(job, "/")[1],
			Month:     conf.Month,
			Year:      conf.Year,
			Crawler:   crawlerInfo,
			Timestamp: time.Now(),
			ProcInfo:  *pi,
		}
		return &cr, nil
	}
	if err := json.Unmarshal([]byte(pi.Stdout), &cr); err != nil {
		return nil, fmt.Errorf("error trying to unmarshal crawling result: %q", err)
	}
	return &cr, nil
}

// statusCode returns the exit code returned for the cmd execution.
// 0 if no error.
// -1 if process was terminated by a signal or hasn't started.
// -2 if error is not an ExitError.
func statusCode(err error) int {
	if err == nil {
		return 0
	}
	if exitError, ok := err.(*exec.ExitError); ok {
		return exitError.ExitCode()
	}
	return -2
}
