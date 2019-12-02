package main

import (
	"encoding/json"
	"fmt"

	"github.com/knieriem/odf/ods"
)

var mapping = map[string]string{
	"remuneracoes": "a",
}

// Parser parses the ods tables.
func Parser(files []string) error {
	var doc ods.Doc
	for _, file := range files {
		f, err := ods.Open(file)
		if err != nil {
			return fmt.Errorf("ods.Open error(%s): %q", file, err)
		}
		f.ParseContent(&doc)
		json, err := json.MarshalIndent(doc.Table[0].Strings(), "", " ")
		if err != nil {
			return fmt.Errorf("marshalling error")
		}
		fmt.Printf("%s", json)
	}
	return nil
}
