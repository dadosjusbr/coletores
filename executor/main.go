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
	client, err := newClient()
	if err != nil {
		logError("newClient() error: %s", err)
		os.Exit(1)
	}

	commit, err := getGitCommit()
	if err != nil {
		logError("%s", err)
		os.Exit(1)
	}
	var wg sync.WaitGroup
	wg.Add(len(c.JobList))
	for _, job := range c.JobList {
		go func(job string) {
			defer wg.Done()
			stdOut, stdErr, err := build(job, commit)
			backup(job, "build.stdout", stdOut)
			backup(job, "build.stderr", stdErr)
			if err != nil {
				logError("Build error %s: %q", job, err)
			}

			stdOut, stdErr, err = execDataCollector(job, c.Month, c.Year)
			backup(job, "exec.stdout", stdOut)
			backup(job, "exec.stderr", stdErr)
			// Data collection execution exited with error. Abort job.
			if err != nil {
				logError("Execution error %s-%d-%d: %q", job, c.Month, c.Year, err)
				return
			}
			log(" -- Data collector executed for %s --\n", job)

			err = store(stdOut, client)
			if err != nil {
				logError("Store error %s-%d-%d: %q", job, c.Month, c.Year, err)
			}
			log(" -- Store executed for %s --\n", job)
		}(job)
	}
	wg.Wait()
	fmt.Println("Finished.")
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

// log prints to Stdout
func log(format string, args ...interface{}) {
	time := fmt.Sprintf("%s: ", time.Now().Format(time.RFC3339))
	fmt.Fprintf(os.Stdout, time+format+"\n", args...)
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
