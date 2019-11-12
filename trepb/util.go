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
	Timeout: time.Second * 180,
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

// filePath returns the path that will be used for the saved file.
func filePath(outputFolder string, month, year int) string {
	return fmt.Sprintf("./%s/remuneracoes-trepb-%02d-%04d.html", outputFolder, month, year)
}

// substringBetween returns the substring in str between before and after strings.
func substringBetween(str, before, after string) string {
	a := strings.SplitAfterN(str, before, 2)
	b := strings.SplitAfterN(a[len(a)-1], after, 2)
	if 1 == len(b) {
		return b[0]
	}
	return b[0][0 : len(b[0])-len(after)]
}

// getValue takes a float64 pointer and returns it's value or 0 if it's nil
func getValue(p *float64) float64 {
	if p == nil {
		return 0
	}
	return *p
}

// sumMapValues takes a map of string -> float64 and return the sum of the map values.
func sumMapValues(m map[string]float64) float64 {
	var sum float64
	for _, v := range m {
		sum += v
	}
	return sum
}

// retrieveFloat makes an xpath query to the row and retrieve a float from inner text of the node found.
func retrieveFloat(row *html.Node, v interface{}, xpath string) error {
	r, err := htmlquery.Query(row, xpath)
	if err != nil || r == nil {
		return fmt.Errorf("error trying to find (%s): %q", xpath, err)
	}

	value, err := parseFloat(htmlquery.InnerText(r))
	if err != nil {
		return fmt.Errorf("error parsing float(%s): %q", htmlquery.InnerText(r), err)
	}
	value = math.Abs(value)

	if v, ok := v.(**float64); ok {
		*v = &value
		return nil
	}
	if v, ok := v.(*float64); ok {
		*v = value
		return nil
	}
	return fmt.Errorf("parameter v is not a pointer to a float or a pointer to pointer of float")
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
