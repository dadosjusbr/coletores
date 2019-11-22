package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/dadosjusbr/storage"
)

func main() {
	month := flag.Int("mes", 0, "Mês a ser analisado")
	year := flag.Int("ano", 0, "Ano a ser analisado")
	flag.Parse()

	commit, err := getGitCommit()
	if err != nil {
		logError("%s", err)
		os.Exit(1)
	}

	jobList := []string{
		"/home/marcosbmf/go/projects/coletores/trepb",
	}
	for _, job := range jobList {
		err := build(job, commit)
		if err != nil {
			logError("Building error: %s", err)
			os.Exit(1)
		}
	}

	outputs, execErrs := execJobs(jobList, *month, *year)
	for _, err := range execErrs {
		logError("%s", err)
	}
	result, err := json.Marshal(outputs)
	if err != nil {
		panic("error marshalling results")
	}
	fmt.Printf("%s", result)
	if len(execErrs) > 0 {
		os.Exit(1)
	}
	os.Exit(0)
}

func execJobs(jobs []string, month, year int) ([]storage.CrawlingResult, []error) {
	var execErrors []error
	var outputs []storage.CrawlingResult
	for _, job := range jobs {
		var cr storage.CrawlingResult
		out, err := execDataCollector(job, month, year)
		if err != nil {
			execErrors = append(execErrors, fmt.Errorf("error executing data colector (%s): %q", job, err))
		}
		err = json.Unmarshal(out, &cr)
		if err != nil {
			execErrors = append(execErrors, fmt.Errorf("error unmarshalling crawling result from (%s): %q", job, err))
		} else {
			outputs = append(outputs, cr)
		}
	}

	return outputs, execErrors
}

func execDataCollector(path string, month, year int) ([]byte, error) {
	cmdList := strings.Split(fmt.Sprintf("./%s --mes=%d --ano=%d", filepath.Base(path), month, year), " ")
	cmd := exec.Command(cmdList[0], cmdList[1:]...)
	cmd.Dir = path
	out, err := cmd.CombinedOutput()
	return out, err
}

func getGitCommit() (string, error) {
	cmd := exec.Command("git", "rev-list", "-1", "HEAD")
	stdin, err := cmd.CombinedOutput()
	if err != nil {
		return "", fmt.Errorf("getGitCommit() error: %s", err)
	}
	return string(stdin[:len(stdin)-1]), nil
}

func build(path, commit string) error {
	cmd := exec.Command("go", "build", "-ldflags", fmt.Sprintf(`"-X main.gitCommit=%s"`, commit))
	cmd.Dir = fmt.Sprintf(path)
	err := cmd.Run()
	if err != nil {
		return fmt.Errorf("build() error (%s): %s", path, err)
	}
	return nil
}

// fatalError prints to Stderr
func logError(format string, args ...interface{}) {
	time := fmt.Sprintf("%s: ", time.Now().Format(time.RFC3339))
	fmt.Fprintf(os.Stderr, time+format+"\n", args...)
}
