package status

import "testing"

func TestText(t *testing.T) {
	testCases := []struct {
		name string
		in   int
		out  string
	}{
		{"Testing status OK", 0, "OK"},
		{"Testing status ServiceUnavailable", 1, "Service Unavailable"},
		{"Testing status RequestTimeout", 2, "Request Timedout"},
		{"Testing status DataUnavailable", 3, "Data Unavailable"},
		{"Testing status ParsingError", 4, "Parsing Error"},
		{"Testing unknow status", 505, ""},
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
