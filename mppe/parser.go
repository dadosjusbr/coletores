package main

// it cuts off month, year and extension from name
// to get file name
func getTypeOfFile(fileName string) string {
	fileSize := len(fileName)
	name := fileName[0 : fileSize-13]
	return name
}
