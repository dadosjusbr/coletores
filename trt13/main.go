package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"

	"github.com/joho/godotenv"
)

func main() {
	if err := godotenv.Load(); err != nil {
		log.Fatal("Error loading .env file")
	}

	month := flag.Int("mes", 0, "Mês a ser analisado")
	year := flag.Int("ano", 0, "Ano a ser analisado")

	outputFolder := os.Getenv("OUTPUT_FOLDER")
	flag.Parse()
	if *month == 0 || *year == 0 {
		log.Fatalf("Month or year not provided. Please provide those to continue. --mes={} --ano={}\n")
	}
	if outputFolder == "" {
		outputFolder = "./output"
	}

	if err := os.Mkdir(outputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		log.Fatalf("Error creating output folder(%s): %q", outputFolder, err)
	}
	filePath := fmt.Sprintf("%s/remuneracoes-trt13-%02d-%04d.json", outputFolder, *month, *year)

	if err := crawl(filePath, *month, *year); err != nil {
		log.Fatalf("Crawler error(%02d-%04d): %q", *month, *year, err)
	}

	records, err := parse(filePath)
	if err != nil {
		log.Fatalf("Parser error(%02d-%04d) - %s: %q", *month, *year, filePath, err)
	}

	employees, err := json.MarshalIndent(records, "\n", "  ")
	if err != nil {
		log.Fatalf("JSON marshaling error: %q", err)
	}
	fmt.Printf("%s", employees)
}
