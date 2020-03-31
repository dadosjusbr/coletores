package main

import "testing"

func TestGetTypeOfFile_Sucess(t *testing.T) {
	testCases := []struct {
		name string
		in   string
		out  string
	}{
		{"Should has sucess on getting file name", "fileName-02-2019.xlsx", "fileName"},
		{"Should has sucess on getting file name", "01-29-february-file-name-02-2019.xlsx", "01-29-february-file-name"},
	}
	for _, tt := range testCases {
		t.Run(tt.name, func(t *testing.T) {
			res := getFileDocumentation(tt.in)
			if res != tt.out {
				t.Errorf("got %s, want %s", res, tt.out)
			}
		})
	}
}
