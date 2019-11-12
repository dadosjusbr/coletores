package main

import (
	"bytes"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"golang.org/x/net/html"
)

// Test if httpReq is making desired request and returning correct parsed document.
func Test_httpReq(t *testing.T) {
	htmlSample := "<html><head></head><body><div><span></span></div></body></html>"
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, htmlSample)
	}))
	defer ts.Close()

	req, err := http.NewRequest("GET", ts.URL, nil)
	assert.NoError(t, err)

	doc, err := httpReq(req)
	assert.NoError(t, err)

	var buf bytes.Buffer
	assert.NoError(t, html.Render(&buf, doc))
	// HTML parser adds a \n before closing of body tag.
	assert.Equal(t, "<html><head></head><body><div><span></span></div>\n</body></html>", buf.String())
}

// Test if substringBetween is returning the desired strings.
func Test_substringBetween(t *testing.T) {
	type args struct {
		str    string
		before string
		after  string
	}
	tests := []struct {
		name string
		args args
		want string
	}{
		{"no splits", args{"hello", "g", "g"}, "hello"},
		{"both splits", args{"ghellog", "g", "o"}, "hell"},
		{"first split only", args{"ghello", "g", "m"}, "hello"},
		{"last split only", args{"hellog", "m", "g"}, "hello"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := substringBetween(tt.args.str, tt.args.before, tt.args.after); got != tt.want {
				t.Errorf("substringBetween() = %v, want %v", got, tt.want)
			}
		})
	}
}

// Test if parseFloat will get the correct numbers from the parsed string.
func Test_parseFloat(t *testing.T) {
	tests := []struct {
		name    string
		arg     string
		want    float64
		wantErr bool
	}{
		{"units", "10,55", 10.55, false},
		{"units without comma", "10.55", 10.55, false},
		{"Thousands", "1.000,55", 1000.55, false},
		{"Not a number", "sd", 0, true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := parseFloat(tt.arg)
			if (err != nil) != tt.wantErr {
				t.Errorf("parseFloat() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if got != tt.want {
				t.Errorf("parseFloat() = %v, want %v", got, tt.want)
			}
		})
	}
}

func Test_retrieveFloat(t *testing.T) {
	htmlSample := `<table><tr><td id="h01">115</td>
	<td id="h02">115.10</td>
	<td id="h03">-115.44</td>
	<td id="h04">         115.16           </td>
	<td id="h05">  notANumber           </td>
	<td id="h06">1.150,16</td>
	<tr><table>`
	rowSample, err := html.Parse(strings.NewReader(htmlSample))
	assert.NoError(t, err)
	var value float64
	var pointer *float64

	type args struct {
		row   *html.Node
		v     interface{}
		xpath string
	}
	tests := []struct {
		name    string
		args    args
		wantErr bool
		want    float64
	}{
		{"To variable", args{rowSample, &value, `//td[@id="h01"]`}, false, 115.0},
		{"To pointer", args{rowSample, &pointer, `//td[@id="h01"]`}, false, 115.0},
		{"float", args{rowSample, &value, `//td[@id="h02"]`}, false, 115.10},
		{"negative", args{rowSample, &value, `//td[@id="h03"]`}, false, 115.44},
		{"empty spaces around the number", args{rowSample, &value, `//td[@id="h04"]`}, false, 115.16},
		{"BRL Format", args{rowSample, &value, `//td[@id="h06"]`}, false, 1150.16},
		{"bad number error", args{rowSample, &value, `//td[@id="h05"]`}, true, 0},
		{"bad query", args{rowSample, &value, `//td[@id="c00"]`}, true, 0},
		{"wrong value parameter", args{rowSample, nil, `//td[@id="h04"]`}, true, 0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if err := retrieveFloat(tt.args.row, tt.args.v, tt.args.xpath); (err != nil) != tt.wantErr {
				t.Fatalf("retrieveFloat() error = %v, wantErr %v", err, tt.wantErr)
			}
			if !tt.wantErr {
				if v, ok := tt.args.v.(**float64); ok {
					if *(*v) != tt.want {
						t.Fatalf("retrieveFloat() want %f, have %f", tt.want, *(*v))
					}
				}
				if v, ok := tt.args.v.(*float64); ok {
					if *v != tt.want {
						t.Fatalf("retrieveFloat() want %f, have %f", tt.want, *v)
					}
				}
			}
		})
	}
}

func Test_retrieveString(t *testing.T) {
	htmlSample := `<table><tr>
	<td id="h01">hello World</td>
	<td id="h02">              hello        </td>
	<td id="h03">João Cárlos Mẽlo</td>
	<tr><table>`
	rowSample, err := html.Parse(strings.NewReader(htmlSample))
	assert.NoError(t, err)

	var result string

	type args struct {
		row   *html.Node
		s     *string
		xpath string
	}
	tests := []struct {
		name    string
		args    args
		wantErr bool
		want    string
	}{
		{"Simple string", args{rowSample, &result, `//td[@id="h01"]`}, false, "hello World"},
		{"empty spaces around string", args{rowSample, &result, `//td[@id="h02"]`}, false, "hello"},
		{"words with latin letters", args{rowSample, &result, `//td[@id="h03"]`}, false, "João Cárlos Mẽlo"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if err := retrieveString(tt.args.row, tt.args.s, tt.args.xpath); (err != nil) != tt.wantErr {
				t.Errorf("retrieveString() error = %v, wantErr %v", err, tt.wantErr)
			}
			if !tt.wantErr && *tt.args.s != tt.want {
				t.Errorf("retrieveString() wrong result. Have: %s, want: %s", *tt.args.s, tt.want)
			}
		})
	}
}
