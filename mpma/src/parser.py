import sys
import pandas as pd
import parser_remuneration 
import update_remuneration
import csv

def read_html(path, head = None):
    try:
        # Coloca uma vírgula nas casas decimais.
        data = pd.read_html(path, header = head, decimal=',')
        data = data[0]
        return data
    except Exception as excep:
        sys.exit(f'Não foi possível ler o arquivo: {path}. O seguinte erro foi gerado: {str(excep)}')


def writer_csv_indemnization(output_patch, indemnization):
    file_csv = open(output_patch, 'w')
    writer_file_csv = csv.writer(file_csv)
    # Pega o header do dataframe que foi retornado pelo pandas,
    # e o transforma no header da planilha csv.
    writer_file_csv.writerow(indemnization)
    # Escreve as outras linhas no documento. uso o to_numpy para pegar somente os valores,
    # e não o header.
    for row in indemnization.to_numpy():
        writer_file_csv.writerow(row)
    file_csv.close()


def parse(data):
    remuneration = read_html(data[0])
    # Uso o head=1 para pegar a segunda linha do header e usar ela como header do csv,
    # por conta que ela é mais completa.
    indemnization = read_html(data[1], head = 1)
    # Cria o nome do arquivo csv, removendo a extensão das planilhas em html.
    output_patch = data[1].replace('.html', '.csv')

    writer_csv_indemnization(output_patch, indemnization)
    
    remuneration = remuneration.to_numpy()
    employes_remuneration = parser_remuneration.parse(remuneration)
    employes_update = update_remuneration.update(employes_remuneration, output_patch)
    return list(employes_update.values())
