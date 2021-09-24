import sys
import pandas as pd
import parser_remuneration 
import update_remuneration
import csv

def read_html(path, head = None):
    try:
        data = pd.read_html(path, header=head, decimal=',') # Coloca uma vírgula nas casas decimais
        data = data[0]
        return data

    except Exception as excep:
        sys.exit(f'Não foi possível ler o arquivo: {path}. O seguinte erro foi gerado: {str(excep)}')


def writer_csv_indemnization(output_patch, indemnization):
    file_csv = open(output_patch, 'w')
    writer_file_csv = csv.writer(file_csv)
    writer_file_csv.writerow(indemnization)
    for row in indemnization.to_numpy():
        writer_file_csv.writerow(row)
    file_csv.close()


def parse(data):
    remuneration = read_html(data[0])
    indemnization = read_html(data[1], head = 1)
    output_patch = data[1].replace('.html', '.csv')

    writer_csv_indemnization(output_patch, indemnization)
    
    remuneration = remuneration.to_numpy()
    employes_remuneration = parser_remuneration.parse(remuneration)
    employes_update = update_remuneration.update(employes_remuneration, output_patch)
    return list(employes_update.values())
