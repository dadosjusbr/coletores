import pandas as pd
import sys, os
import parser_remuneration
import update_remuneration

def openCsv(file):
    try:
        data = pd.read_csv(file)
        return data
    except Exception as excep:
        sys.stderr.write(f"Não foi possível ler o arquivo: {file}. O seguinte erro foi gerado: {str(excep)}")
        os._exit(1)

def parse(data, year):
    remuneration = openCsv(data[0])
    employes_remuneration = parser_remuneration.parse(remuneration)
    if year == '2018':
        return list(employes_remuneration.values())
    indemnization = openCsv(data[1])
    employes_update = update_remuneration.update(employes_remuneration, indemnization)
    return list(employes_update.values())
