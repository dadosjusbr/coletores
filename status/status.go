package status

import (
	"errors"
	"fmt"
	"log"
	"os"
)

// Code is a custom type to represent ints
type Code int

const (
	// OK means that the process worked without errors
	OK Code = 0

	// InvalidParameters should be used for scenarios where month and year are not valid
	InvalidParameters Code = 1

	// SystemError should be used for scenarios like i/o erros, for example a failure on opening a file
	SystemError Code = 2

	// ConnectionError should be used for scenarios with connection problems, like timeouts or service unavailable
	ConnectionError Code = 3

	// DataUnavailable means that the desired data was not found on crawling
	DataUnavailable Code = 4

	//InvalidFile should be used for invalid files or for scenarios where some data could not be extracted
	InvalidFile Code = 5

	// Unknown means that something unexpected has happend
	Unknown Code = 6
)

var (
	statusText = map[Code]string{
		OK:                "OK",
		InvalidParameters: "Invalid Parameters",
		SystemError:       "System Error",
		ConnectionError:   "Connection Error",
		DataUnavailable:   "Data Unavailable",
		InvalidFile:       "Invalid File",
		Unknown:           "Unknown",
	}
)

// Text returns a text for a status code. It returns the empty
// string if the code is unknown.
func Text(code Code) string {
	return statusText[code]
}

// ExitFromError logs the error message and call os.Exit
// passing the code if err is of type StatusError
func ExitFromError(err error) {
	log.Println(fmt.Errorf("%q", err))
	var se *Error
	if errors.As(err, &se) {
		os.Exit(int(se.Code))
	}
	os.Exit(int(Unknown))
}
