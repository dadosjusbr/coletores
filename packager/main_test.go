package main

import (
	"testing"

	"github.com/dadosjusbr/storage"
	"golang.org/x/mod/sumdb/dirhash"
)

func makePointer(x float64) *float64 {
	return &x
}

var (
	emp2Row = []storage.Employee{
		{
			Reg:       "",
			Name:      "ADAUTO DIAS DOS SANTOS",
			Role:      "OFICIAL DE DILIGENCIA I - APOSENTADO(A) ",
			Type:      "servidor",
			Workplace: "PBPREV",
			Active:    false,
			Income: &storage.IncomeDetails{
				Total: 30368.59,
				Wage:  makePointer(7000),
				Perks: &storage.Perks{
					Total: 600,
				},
				Other: &storage.Funds{
					Total:            100,
					PersonalBenefits: makePointer(7475.71),
					EventualBenefits: makePointer(0),
					PositionOfTrust:  makePointer(5990.88),
					Gratification:    makePointer(0),
					OriginPosition:   makePointer(0),
				},
			},
			Discounts: &storage.Discount{
				Total:            8930.05,
				PrevContribution: makePointer(2719.5),
				CeilRetention:    makePointer(0),
				IncomeTax:        makePointer(6210.55),
				Others: map[string]float64{
					"Sundry": 0,
				},
			},
		},
		{
			Reg:       "",
			Name:      "Abraao Falcao De Carvalho",
			Role:      "Promotor Eleitoral",
			Type:      "servidor",
			Workplace: "10ª zona eleitoral - guarabira/pb",
			Active:    true,
			Income: &storage.IncomeDetails{
				Total: 10000,
				Wage:  makePointer(5000),
				Perks: &storage.Perks{
					Total: 200,
				},
				Other: &storage.Funds{
					Total:            500,
					PersonalBenefits: makePointer(6476.95),
					EventualBenefits: makePointer(0),
					PositionOfTrust:  makePointer(4631.61),
					Gratification:    makePointer(0),
					OriginPosition:   makePointer(0),
				},
			},
			Discounts: &storage.Discount{
				Total:            405.98,
				PrevContribution: makePointer(992),
				CeilRetention:    makePointer(0),
				IncomeTax:        makePointer(405.98),
				Others: map[string]float64{
					"Sundry": 0,
				},
			},
		},
	}

	crawler = storage.Crawler{CrawlerID: "mppb", CrawlerVersion: ""}
	cr      = storage.CrawlingResult{AgencyID: "mppb", Year: 2020, Month: 2, Crawler: crawler, Employees: emp2Row, Files: []string{"teste.txt", "outroTeste.txt"}}
)

func Test_pack(t *testing.T) {
	tests := []struct {
		name    string
		cr      storage.CrawlingResult
		wantErr bool
	}{
		//Test if zip file has the same content of a sample zip file.
		{name: "Ok", cr: cr},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			zipFile := pack(tt.cr)
			hashPack, _ := dirhash.HashZip(zipFile, dirhash.Hash1)
			hashSample, _ := dirhash.HashZip("sampleDtPackage.zip", dirhash.Hash1)
			if hashPack != hashSample {
				t.Errorf("Integrity files has not the same content!")
			}
		})
	}
}
