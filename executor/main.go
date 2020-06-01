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
}

type executionResult struct {
	Pr storage.PackagingResult
	Cr storage.CrawlingResult
}

var c config

func init() {
	var err error
	if err := godotenv.Load("envFiles/.env"); err != nil {
		status.ExitFromError(status.NewError(status.SystemError, fmt.Errorf("Error loading .env file")))
	}
	if err := envconfig.Process("", &c); err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Error loading config values from .env: %v", err.Error())))
	}
	if c.OutputFolder, err = filepath.Abs(c.OutputFolder); err != nil {
		status.ExitFromError(status.NewError(status.SystemError, fmt.Errorf("Error trying to get absolute path for output folder: %v", err.Error())))
	}
	if err := os.Mkdir(c.OutputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		status.ExitFromError(status.NewError(status.SystemError, fmt.Errorf("Error creating output folder(%s): %v", c.OutputFolder, err)))
	}
	fmt.Printf("%v\n", c)
}

func main() {
	commit, err := getGitCommit()
	if err != nil {
		status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Error gettint git commig %s", err)))
	}
	var wg sync.WaitGroup
	wg.Add(len(c.JobList))
	for _, job := range c.JobList {
		defer wg.Done()
		//Collect Data
		var er executionResult
		log("Starting to build DataCollector image for %s", job)
		procInfo, err := buildDockerImage(job, commit)
		log("DataCollector image builded for %s", job)
		if err != nil {
			status.ExitFromError(status.NewError(status.SystemError, fmt.Errorf("Build error %s: %v", job, err)))
		} else {
			log("Starting to exec DataCollector image for %s", job)
			procInfo, err = execImage(job, er)
			if err != nil {
				status.ExitFromError(status.NewError(status.SystemError, fmt.Errorf("Execution error %s-%d-%d: %v", job, c.Month, c.Year, err)))
			}
		}
		log(" -- Data collector executed for %s --\n", job)
		cr, err := genCR(job, procInfo, commit, c.Month, c.Year)
		if err != nil {
			status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Error trying to generate crawling result %s", err)))
		}
		er.Cr = *cr
		// Package Data
		log("Starting to build Packager step ...")
		procInfo, err = buildDockerImage("../packager", commit)
		if err != nil {
			testPack, err := json.Marshal(&procInfo)
			if err != nil {
				status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Error trying to Marshall ProcInfoPackager Json  %s", err)))
			}
			fmt.Fprintf(os.Stderr, "%s", string(testPack))
			status.ExitFromError(status.NewError(status.SystemError, fmt.Errorf("Error trying to build package image %s", err)))
		}
		log("Packager step built sucessfully.")
		procInfoPack, err := execImage("packager", er)
		if err != nil {
			status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Execution error %s-%d-%d: %v", job, c.Month, c.Year, err)))
		}
		pckResult := storage.PackagingResult{
			ProcInfo: *procInfoPack,
			Package:  procInfoPack.Stdout,
		}
		log(" -- Package executed for %s --\n", job)
		er.Pr = pckResult
		// Store Data
		log("Starting to build Store step ...")
		procInfoStore, err := buildDockerImage("../store", commit)
		if err != nil {
			testStore, err := json.Marshal(&procInfoStore)
			if err != nil {
				status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Error trying to Marshall ProcInfoStore Json  %s", err)))
			}
			fmt.Fprintf(os.Stderr, "%s", string(testStore))
			status.ExitFromError(status.NewError(status.SystemError, fmt.Errorf("Error trying to build package image %s", err)))
		}
		log("Store Step built sucessfully.")
		_, err = execImage("store", er)
		if err != nil {
			status.ExitFromError(status.NewError(status.DataUnavailable, fmt.Errorf("Store error: %v", err)))
			return
		}
		log(" -- Store executed for %s --\n", job)
		return
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
func buildDockerImage(dir, commit string) (*storage.ProcInfo, error) {
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
func execImage(dir string, er executionResult) (*storage.ProcInfo, error) {
	erJSON, err := json.Marshal(er)
	if err != nil {
		return nil, fmt.Errorf("Error trying to marshal er %s", erJSON)
	}
	cmdList := buildCmd(filepath.Base(dir))
	cmd := exec.Command(cmdList[0], cmdList[1:]...)
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

// buildCmd build command to run dockerFile of each step.
func buildCmd(img string) []string {
	var envFile string
	if _, err := os.Stat(fmt.Sprintf("envFiles/.env.%s", img)); !os.IsNotExist(err) {
		envFile = fmt.Sprintf("--env-file=./envFiles/.env.%s ", img)
	}
	cmdFmt := "docker run %s-v dadosjusbr:/output --rm %s %s" //docker args (envFIle outputPath -i), image, args img
	var dockerArgs, imgArgs string
	switch img {
	case "packager":
		outPath := fmt.Sprintf("-e OUTPUT_FOLDER=%s", c.OutputFolder)
		dockerArgs = fmt.Sprintf("-i %s %s", outPath, envFile)
		//cmdList = strings.Split(fmt.Sprintf(`docker run -e %s  -i -v dadosjusbr:/output --rm packager`, outPath), " ")
	case "store":
		dockerArgs = fmt.Sprintf("-i %s", envFile)
		//cmdList = strings.Split(fmt.Sprintf(`docker run %s -i -v dadosjusbr:/output --rm store`, envFile), " ")
	default:
		outPath := fmt.Sprintf("-e OUTPUT_FOLDER=%s/%s", c.OutputFolder, img)
		dockerArgs = fmt.Sprintf("%s %s", outPath, envFile)
		imgArgs = fmt.Sprintf("--mes=%d --ano=%d", c.Month, c.Year)
		//cmdList = strings.Split(fmt.Sprintf(`docker run -v dadosjusbr:/output --rm -e %s --env-file=.env %s --mes=%d --ano=%d`, outPath, filepath.Base(dir), month, year), " ")
	}
	return strings.Split(fmt.Sprintf(cmdFmt, dockerArgs, img, imgArgs), " ")
}

// genCR creates a crawling result
func genCR(job string, procInfo *storage.ProcInfo, commit string, month, year int) (*storage.CrawlingResult, error) {
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
			ProcInfo:  *procInfo,
		}
		return &cr, nil
	}
	if err := json.Unmarshal([]byte(procInfo.Stdout), &cr); err != nil {
		return nil, fmt.Errorf("error trying to unmarshal crawling result: %q", err)
	}
	cr.ProcInfo = *procInfo
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
		e
		return 0
	}
	if exitError, ok := err.(*exec.ExitError); ok {
		return exitError.ExitCode()
	}
	return -2
}
