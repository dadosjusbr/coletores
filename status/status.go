package status

import (
	"log"
	"os"
)

// Code is a custom type to represent ints
type Code int

// Colector status codes. They're sorted in a semantic order
// where in the house of 100's are the possible erros for the
// setup process, at the 200's the possible erros on Crawling,
// at 300's the ones possible on Parsing and at 400's the general
// errors.
const (
	// OK means that the process worked without errors
	OK Code = 0

	// MonthAndYearNotProvided means that month and year to search were not provided
	MonthAndYearNotProvided Code = 100

	// InvalidMonth should be used if the colector has a month that it does not suport yet
	InvalidMonth Code = 101

	// InvalidYear should be used if the colector has a year that it does not suport yet
	InvalidYear Code = 102

	// CouldNotCreateDirectory means that the directory to hold files could not be created
	CouldNotCreateDirectory Code = 103

	// ServiceUnavailable means that the website is unavailable
	ServiceUnavailable Code = 200

	// RequestTimeout means that the request time timedout
	RequestTimeout Code = 201

	// DataUnavailable means that the desired data was not found on crawling
	DataUnavailable Code = 202

	// CouldNotOpenFile means that an error has occurred trying to read the file
	CouldNotOpenFile Code = 300

	// CouldNotExtractData means that ocurred and error extracting a value from file
	CouldNotExtractData Code = 301

	// Unexpected means that something no expected has happend
	Unexpected Code = 400
)

var (
	statusText = map[Code]string{
		OK: "OK",

		MonthAndYearNotProvided: "Month and year not provided",
		InvalidMonth:            "Invalid Month",
		InvalidYear:             "Invalid Year",
		CouldNotCreateDirectory: "Could not create directory",

		ServiceUnavailable: "Service Unavailable",
		RequestTimeout:     "Request Timedout",
		DataUnavailable:    "Data Unavailable",

		CouldNotOpenFile:    "Could not open file",
		CouldNotExtractData: "Could not extract data",

		Unexpected: "Unexpected",
	}
)

// Text returns a text for a status code. It returns the empty
// string if the code is unknown.
func Text(code Code) string {
	return statusText[code]
}

// ExitFromError exits the program logging a message an
// setting the process code
func ExitFromError(statusError *StatusError) {
	log.Println(statusError.Message)
	os.Exit(int(statusError.Code))
}
