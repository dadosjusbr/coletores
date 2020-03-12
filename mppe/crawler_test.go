package main

import (
	"testing"
)

func TestFindFileIdentifier(t *testing.T) {
	fakeHTMLFile := ".../4554/someResourcePath-fevereiro:download=5051:membros-ativos-02-2019"
	category := "remuneracao-de-todos-os-membros-ativos"
	memberType := "membrosAtivos"
	year := 2019
	month := 2
	patternToSearch := pathResolver(month, year, category)
	code, err := findFileIdentifier(memberType, fakeHTMLFile, patternToSearch)
	if code != "5051" {
		t.Error()
	}
	if err != nil {
		t.Error()
	}
}

func TestProcessErrorMessageMustReturnNull(t *testing.T) {
	emptyStringList := []string{}
	err := processErrorMessages(emptyStringList)
	if err != nil {
		t.Error()
	}
}

func TestProcessErrorMessageMustNotReturnNull(t *testing.T) {
	fakeErrorMessages := []string{"error1"}
	err := processErrorMessages(fakeErrorMessages)
	if err == nil {
		t.Error()
	}
}
