package status

import "testing"

func TestText(t *testing.T) {
	testCases := []struct {
		name string
		in   Code
		out  string
	}{
		{"Testing status OK", 0, "OK"},

		{"Testing status MonthAndYearNotProvided", 100, "Month and year not provided"},
		{"Testing status InvalidMonth", 101, "Invalid Month"},
		{"Testing status InvalidYear", 102, "Invalid Year"},
		{"Testing status CouldNotCreateDirectory", 103, "Could not create directory"},

		{"Testing status ServiceUnavailable", 200, "Service Unavailable"},
		{"Testing status RequestTimeout", 201, "Request Timedout"},
		{"Testing status DataUnavailable", 202, "Data Unavailable"},

		{"Testing unknow status", 505, ""},
		{"Testing status Unexpected", 400, "Unexpected"},
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

func TestNewStatusError(t *testing.T) {
	testCases := []struct {
		name    string
		message string
		code    Code
		out     *StatusError
	}{
		{
			"Should create a status error for time out",
			"request timed out",
			RequestTimeout,
			&StatusError{
				Message: "request timed out",
				Code:    RequestTimeout,
			},
		},
		{
			"Should create a status error for data unavailable",
			"data is not present",
			DataUnavailable,
			&StatusError{
				Message: "data is not present",
				Code:    DataUnavailable,
			},
		},
	}
	for _, tt := range testCases {
		t.Run(tt.name, func(t *testing.T) {
			se := NewStatusError(tt.code, tt.message)
			if se.Code != tt.out.Code {
				t.Errorf("got %d, want %d", se.Code, tt.out.Code)
			}
			if se.Message != tt.out.Message {
				t.Errorf("got %s, want %s", se.Message, tt.out.Message)
			}
		})
	}
}
