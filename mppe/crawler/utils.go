package crawler

import (
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"regexp"
	"strconv"
	"strings"
)

var (
	baseURL = "https://transparencia.mppe.mp.br/contracheque/category/"

	months = map[int]string{
		1:  "janeiro",
		2:  "fevereiro",
		3:  "marco",
		4:  "maio",
		5:  "abril",
		6:  "junho",
		7:  "julho",
		8:  "agosto",
		9:  "setembro",
		10: "outurbo",
		11: "novembro",
		12: "dezembro",
	}
)

// download a file and put its bytes into a buffer
func donwloadFile(url string, w io.Writer) error {
	resp, err := http.Get(url)

	if err != nil {
		return fmt.Errorf("error downloading file:%q", err)
	}

	defer resp.Body.Close()

	if _, err := io.Copy(w, resp.Body); err != nil {
		return fmt.Errorf("error copying response content:%q", err)
	}

	return nil
}

// it get a path of a file and returns the file content as a string
func fileToString(filePath string) (string, error) {
	bytes, err := ioutil.ReadFile(filePath)
	if err != nil {
		return "nil", fmt.Errorf("Error getting downloaded html as a string")
	}
	return string(bytes), nil
}

// it gets a HMLT file as a string and searchs inside of it a pattern
// with only numbers
func findFileIdentifier(htmlAsString, pattern string) (string, error) {
	indexOfPattern := strings.Index(htmlAsString, pattern)

	nPreviousChars, err := strconv.Atoi(os.Getenv("PREVIOUS_N_CHARS"))

	if err != nil {
		return "nil", fmt.Errorf("Not possible to get previous n chars from environment")
	}

	if indexOfPattern > 0 {
		substringWithFileIdentifier := htmlAsString[indexOfPattern-nPreviousChars : indexOfPattern]
		possibleMatches := regexp.MustCompile("[0-9]+").FindAllString(substringWithFileIdentifier, -1)
		if len(possibleMatches) == 0 {
			return "nil", fmt.Errorf("Was not possible to get file indetifier")
		}
		fileIdentifier := possibleMatches[0]
		return fileIdentifier, nil
	}

	return "nil", fmt.Errorf("Was not found anny pattern")
}
