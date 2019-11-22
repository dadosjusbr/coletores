package main

import (
	"flag"
	"fmt"
	"log"
	"os/exec"
	"path/filepath"
	"strings"
)

func main() {
	month := flag.Int("mes", 0, "Mês a ser analisado")
	year := flag.Int("ano", 0, "Ano a ser analisado")
	flag.Parse()

	commit, err := getGitCommit()
	if err != nil {
		log.Fatalf("%s", err)
	}

	jobList := []string{
		"/home/marcosbmf/go/projects/coletores/trepb",
	}
	for _, job := range jobList {
		err := build(job, commit)
		if err != nil {
			log.Fatalf("Building error: %s", err)
		}
	}
	for _, job := range jobList {
		out, err := execDataCollector(job, *month, *year)
		fmt.Println(out, err)
	}
}

func execDataCollector(path string, month, year int) (string, error) {
	cmdList := strings.Split(fmt.Sprintf("./%s --mes=%d --ano=%d", filepath.Base(path), month, year), " ")
	cmd := exec.Command(cmdList[0], cmdList[1:]...)
	cmd.Dir = path
	out, err := cmd.CombinedOutput()
	return string(out), err
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
