import camelot
import sys
import glob
import os

def pdfToCsv(path):
    tables = camelot.read_pdf(path, pages="1-end")
    fileName = path.replace(".pdf", ".csv")
    tables.export(fileName, f="csv")
    return 0

def joinCSVs(path):
    fileName = path.replace(".pdf", "")
    all_filenames = [i for i in glob.glob('{}*.{}'.format(fileName, "csv"))]
    newCSV=""
    for file in all_filenames:
        with open(file) as fp: 
            newCSV += fp.read()
        os.remove(file)
    with open (path.replace(".pdf", ".csv"), 'w') as fp: 
        fp.write(newCSV)

def main():
    path = sys.argv[1]
    print(path)
    if not ".pdf" in path:
        return 1
    pdfToCsv(path)
    joinCSVs(path)


if __name__ == '__main__':
    main()
