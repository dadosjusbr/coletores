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

def parse(data):
    remuneration = read_html(data[0])
    indemnization = read_html(data[1], head = 1)
    output_patch = f'{data[1].replace(".html", "")}.csv'

    # f = csv.writer(open(output_patch,'w'))
    f = open(output_patch, 'w')
    abre = csv.writer(f)
    abre.writerow(indemnization)
    for row in indemnization.to_numpy():
        abre.writerow(row)
    f.close()
    
    remuneration = remuneration.to_numpy()
    employes_remuneration = parser_remuneration.parse(remuneration)
    employes_update = update_remuneration.update(employes_remuneration, output_patch)
    return list(employes_update.values())
    