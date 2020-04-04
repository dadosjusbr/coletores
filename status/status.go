package status

const (
	// OK means that the process worked without errors
	OK = 0

	// ServiceUnavailable means that the website is unavailable
	ServiceUnavailable = 1

	// RequestTimeout means that the request time timedout
	RequestTimeout = 2

	// DataUnavailable means that the desired data was not found on crawling
	DataUnavailable = 3

	// ParsingError means that an error has occurred during parse
	ParsingError = 4
)

var (
	statusText = map[int]string{
		OK:                 "OK",
		ServiceUnavailable: "Service Unavailable",
		RequestTimeout:     "Request Timedout",
		DataUnavailable:    "Data Unavailable",
		ParsingError:       "Parsing Error",
	}
)

// Text returns a text for a status code. It returns the empty
// string if the code is unknown.
func Text(code int) string {
	return statusText[code]
}
