package main

import (
	"fmt"
	"math"
	"net/http"
	"strconv"
	"strings"
	"time"

	"github.com/antchfx/htmlquery"
	"golang.org/x/net/html"
)

var netClient = &http.Client{
	Timeout: time.Second * 150,
	CheckRedirect: func(req *http.Request, via []*http.Request) error {
		return http.ErrUseLastResponse
	},
}

// httpReq makes specified request and returns the html parsed tree.
func httpReq(req *http.Request) (*html.Node, error) {
	resp, err := netClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("error making request to %s: %q", req.URL, err)
	}
	defer resp.Body.Close()

	doc, err := htmlquery.Parse(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("error loading doc (%s): %q", req.URL, err)
	}
	return doc, nil
}

//substringBetween returns the substring in str between before and after strings.
func substringBetween(str, before, after string) string {
	a := strings.SplitAfterN(str, before, 2)
	b := strings.SplitAfterN(a[len(a)-1], after, 2)
	if 1 == len(b) {
		return b[0]
	}
	return b[0][0 : len(b[0])-len(after)]
}

// retrieveFloat makes an xpath query to the row and retrieve a float from inner text of the node found.
func retrieveFloat(row *html.Node, v *float64, xpath string) error {
	r, err := htmlquery.Query(row, xpath)
	if err != nil || r == nil {
		return fmt.Errorf("error trying to find (%s): %q", xpath, err)
	}

	value, err := parseFloat(htmlquery.InnerText(r))
	if err != nil {
		return fmt.Errorf("error parsing float(%s): %q", htmlquery.InnerText(r), err)
	}

	*v = math.Abs(value)
	return nil
}

// parseFloat makes the string with format "xx.xx,xx" able to be parsed by the strconv.ParseFloat and return it parsed.
func parseFloat(s string) (float64, error) {
	s = strings.Trim(s, " ")
	s = strings.Replace(s, ",", ".", 1)
	if n := strings.Count(s, "."); n > 1 {
		s = strings.Replace(s, ".", "", n-1)
	}
	return strconv.ParseFloat(s, 64)
}

// retrieveString makes an xpath query to the row and retrieve the innerText of the node found trimmed for white spaces.
func retrieveString(row *html.Node, s *string, xpath string) error {
	r, err := htmlquery.Query(row, xpath)
	if err != nil || r == nil {
		return fmt.Errorf("error trying to find (%s): %q", xpath, err)
	}
	*s = strings.Trim((htmlquery.InnerText(r)), " ")
	return nil
}
