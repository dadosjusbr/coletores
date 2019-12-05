package main

import (
	"flag"
	"log"
	"os"

	"github.com/joho/godotenv"
)

func main() {
	if err := godotenv.Load(); err != nil {
		log.Fatal("Error loading .env file")
	}
	outputFolder := os.Getenv("OUTPUT_FOLDER")

	month := flag.Int("mes", 0, "Mês a ser analisado")
	year := flag.Int("ano", 0, "Ano a ser analisado")
	flag.Parse()

	if *month == 0 || *year == 0 {
		logError("Month or year not provided. Please provide those to continue. --mes={} --ano={}\n")
		os.Exit(1)
	}
	if outputFolder == "" {
		outputFolder = "./output"
	}

	if err := os.Mkdir(outputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		logError("Error creating output folder(%s): %q", outputFolder, err)
		os.Exit(1)
	}

	files, err := Crawl(outputFolder, *month, *year)
	if err != nil {
		logError("Crawler error: %q", err)
		os.Exit(1)
	}

	if err = Parse(files); err != nil {
		logError("Parsing error: %q", err)
	}
}
