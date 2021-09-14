import pandas as pd
import sys
import os
from parser_remuneration import parse
from update_remuneration import UpdateRemuneration


def openHTML(file):
    try:
        data = pd.read_html(file)
        data = data[0].to_numpy()
        return data
    except Exception as excep:
        print(
            f"Não foi possível ler o arquivo: {file}. O seguinte erro foi gerado: {str(excep)}")
        os._exit(1)


def parse(data):
    remuneration = openHTML(data[0])
    # for row in rows:
    #     print(row)

    # indemnization = openHTML(data[1])
    employes_remuneration = parse(remuneration)
    # employes_update = UpdateRemuneration(employes_remuneration, indemnization).update()
    return list(employes_remuneration.values())
