package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/joho/godotenv"
)

func main() {
	if err := godotenv.Load(); err != nil {
		log.Fatal("Error loading .env file")
	}

	month := flag.Int("mes", 0, "Mês a ser analisado")
	year := flag.Int("ano", 0, "Ano a ser analisado")

	flag.Parse()

	if *month == 0 || *year == 0 {
		logError("Month or year not provided. Please provide those to continue. --mes={} --ano={}\n")
		os.Exit(1)
	}

	if *year < 2011 {
		logError("Years before 2011 are not supported yet :(")
		os.Exit(1)
	}

	if *month < 1 || *month > 12 {
		logError("Invalid month value. Give values between 1 and 12")
		os.Exit(1)
	}

	outputFolder := os.Getenv("OUTPUT_FOLDER")

	if outputFolder == "" {
		outputFolder = "./output"
	}

	if err := os.Mkdir(outputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		logError("Error creating output folder(%s): %q", outputFolder, err)
		os.Exit(1)
	}

	paths, err := Crawl(outputFolder, *month, *year)
	if err != nil {
		logError("Error on crawling: ", err.Error())
		os.Exit(1)
	}

	fmt.Println(paths)
}

func logError(format string, args ...interface{}) {
	time := fmt.Sprintf("%s: ", time.Now().Format(time.RFC3339))
	fmt.Fprintf(os.Stderr, time+format+"\n", args...)
}