import pandas as pd
import sys, os
from parser_remuneration import Remuneration
# import update_remuneration

def openCsv(file):
    try:
        data = pd.read_csv(file)
        return data
    except Exception as excep:
        sys.stderr.write(f"Não foi possível ler o arquivo: {file}. O seguinte erro foi gerado: {str(excep)}")
        os._exit(1)

def openOds(file):
    try:
        data = pd.read_excel(file)
        return data
    except Exception as excep:
        sys.stderr.write(f"Não foi possível ler o arquivo: {file}. O seguinte erro foi gerado: {str(excep)}")
        os._exit(1)

def parse(data):
    remuneration = openCsv(data[0])
    # indemnization = openOds(data[1])
    employes_remuneration = Remuneration(remuneration).parser()
    return list(employes_remuneration.values())
    # employes_update = update_remuneration.update(employes_remuneration, indemnization)
    # return list(employes_update.values())
