import pandas as pd
import sys, os
from parser_remuneration import Remuneration
from update_remuneration import UpdateRemuneration
# import update_remuneration

def openCsv(file):
    try:
        data = pd.read_csv(file)
        return data
    except Exception as excep:
        sys.stderr.write(f"Não foi possível ler o arquivo: {file}. O seguinte erro foi gerado: {str(excep)}")
        os._exit(1)

def openXls(file):
    try:
        data = pd.read_excel(file, engine='xlrd').to_numpy()
        return data
    except Exception as excep:
        sys.stderr.write(f"Não foi possível ler o arquivo: {file}. O seguinte erro foi gerado: {str(excep)}")
        os._exit(1)

def parse(data):
    remuneration = openCsv(data[0])
    indemnization = openXls(data[1])
    employes_remuneration = Remuneration(remuneration).parser()
    employes_update = UpdateRemuneration(employes_remuneration, indemnization).update()
    return list(employes_update.values())
