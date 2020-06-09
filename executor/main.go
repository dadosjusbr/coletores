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
	storeDirErr = "../store-error"
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

		// Collect Data
		mustBuild(job, commit, conf)
		er.Cr = mustExecDataCollector(job, commit, conf)

		// Package Data
		mustBuild(packagerDir, commit, conf)
		er.Pr = mustExecPackager(er, conf)

		// Store Data
		mustBuild(storeDir, commit, conf)
		mustExecStore(er, conf)
	}
	fmt.Println("Finished.")
}

func mustExecStore(er executionResult, conf config) {
	id := fmt.Sprintf("store-%d-%d", conf.Month, conf.Year)
	log.Printf("Executing %s ...\n", id)
	pi, err := execImage(storeDir, er, conf)
	if err != nil {
		log.Fatalf("Error executing %s: %q. ProcInfo:%+v", id, err, pi)
	}
	log.Printf("%s executed successfully\n", id)
}

func mustExecPackager(er executionResult, conf config) storage.PackagingResult {
	id := fmt.Sprintf("packager-%d-%d", conf.Month, conf.Year)
	log.Printf("Executing %s ...\n", id)
	pi, err := execImage(packagerDir, er, conf)
	if err != nil {
		log.Fatalf("Error executing %s: %q. ProcInfo:%+v", id, err, pi)
	}
	log.Printf("%s executed successfully\n", id)
	return storage.PackagingResult{Package: pi.Stdout}
}

func mustExecDataCollector(job, commit string, conf config) storage.CrawlingResult {
	id := fmt.Sprintf("%s-%d-%d", job, conf.Month, conf.Year)
	log.Printf("Executing %s ...\n", id)
	pi, err := execImage(job, executionResult{}, conf)
	if err != nil {
		log.Fatalf("Error executing DataCollector %s: %q. ProcInfo:%+v", id, err, pi)
	}
	cr, err := genCR(job, commit, pi, conf)
	if err != nil {
		log.Fatalf("Error trying to generate crawling result %s:%q", id, err)
	}
	log.Printf("%s executed successfully\n", id)
	return *cr
}

// tries to build a docker image for a job and panics if it can not suceed.
func mustBuild(job, commit string, conf config) {
	id := fmt.Sprintf("%s-%d-%d", job, conf.Month, conf.Year)
	log.Printf("Building image %s...\n", id)
	pi, err := buildImage(job, commit)
	if err != nil {
		log.Fatalf("Error building DataCollector image %s: %q", id, err)
	} else if status.Code(pi.ExitStatus) != status.OK {
		log.Fatalf("Status code %d(%s) building DataCollector image %s", pi.ExitStatus, status.Text(status.Code(pi.ExitStatus)), id)
	}
	log.Printf("Image %s build sucessfully\n", id)
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
		fmt.Sprintf("--mes=%d", conf.Month),
		fmt.Sprintf("--ano=%d", conf.Year),
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
