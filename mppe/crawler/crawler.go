package crawler

import (
	"fmt"
	"sync"
)

// Crawler defines how the crawlers should work
type crawler interface {
	crawl(outputPath string, month, year int) (string, error)

	getURLForYear(year int) string

	getPatternToSearch(month, year int) string

	getURLToDownloadSheet(year int, fileCode string) string

	getFileName(outputFolder string, month, year int) string
}

var (
	//Crawlers is the registry
	crawlers = map[string]crawler{
		"exerciciosAnteriores":          newPreviousYears(),
		"indenizacoesEOutrosPagamentos": newIndemnityAndOtherPayments(),
	}
)

// Crawl get all files on internet, download then and return the paths
func Crawl(outputPath string, month, year int) ([]string, error) {
	paths := make([]string, 8)

	pathsChannel := make(chan string, 10)
	errChannel := make(chan error, 10)

	var wg sync.WaitGroup

	for _, c := range crawlers {
		wg.Add(1)

		go func(outputPath string, month, year int, cr crawler) {
			defer wg.Done()

			path, err := cr.crawl(outputPath, month, year)

			if err != nil {
				errChannel <- err
			}

			pathsChannel <- path

		}(outputPath, month, year, c)
	}

	wg.Wait()

	close(errChannel)
	close(pathsChannel)

	for err := range errChannel {
		if err != nil {
			fmt.Println("o error: ", err.Error())
			return nil, err
		}
	}

	for path := range pathsChannel {
		paths = append(paths, path)
	}

	return paths, nil
}
