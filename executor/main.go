package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"sync"
	"time"

	"github.com/dadosjusbr/coletores/status"
	"github.com/dadosjusbr/storage"
	"github.com/joho/godotenv"
	"github.com/kelseyhightower/envconfig"
)

type config struct {
	OutputFolder string   `envconfig:"OUTPUT_FOLDER"`
	JobList      []string `envconfig:"JOB_LIST"`
	Month        int
	Year         int
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
	var err error
	if err := godotenv.Load(); err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("Error loading .env file")))
	}
	if err := envconfig.Process("", &c); err != nil {
		status.ExitFromError(status.NewError(4, fmt.Errorf("Error loading config values from .env: %v", err.Error())))
	}
	if c.OutputFolder, err = filepath.Abs(c.OutputFolder); err != nil {
		status.ExitFromError(status.NewError(2, fmt.Errorf("Error trying to get absolute path for output folder: %v", err.Error())))
	}
	if err := os.Mkdir(c.OutputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		status.ExitFromError(status.NewError(2, fmt.Errorf("Error creating output folder(%s): %v", c.OutputFolder, err)))
	}
	fmt.Printf("%v\n", c)
}

func main() {

	commit, err := getGitCommit()
	if err != nil {
		status.ExitFromError(status.NewError(4, fmt.Errorf("Error gettint git commig %s", err)))
	}
	log("Starting do build package")
	procInfo, err := buildDockerImage("../packager", commit)
	if err != nil {
		testPack, _ := json.Marshal(&procInfo)
		fmt.Fprintf(os.Stderr, "%s", string(testPack))
		status.ExitFromError(status.NewError(2, fmt.Errorf("Error trying to build package image %s", err)))
	}
	log("Package Builded")
	log("Starting do build store")
	procInfoStore, err := buildDockerImage("../store", commit)
	if err != nil {
		testStore, _ := json.Marshal(&procInfoStore)
		fmt.Fprintf(os.Stderr, "%s", string(testStore))
		status.ExitFromError(status.NewError(2, fmt.Errorf("Error trying to build package image %s", err)))
	}
	log("Store Builded")

	var wg sync.WaitGroup
	wg.Add(len(c.JobList))
	for _, job := range c.JobList {
		go func(job string) {
			defer wg.Done()
			//Collect Data
			log("Starting to build Data Collect image for %s", job)
			procInfo, err := buildDockerImage(job, commit)
			if err != nil {
				status.ExitFromError(status.NewError(2, fmt.Errorf("Build error %s: %v", job, err)))
			} else {
				procInfo, err = execDataCollector(job, c.Month, c.Year)
				if err != nil {
					status.ExitFromError(status.NewError(2, fmt.Errorf("Execution error %s-%d-%d: %v", job, c.Month, c.Year, err)))
				}
			}
			log(" -- Data collector executed for %s --\n", job)
			cr, err := genCR(job, procInfo, commit, c.Month, c.Year)
			if err != nil {
				status.ExitFromError(status.NewError(4, fmt.Errorf("Error trying to generate crawling result %s", err)))
			}
			// Package Data
			pckResult, err := execPack(*cr)
			if err != nil {
				status.ExitFromError(status.NewError(4, fmt.Errorf("Execution error %s-%d-%d: %v", job, c.Month, c.Year, err)))
			}
			log(" -- Package executed for %s --\n", job)
			execResult := executionResult{Pr: *pckResult, Cr: *cr}
			// Store Data
			_, err = execStore(execResult)
			if err != nil {
				status.ExitFromError(status.NewError(4, fmt.Errorf("Store error: %v", err)))
				return
			}
			log(" -- Store executed for %s --\n", job)
			return
		}(job)
	}
	wg.Wait()
	fmt.Println("Finished.")
}

// getGitCommit returns the last git commit for the local repository.
func getGitCommit() (string, error) {
	cmd := exec.Command("git", "rev-list", "-1", "HEAD")
	stdout, err := cmd.CombinedOutput()
	if err != nil {
		return "", fmt.Errorf("getGitCommit() error: %s", err)
	}
	return string(stdout[:len(stdout)-1]), nil
}

// build runs a go build for each path. It will also insert the value of main.gitCommit in the binaries.
func buildDockerImage(dir, commit string) (storage.ProcInfo, error) {
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
	return procInfo, err
}

// execDataCollector executes the data collector located in path and returns it's stdin, stdout and exit error if any.
func execDataCollector(dir string, month, year int) (storage.ProcInfo, error) {
	outPath := fmt.Sprintf("OUTPUT_FOLDER=%s/%s", c.OutputFolder, filepath.Base(dir))
	cmdList := strings.Split(fmt.Sprintf(`docker run -v dadosjusbr:/output --rm -e %s --env-file=.env %s --mes=%d --ano=%d`, outPath, filepath.Base(dir), month, year), " ")
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
	return procInfo, err
}

// execPack executes the data collector located in path and returns it's stdin, stdout and exit error if any.
func execPack(cr storage.CrawlingResult) (*storage.PackagingResult, error) {
	outPath := fmt.Sprintf("OUTPUT_FOLDER=%s", c.OutputFolder)

	cmdList := strings.Split(fmt.Sprintf(`docker run -e %s -i -v dadosjusbr:/output --rm packager`, outPath), " ")
	cmd := exec.Command(cmdList[0], cmdList[1:]...)
	crJSON, err := json.Marshal(cr)
	if err != nil {
		return nil, fmt.Errorf("Error trying to marshal cr %s", crJSON)
	}
	cmd.Stdin = strings.NewReader(string(crJSON))
	var outb, errb bytes.Buffer
	cmd.Stdout = &outb
	cmd.Stderr = &errb
	err = cmd.Run()
	exitStatus := statusCode(err)
	procInfo := storage.ProcInfo{
		Stdout:     string(outb.Bytes()),
		Stderr:     string(errb.Bytes()),
		Cmd:        strings.Join(cmdList, " "),
		CmdDir:     cmd.Dir,
		ExitStatus: exitStatus,
		Env:        os.Environ(),
	}
	PckResult := storage.PackagingResult{
		ProcInfo: procInfo,
		Package:  procInfo.Stdout,
	}
	return &PckResult, err
}

// execPack executes the data collector located in path and returns it's stdin, stdout and exit error if any.
func execStore(er executionResult) (*storage.ProcInfo, error) {
	outPath := fmt.Sprintf("OUTPUT_FOLDER=%s", c.OutputFolder)
	mgoURI := fmt.Sprintf("MONGODB_URI=%s", c.MongoURI)
	dbName := fmt.Sprintf("MONGODB_DBNAME=%s", c.DBName)
	miCol := fmt.Sprintf("MONGODB_MICOL=%s", c.MongoMICol)
	agCol := fmt.Sprintf("MONGODB_AGCOL=%s", c.MongoAgCol)
	swftUser := fmt.Sprintf("SWIFT_USERNAME=%s", c.SwiftUsername)
	swftKey := fmt.Sprintf("SWIFT_APIKEY=%s", c.SwiftAPIKey)
	swftAuth := fmt.Sprintf("SWIFT_AUTHURL=%s", c.SwiftAuthURL)
	swftDmn := fmt.Sprintf("SWIFT_DOMAIN=%s", c.SwiftDomain)
	swftCtnr := fmt.Sprintf("SWIFT_CONTAINER=%s", c.SwiftContainer)
	cmdList := strings.Split(fmt.Sprintf(`docker run -e %s -e %s -e %s -e %s -e %s -e %s -e %s -e %s -e %s -e %s -i -v dadosjusbr:/output --rm store`, outPath, mgoURI, dbName, miCol, agCol, swftUser, swftKey, swftAuth, swftDmn, swftCtnr), " ")
	cmd := exec.Command(cmdList[0], cmdList[1:]...)
	erJSON, err := json.Marshal(er)
	if err != nil {
		return nil, fmt.Errorf("Error trying to marshal er %s", erJSON)
	}
	cmd.Stdin = strings.NewReader(string(erJSON))
	var outb, errb bytes.Buffer
	cmd.Stdout = &outb
	cmd.Stderr = &errb
	err = cmd.Run()
	exitStatus := statusCode(err)
	procInfo := storage.ProcInfo{
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
func genCR(job string, procInfo storage.ProcInfo, commit string, month, year int) (*storage.CrawlingResult, error) {
	var cr storage.CrawlingResult
	if procInfo.ExitStatus == 1 {
		crawlerInfo := storage.Crawler{
			CrawlerID:      strings.Split(job, "/")[1],
			CrawlerVersion: commit,
		}
		cr = storage.CrawlingResult{
			AgencyID:  strings.Split(job, "/")[1],
			Month:     month,
			Year:      year,
			Crawler:   crawlerInfo,
			Timestamp: time.Now(),
			ProcInfo:  procInfo,
		}
		return &cr, nil
	}
	if err := json.Unmarshal([]byte(procInfo.Stdout), &cr); err != nil {
		return nil, fmt.Errorf("error trying to unmarshal crawling result: %q", err)
	}
	cr.ProcInfo = procInfo
	return &cr, nil
}

// log prints to Stdout
func log(format string, args ...interface{}) {
	time := fmt.Sprintf("%s: ", time.Now().Format(time.RFC3339))
	fmt.Fprintf(os.Stdout, time+format+"\n", args...)
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
