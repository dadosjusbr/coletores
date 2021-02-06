package main

import (
	"fmt"
	"io"
	"net/http"
	"net/http/httputil"
	"os"
	"time"
)

var netClient = &http.Client{
	Timeout: time.Second * 360,
}

// crawl retrieve payment information from TJ-BA and save it into a filePath
func crawl(filePath string, month, year int) error {
	f, err := os.Create(filePath)
	if err != nil {
		return fmt.Errorf("Error creating file(%s):%q", filePath, err)
	}
	defer f.Close()

	url := fmt.Sprintf("https://transparencia.tjba.jus.br/transparencia/api/v1/remuneracao/ano/%d/mes/%d", year, month)

	if err = download(url, f); err != nil {
		os.Remove(filePath)
		return fmt.Errorf("Error while downloading content (%02d-%04d): %q", month, year, err)
	}
	return nil
}

// download makes a req to reqURL and saves response body to an io.Writer
func download(reqURL string, w io.Writer) error {
    req, err := http.NewRequest(http.MethodGet, reqURL, nil)
    if err != nil {
        return fmt.Errorf("error while creating a GET request to (%s): %q", reqURL, err)
    }
    requestDump, err := httputil.DumpRequestOut(req, true)
    if err != nil {
		return fmt.Errorf("error while dumping the request: GET (%s) - Error: %q", reqURL, err)
	}
	fmt.Printf("%q", requestDump)

    resp, err := netClient.Do(req)

	if err != nil {
		return fmt.Errorf("error while making GET request to (%s): %q", reqURL, err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("unexpected status code. Request: GET (%s) - Response: (%d): %s", reqURL, resp.StatusCode, http.StatusText(resp.StatusCode))
	}

	responseDump, err := httputil.DumpResponse(resp, true)
	if err != nil {
		return fmt.Errorf("error while dumping the response: GET (%s) - Error: %q", reqURL, err)
	}
	fmt.Printf("%q", responseDump)

	if _, err := io.Copy(w, resp.Body); err != nil {
		return fmt.Errorf("error copying response content:%q", err)
	}
	return nil
}
