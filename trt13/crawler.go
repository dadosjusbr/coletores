package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

var netClient = &http.Client{
	Timeout: time.Second * 60,
}

func crawl(filePath string, month, year int) error {
	f, err := os.Create(filePath)
	if err != nil {
		return fmt.Errorf("Error creating file(%s):%q", filePath, err)
	}
	defer f.Close()

	reqURL := fmt.Sprintf("https://www.trt13.jus.br/transparenciars/api/anexoviii/anexoviii?mes=%02d&ano=%04d", month, year)
	if err = download(reqURL, f); err != nil {
		os.Remove(filePath)
		return fmt.Errorf("Error while downloading content (%02d-%04d): %q", month, year, err)
	}
	return nil
}

func download(reqURL string, w io.Writer) error {
	req, err := http.NewRequest("GET", reqURL, nil)
	if err != nil {
		return fmt.Errorf("error while creating *http.Request: %q", err)
	}
	req.Header.Set("Accept", "application/json")

	resp, err := netClient.Do(req)
	if err != nil {
		return fmt.Errorf("error while making GET request to (%s): %q", reqURL, err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("unexpected status code. Request: GET (%s) - Response: (%d): %s", reqURL, resp.StatusCode, http.StatusText(resp.StatusCode))
	}

	if io.Copy(w, resp.Body); err != nil {
		return fmt.Errorf("error copying response content:%q", err)
	}
	return nil
}
