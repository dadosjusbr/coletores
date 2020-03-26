package main

import (
	"flag"
	"fmt"
	"os"
	"time"
)

var gitCommit string

func main() {
	fmt.Println("gitCommit: ", gitCommit)
	month := flag.Int("mes", 0, "Mês a ser analisado")
	year := flag.Int("ano", 0, "Ano a ser analisado")
	flag.Parse()
	if *month == 0 || *year == 0 {
		logError("month or year not provided. Please provide those to continue. --mes={} --ano={}\n")
		os.Exit(1)
	}
	if *year < 2011 {
		logError("years before 2011 are not supported yet :(")
		os.Exit(1)
	}
	if *month < 1 || *month > 12 || *month <= 0 {
		logError("invalid month value. Give values between 1 and 12")
		os.Exit(1)
	}
	if *year <= 0 {
		logError("invalid year value. Give years from and above 2011")
		os.Exit(1)
	}
	outputFolder := os.Getenv("OUTPUT_FOLDER")
	if outputFolder == "" {
		outputFolder = "./output"
	}
	if err := os.Mkdir(outputFolder, os.ModePerm); err != nil && !os.IsExist(err) {
		logError("error creating output folder(%s): %q", outputFolder, err)
		os.Exit(1)
	}
	paths, err := Crawl(outputFolder, *month, *year, baseURL)
	if err != nil {
		logError("error on crawling: ", err.Error())
		os.Exit(1)
	}
	fmt.Println(paths)
}

func logError(format string, args ...interface{}) {
	time := fmt.Sprintf("%s: ", time.Now().Format(time.RFC3339))
	fmt.Fprintf(os.Stderr, time+format+"\n", args...)
}
