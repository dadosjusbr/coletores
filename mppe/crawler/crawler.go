package crawler

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
		"membrosAtivos":                 newActiveMembers(),
		"membrosInativos":               newInactiveMembers(),
		"servidoresAtivos":              newActiveEmployees(),
		"servidoresInativos":            newInactiveEmployees(),
		"pensionista":                   newPensioner(),
		"colaborador":                   newCollaborator(),
		"exerciciosAnteriores":          newPreviousYears(),
		"indenizacoesEOutrosPagamentos": newIndemnityAndOtherPayments(),
	}
)

// Crawl get all files on internet, download then and return the paths
func Crawl(outputPath string, month, year int) ([]string, error) {
	paths := make([]string, 8)

	for _, crawler := range crawlers {

		path, err := crawler.crawl(outputPath, month, year)

		if err != nil {
			return nil, err
		}

		paths = append(paths, path)
	}

	return paths, nil
}
