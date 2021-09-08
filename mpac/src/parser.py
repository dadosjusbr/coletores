import pandas as pd
import sys, os
import parser_remuneration

def openOds(file):
    try:
        data = pd.read_excel(file, engine="odf").to_numpy()
        return data
    except Exception as excep:
        print(excep)
        os._exit(1)

def parse(file_names):
    print(file_names[0])
    remuneration = openOds(file_names[0])
    employes_remuneration = parser_remuneration.parse(remuneration)
    return list(employes_remuneration.values())

