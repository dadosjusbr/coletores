package main

import (
	"testing"
)

var flagtests = []struct {
	name            string
	memberType      string
	patternToSearch string
	fakeHTMLFile    string
	desiredOutput   string
}{
	{"Should get right code for membros ativos for years differente of 2017", "membrosAtivos", ":membros-ativos-02-2019", ".../4554/resource-fevereiro:download=5051:membros-ativos-02-2019", "5051"},
	{"Should fail gettting code for membros ativos for years differente of 2017", "membrosAtivos", ":membros-ativos-fevereiro-2019", ".../4554/status:download=5051:membros-ativos-02-2019", "nil"},
	{"Should fail gettting code for membros ativos for year 2017", "membrosAtivos", ":membros-ativos-fevereiro-2017", ".../4554/recursos:download=5051:membros-ativos-02-2019", "nil"},
	{"Should get right code for membros ativos for year 2017", "membrosAtivos", ":quadro-de-membros-ativos-fevereiro-2017", ".../4554/resource-online:download=5051:quadro-de-membros-ativos-fevereiro-2017", "5051"},
	{"Should get right code for membros in ativos for year differente of 2014", "membrosInativos", ":membros-inativos-03-2017", ".../4554/resource:download=4312:membros-inativos-03-2017", "4312"},
	{"Should get right code for membros in ativos for year 2014 and month different of janeiro", "membrosInativos", ":membros-inativos-03-2014", ".../4554/resource:download=1234:membros-inativos-03-2014", "1234"},
	{"Should get right code for membros in ativos for year 2014 and month janeiro", "membrosInativos", ":membros-inativos-01-2015", ".../4554/resource:download=4567:membros-inativos-01-2015", "4567"},
}

func TestFindFileIdentifier(t *testing.T) {
	for _, tt := range flagtests {
		t.Run(tt.name, func(t *testing.T) {
			code, _ := findFileIdentifier(tt.memberType, tt.fakeHTMLFile, tt.patternToSearch)
			if code != tt.desiredOutput {
				t.Errorf("got %s, want %s", code, tt.desiredOutput)
			}
		})
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
