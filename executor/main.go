package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/dadosjusbr/storage"
	"github.com/joho/godotenv"
	"github.com/kelseyhightower/envconfig"
)

type config struct {
	OutputFolder string   `envconfig:"OUTPUT_FOLDER"`
	JobList      []string `envconfig:"JOB_LIST"`
	Month        int
	Year         int
	MongoURI     string `envconfig:"MONGODB_URI"`
	DBName       string `envconfig:"MONGODB_DBNAME"`
}

var c config

func init() {
	var err error
	if err := godotenv.Load(); err != nil {
		logError("Error loading .env file")
		os.Exit(1)
	}
	if err := envconfig.Process("", &c); err != nil {
		logError("Error loading config values from .env: %q", err.Error())
		os.Exit(1)
	}
	if c.OutputFolder, err = filepath.Abs(c.OutputFolder); err != nil {
		logError("Error trying to get absolute path for output folder: %q", err.Error())
		os.Exit(1)
	}
	if err := os.Mkdir(c.OutputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		logError("Error creating output folder(%s): %q", c.OutputFolder, err)
		os.Exit(1)
	}
	fmt.Printf("%v\n", c)
}

func main() {
	storageClient, err := storage.NewClient(c.MongoURI)
	if err != nil {
		logError("Error trying to initialize mongo client: %q", err)
		os.Exit(1)
	}
	err = storageClient.Connect(c.DBName)
	if err != nil {
		logError("Error trying to connect to mongo client: %q", err)
		os.Exit(1)
	}
	defer storageClient.Disconnect()

	commit, err := getGitCommit()
	if err != nil {
		logError("%s", err)
		os.Exit(1)
	}

	for _, job := range c.JobList {
		stdOut, stdErr, err := build(job, commit)
		backup(job, "build.stdout", stdOut)
		backup(job, "build.stderr", stdErr)
		if err != nil {
			logError("Build error %s: %q", job, err)
			continue
		}
		stdOut, stdErr, err = execDataCollector(job, c.Month, c.Year)
		backup(job, "exec.stdout", stdOut)
		backup(job, "exec.stderr", stdErr)
		if err != nil {
			logError("Execution error %s: %q", job, err)
			continue
		}
		err = store(stdOut, storageClient)
		if err != nil {
			logError("Store error %s: %q", job, err)
			continue
		}
	}
}

// store stores crawling results to db in storageClient
func store(content []byte, storageClient *storage.Client) error {
	var cr storage.CrawlingResult
	err := json.Unmarshal(content, &cr)
	if err != nil {
		return fmt.Errorf("error trying to unmarshal crawling result: %q", err)
	}
	err = storageClient.Store(cr)
	if err != nil {
		return fmt.Errorf("error trying to store crawling result: %q", err)
	}
	return nil
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

// execDataCollector executes the data collector located in path and returns it's stdin, stdout and exit error if any.
func execDataCollector(path string, month, year int) ([]byte, []byte, error) {
	cmdList := strings.Split(fmt.Sprintf("./%s --mes=%d --ano=%d", filepath.Base(path), month, year), " ")
	cmd := exec.Command(cmdList[0], cmdList[1:]...)
	cmd.Dir = path
	cmd.Env = append(cmd.Env, fmt.Sprintf("OUTPUT_FOLDER=%s/%s", c.OutputFolder, filepath.Base(path)))
	var outb, errb bytes.Buffer
	cmd.Stdout = &outb
	cmd.Stderr = &errb
	err := cmd.Run()
	return outb.Bytes(), errb.Bytes(), err
}

// build runs a go build for each path. It will also insert the value of main.gitCommit in the binaries.
func build(path, commit string) ([]byte, []byte, error) {
	cmd := exec.Command("go", "build", "-ldflags", fmt.Sprintf("-X main.gitCommit=%s", commit))
	cmd.Dir = path
	var outb, errb bytes.Buffer
	cmd.Stdout = &outb
	cmd.Stderr = &errb
	err := cmd.Run()
	return outb.Bytes(), errb.Bytes(), err
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

// fatalError prints to Stderr
func logError(format string, args ...interface{}) {
	time := fmt.Sprintf("%s: ", time.Now().Format(time.RFC3339))
	fmt.Fprintf(os.Stderr, time+format+"\n", args...)
}

// backup will log content of job-description when content is not empty
func backup(job string, desc string, content []byte) {
	if len(content) == 0 {
		return
	}
	path := fmt.Sprintf("%s/%s(%d-%d)-%s-%s", c.OutputFolder, filepath.Base(job), c.Month, c.Year, desc, time.Now().Format(time.RFC3339))
	f, err := os.Create(path)
	if err != nil {
		logError("backup error: error creating file: %s", err)
		os.Exit(1)
	}
	defer f.Close()

	_, err = f.Write(content)
	if err != nil {
		logError("backup error: error writing to file: %s", err)
		os.Exit(1)
	}
}
