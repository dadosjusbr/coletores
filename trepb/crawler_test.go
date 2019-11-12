package main

import (
	"io/ioutil"
	"os"
	"strings"
	"testing"

	"github.com/antchfx/htmlquery"
	"github.com/stretchr/testify/assert"
	"golang.org/x/net/html"
)

func Test_save(t *testing.T) {
	parsedHTML, err := html.Parse(strings.NewReader("<table></table>"))
	assert.NoError(t, err)
	tables, err := htmlquery.QueryAll(parsedHTML, "//table")
	assert.NoError(t, err)
	err = save("file", "testFolder", tables)
	assert.NoError(t, err)
	f, err := os.Open("./testFolder/file.html")
	assert.NoError(t, err)
	content, err := ioutil.ReadAll(f)
	assert.Equal(t, "<table></table>", string(content))
	assert.NoError(t, os.RemoveAll("./testFolder"))
}
