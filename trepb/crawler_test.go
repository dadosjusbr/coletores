package main

import (
	"io/ioutil"
	"log"
	"os"
	"strings"
	"testing"

	"github.com/antchfx/htmlquery"
	"github.com/stretchr/testify/assert"
	"golang.org/x/net/html"
)

//Test if save saves the correct content to a file at filePath
func Test_save(t *testing.T) {
	table := "<table><tbody><tr><td>éâõ</td></tr></tbody></table>"
	outputFolder := "./testFolder"
	if err := os.Mkdir(outputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		log.Fatalf("Error creating output folder(%s): %q", outputFolder, err)
	}
	filePath := "./testFolder/file.html"

	parsedHTML, err := html.Parse(strings.NewReader(table))
	assert.NoError(t, err)
	tables, err := htmlquery.QueryAll(parsedHTML, "//table")
	assert.NoError(t, err)
	err = save(filePath, tables)
	assert.NoError(t, err)
	f, err := os.Open(filePath)
	assert.NoError(t, err)
	content, err := ioutil.ReadAll(f)
	assert.Equal(t, table, string(content))
	assert.NoError(t, os.RemoveAll(outputFolder))
}
