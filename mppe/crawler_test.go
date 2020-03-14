package main

import (
	"testing"
)

var findFileIdentifierSucessTestCases = []struct {
	name            string
	memberType      string
	patternToSearch string
	fakeHTMLFile    string
	desiredOutput   string
}{
	{"Should get right code for membros ativos for years differente of 2017", "membrosAtivos", ":membros-ativos-02-2019", ".../4554/resource-fevereiro:download=5051:membros-ativos-02-2019", "5051"},
	{"Should get right code for membros ativos for year 2017", "membrosAtivos", ":quadro-de-membros-ativos-fevereiro-2017", ".../4554/resource-online:download=5051:quadro-de-membros-ativos-fevereiro-2017", "5051"},
	{"Should get right code for membros inativos for year differente of 2014", "membrosInativos", ":membros-inativos-03-2017", ".../4554/resource:download=4312:membros-inativos-03-2017", "4312"},
	{"Should get right code for membros inativos for year 2014 and month different of janeiro", "membrosInativos", ":membros-inativos-03-2014", ".../4554/resource:download=1234:membros-inativos-03-2014", "1234"},
	{"Should get right code for membros inativos for year 2014 and month janeiro", "membrosInativos", ":membros-inativos-01-2015", ".../4554/resource:download=4567:membros-inativos-01-2015", "4567"},
	{"Should get right code for servidores ativos", "servidoresAtivos", ":servidores-ativos-01-2015", ".../31342sas2/endpoint:download=9999:servidores-ativos-01-2015", "9999"},
	{"Should get right code for servidores inativos", "servidoresInativos", ":servidores-inativos-01-2015", ".../ghytr6/resource:download=1098:servidores-inativos-01-2015", "1098"},
	{"Should get right code for pensionistas", "pensionistas", ":pensionistas-01-2015", ".../5tghjuw2/Controller:random=5453:pensionistas-01-2015", "5453"},
	{"Should get right code for colaboradores", "colaboradores", ":contracheque-valores-percebidos-colaboradores-fevereiro", ".../random/servlet:code=3490:contracheque-valores-percebidos-colaboradores-fevereiro", "3490"},
	{"Should get right code for exercicios anteriores", "exerciciosAnteriores", ":dea-022019", ".../controller_servlet:download=5378:dea-022019", "5378"},
	{"Should get right code for indenizacoes e outros pagamentos", "indenizacoesEOutrosPagamentos", ":virt-abril-2019", ".../members_controller:code=8712:virt-abril-2019", "8712"},
}

func TestFindFileIdentifier_Success(t *testing.T) {
	for _, tt := range findFileIdentifierSucessTestCases {
		t.Run(tt.name, func(t *testing.T) {
			code, _ := findFileIdentifier(tt.memberType, tt.fakeHTMLFile, tt.patternToSearch)
			if code != tt.desiredOutput {
				t.Errorf("got %s, want %s", code, tt.desiredOutput)
			}
		})
	}
}

var errorMessageSucessTestCases = []struct {
	name       string
	in         []string
	outMessage string
}{
	{"two error strings", []string{"error1", "error2"}, "\nerror1\n\nerror2\n"},
	{"one error string", []string{"error1"}, "\nerror1\n"},
	{"three error strings", []string{"error1", "error2", "error3"}, "\nerror1\n\nerror2\n\nerror3\n"},
}

func TestProcessErrorMessage(t *testing.T) {
	for _, tt := range errorMessageSucessTestCases {
		t.Run(tt.name, func(t *testing.T) {
			err := processErrorMessages(tt.in)
			if err.Error() != tt.outMessage {
				t.Errorf("got %s, want %s", err.Error(), tt.outMessage)
			}
		})
	}
}
