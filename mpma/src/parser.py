import sys
import pandas as pd
import parser_remuneration 
import update_remuneration

def read_html(path):
    try:
        data = pd.read_html(path,decimal=',') # Coloca uma vírgula nas casas decimais
        data = data[0]
        return data

    except Exception as excep:
        sys.exit(f'Não foi possível ler o arquivo: {path}. O seguinte erro foi gerado: {str(excep)}')

def parse(data):
    remuneration = read_html(data[0])
    indemnization = read_html(data[1])
    #Parsing data
    remuneration = remuneration.to_numpy()
    indemnization = indemnization.to_numpy()

    employes_remuneration = parser_remuneration.parse(remuneration)
    employes_update = update_remuneration.update(employes_remuneration, indemnization)
    return list(employes_update.values())
    
