package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"

	storage "github.com/dadosjusbr/storage"
)

func parse(filePath string) error {
	resultJSON, err := readJSON(filePath)
	if err != nil {
		return fmt.Errorf("error reading json: %q", err)
	}

	_, err = parseEmployees(resultJSON)
	if err != nil {
		return fmt.Errorf("error parsing employees: %q", err)
	}
	return nil
}

func readJSON(filePath string) (map[string]interface{}, error) {
	jsonFile, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("error trying to open file at (%s) : %q", filePath, err)
	}
	defer jsonFile.Close()

	byteValue, err := ioutil.ReadAll(jsonFile)
	var result map[string]interface{}
	err = json.Unmarshal(byteValue, &result)
	if err != nil {
		return nil, fmt.Errorf("error trying to unmarshal json: %q", err)
	}

	return result, nil
}

func parseEmployees(m map[string]interface{}) ([]storage.Employee, error) {
	mapArray, err := getSliceOfMaps(m, "listaAnexoviiiServidorMagistradoPensionista")
	if err != nil {
		return nil, fmt.Errorf("error trying to retrieve array of categories: %q", err)
	}
	for _, category := range mapArray {
		parseCategory(category)
	}
	return nil, nil
}

func parseCategory(category map[string]interface{}) ([]storage.Employee, error) {
	var role string
	if err := getString(&role, category, "rotuloCabecalho"); err != nil {
		return nil, fmt.Errorf("couldn't find string for role: %q", err)
	}
	fmt.Println(role)

	cMap, err := getSliceOfMaps(category, "listaAnexoviii")
	if err != nil {
		return nil, fmt.Errorf("couldn't find map for category: %q", err)
	}
	fmt.Println(len(cMap))
	return nil, nil
}
