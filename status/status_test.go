package status

import (
	"errors"
	"fmt"
	"log"
	"os"
	"os/exec"
	"syscall"
	"testing"
)

func TestText(t *testing.T) {
	testCases := []struct {
		name string
		in   Code
		out  string
	}{
		{"Testing status OK", 0, "OK"},
		{"Testing status InvalidParameters", 1, "Invalid Parameters"},
		{"Testing status SystemError", 2, "System Error"},
		{"Testing status ConnectionError", 3, "Connection Error"},
		{"Testing status DataUnavailable", 4, "Data Unavailable"},
		{"Testing status InvalidFile", 5, "Invalid File"},
		{"Testing Unknown status", 6, "Unknown"},
		{"Testing status Unexpected", -505, ""},
	}
	for _, tt := range testCases {
		t.Run(tt.name, func(t *testing.T) {
			res := Text(tt.in)
			if res != tt.out {
				t.Errorf("got %s, want %s", res, tt.out)
			}
		})
	}
}

func TestExitFromError(t *testing.T) {
	testCode := int(InvalidFile)
	if os.Getenv("FLAG") == "1" {
		ExitFromError(NewStatusError(InvalidFile, errors.New("Invalid Parameters")))
		return
	}
	cmd := exec.Command(os.Args[0], "-test.run=TestExitFromError")
	cmd.Env = append(os.Environ(), "FLAG=1")
	err := cmd.Run()
	e, ok := err.(*exec.ExitError)
	if !ok {
		log.Fatal("failed to get ExitError")
	}
	status, ok := e.Sys().(syscall.WaitStatus)
	if !ok {
		log.Fatal("failed to status from execution")
	}
	if status.ExitStatus() != testCode {
		log.Fatal(fmt.Sprintf("want %d, got %d", status.ExitStatus(), testCode))
	}
}
