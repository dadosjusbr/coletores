package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"sync"
)

const (
	baseURL          = "http://pitagoras.mppb.mp.br/PTMP/"
	tipoEstagiarios  = "estagiarios"
	tipoIndenizacoes = "indenizacoes"
)

var (
	tipos = map[string]int{
		"membrosAtivos":         1,
		"membrosInativos":       2,
		"servidoresAtivos":      3,
		"servidoresInativos":    4,
		"servidoresDisponiveis": 5,
		"aposentados":           6,
	}
)

// Crawl retrieves payment files from MPPB.
func Crawl(outputPath string, month, year int) ([]string, error) {
	var files []string
	pathChan := make(chan string, 10)
	errChan := make(chan error, 10)
	var wg sync.WaitGroup
	for typ, url := range links(baseURL, month, year) {
		wg.Add(1)
		go func(typ, url string) {
			defer wg.Done()
			filePath := fmt.Sprintf("%s/%s-%d-%d.ods", outputPath, typ, month, year)
			f, err := os.Create(filePath)
			if err != nil {
				errChan <- fmt.Errorf("error creating file(%s):%q", filePath, err)
			}
			defer f.Close()
			if err := download(url, f); err != nil {
				errChan <- fmt.Errorf("error while downloading content: %q", err)
			}
			pathChan <- filePath
		}(typ, url)
	}
	wg.Wait()
	close(errChan)
	close(pathChan)

	for err := range errChan {
		if err != nil {
			return nil, err
		}
	}

	for path := range pathChan {
		files = append(files, path)
	}

	return files, nil
}

// Generate endpoints able to download
func links(baseURL string, month, year int) map[string]string {
	links := make(map[string]string)
	links[tipoEstagiarios] = fmt.Sprintf("%sFolhaPagamentoEstagiarioExercicioMesOds?exercicio=%d&mes=%d", baseURL, year, month)
	links[tipoIndenizacoes] = fmt.Sprintf("%sFolhaVerbaIndenizRemTemporariaOds?mes=%d&exercicio=%d&tipo=", baseURL, month, year)
	for t, id := range tipos {
		links[t] = fmt.Sprintf("%sFolhaPagamentoExercicioMesNewOds?mes=%d&exercicio=%d&tipo=%d", baseURL, month, year, id)
	}
	return links
}

func download(url string, w io.Writer) error {
	resp, err := http.Get(url)
	if err != nil {
		return fmt.Errorf("error downloading file:%q", err)
	}
	defer resp.Body.Close()
	if _, err := io.Copy(w, resp.Body); err != nil {
		return fmt.Errorf("error copying response content:%q", err)
	}
	return nil
}
