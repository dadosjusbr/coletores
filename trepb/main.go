package main

import (
	"flag"
	"log"
)

func main() {
	month := flag.Int("mes", 0, "Mês a ser analisado")
	year := flag.Int("ano", 0, "Ano a ser analisado")
	name := flag.String("nome", "", "Used for login purposes")
	cpf := flag.String("cpf", "", "used for login purpose. format xxx.xxx.xxx-xx")
	flag.Parse()
	if *month == 0 || *year == 0 || *cpf == "" || *name == "" {
		log.Fatalf("Need all arguments to continue, please try again\n")
	}

	crawl(*name, *cpf, *month, *year)
}
