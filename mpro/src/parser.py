import pandas as pd
import sys, os
import parser_remuneration
import update_remuneration

def openCsv(file):
    try:
        data = pd.read_csv(file)
        return data
    except Exception as excep:
        sys.stderr.write(
            "'Não foi possível ler o arquivo: "
            + file
            + ". O seguinte erro foi gerado: "
            + excep
        )
        os._exit(1)

def parse(file_names):
    remuneration = openCsv(file_names[0])
    indemnization = openCsv(file_names[1])
    employes_remuneration = parser_remuneration.parse(remuneration)
    
    employes_update = update_remuneration.update(employes_remuneration, indemnization)
    return list(employes_update.values())

