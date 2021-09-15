import pandas as pd
import sys
import os
import parser_remuneration 
import update_remuneration
import table

def read_html(path):
    try:
        data = pd.read_html(path,decimal=',') # Coloca uma vírgula nas casas decimais
        data = data[0]
        return data

    except Exception as excep:
        print(f'Não foi possível ler o arquivo: {path}. O seguinte erro foi gerado: {str(excep)}')
        os._exit(1)

def parse(data):
    remuneration = read_html(data[0])
    indemnization = read_html(data[1])
    #Parsing data
    remuneration = remuneration.to_numpy()
    indemnization = indemnization.to_numpy()

    employes_remuneration = parser_remuneration.parse(remuneration)
    employes_update = update_remuneration.update(employes_remuneration, indemnization)
    return list(employes_update.values())
    
