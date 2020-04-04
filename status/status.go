package status

// Code is a custom type to represent ints
type Code int

const (
	// OK means that the process worked without errors
	OK Code = 0

	// ServiceUnavailable means that the website is unavailable
	ServiceUnavailable Code = 1

	// RequestTimeout means that the request time timedout
	RequestTimeout Code = 2

	// DataUnavailable means that the desired data was not found on crawling
	DataUnavailable Code = 3

	// ParsingError means that an error has occurred during parse
	ParsingError Code = 4

	// Unexpected means that something no expected has happend
	Unexpected Code = 5
)

var (
	statusText = map[Code]string{
		OK:                 "OK",
		ServiceUnavailable: "Service Unavailable",
		RequestTimeout:     "Request Timedout",
		DataUnavailable:    "Data Unavailable",
		ParsingError:       "Parsing Error",
		Unexpected:         "Unexpected",
	}
)

// Text returns a text for a status code. It returns the empty
// string if the code is unknown.
func Text(code Code) string {
	return statusText[code]
}
