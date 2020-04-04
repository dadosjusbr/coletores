# Status Package

Status package aims to create standard status codes for the colectors.

## Getting it
```
go get https://github.com/dadosjusbr/coletores
```

## Available status codes

| Status code | Meaning |
--------------|----------
|OK| The process has occurred with no errors.|
|ServiceUnavailable|The website that provides the data is not available.|
|RequestTimeout|The request to retrieve data timedout.|
|DataUnavailable|Requested data is not available, maybe because the website does not provides that information yet.|
|ParsingError| An error has occurred doing parsing|
______________

## Usage example
```
import (
	"fmt"
    "https://github.com/dadosjusbr/coletores"
)

func main() {
    statusText := status.Text(status.DataUnavailable)
    fmt.Println(statusText)
}
```