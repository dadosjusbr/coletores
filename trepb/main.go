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
	name := os.Getenv("NAME")
	cpf := os.Getenv("CPF")
	outputFolder := os.Getenv("OUTPUT_FOLDER")
	flag.Parse()
	if *month == 0 || *year == 0 || cpf == "" || name == "" {
		log.Fatalf("Need all arguments to continue, please try again.\n")
	}

	if err := crawl(outputFolder, name, cpf, *month, *year); err != nil {
		log.Fatalf("Crawler error: %q", err)
	}

	records, err := parse(*month, *year, outputFolder)
	if err != nil {
		log.Fatalf("Parser error: %q", err)
	}

	employees, err := json.MarshalIndent(records, "\n", "  ")
	if err != nil {
		log.Fatalf("JSON marshaling error: %q", err)
	}
	fmt.Printf("%s", employees)
}
