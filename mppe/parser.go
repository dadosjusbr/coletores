package main

// it returns the employee type
func getType(documentIdentification string) string {
	switch documentIdentification {
	case "proventos-de-todos-os-membros-inativos":
		return "membro"
	case "proventos-de-todos-os-servidores-inativos":
		return "servidor"
	case "remuneracao-de-todos-os-membros-ativos":
		return "membro"
	case "remuneracao-de-todos-os-servidores-atuvos":
		return "servidor"
	case "valores-percebidos-por-todos-os-colaboradores":
		return "colaborador"
	case "valores-percebidos-por-todos-os-pensionistas":
		return "pensionista"
	default:
		return "indefinido"
	}
}

// it checks if the document is of active members or not
func isActive(documentIdentification string) bool {
	switch documentIdentification {
	case "proventos-de-todos-os-membros-inativos":
		return false
	case "proventos-de-todos-os-servidores-inativos":
		return false
	case "verbas-referentes-a-exercicios-anteriores":
		return false
	case "verbas-indenizatorias-e-outras-remuneracoes-temporarias":
		return false
	case "valores-percebidos-por-todos-os-pensionistas":
		return false
	default:
		return true
	}
}

// it cuts off month, year and extension from name
// to get file name
func getFileDocumentation(fileName string) string {
	fileSize := len(fileName)
	name := fileName[0 : fileSize-13]
	return name
}
