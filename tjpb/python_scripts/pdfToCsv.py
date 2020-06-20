import camelot
import sys
import csv
import glob
import os

def pdfToCsv(path):
    bg = False
    if "servidores" in path:
        bg = True
    tables = camelot.read_pdf(path, pages="1-end", flavor='lattice', process_background=bg)
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
    with open (path.replace(".pdf", ".csv"), 'x') as fp: 
        fp.write(newCSV)

def fixCSV(path):
    err = 0
    ok = 0
    with open (path.replace(".pdf", ".csv"), 'r') as fp: 
        for row in csv.reader(fp):
            element = row[0].replace("RENDIMENTOS\n", "").replace("DESCONTOS\n", "").split("\n")
            if len(element) != 16:
                err += 1
            else:
                ok += 1
    print(err, "tamanho errado")
    print(ok, "tamanho certo")


def main():
    path = sys.argv[1]
    print(path)
    if not ".pdf" in path:
        return 1
    pdfToCsv(path)
    joinCSVs(path)
    fixCSV(path)


if __name__ == '__main__':
    main()