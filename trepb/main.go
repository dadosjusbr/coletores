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
	flag.Parse()
	if *month == 0 || *year == 0 || cpf == "" || name == "" {
		log.Fatalf("Need all arguments to continue, please try again\n")
	}

	if err := crawl(name, cpf, *month, *year); err != nil {
		log.Fatalf("Crawler error: %q", err)
	}

	records, err := parser(*month, *year)
	if err != nil {
		log.Fatalf("Parser error: %q", err)
	}

	jsonInfo, err := json.Marshal(records)
	if err != nil {
		log.Fatalf("JSON marshaling error: %q", err)
	}
	fmt.Printf(`{"employees":%s}`, jsonInfo)
}
