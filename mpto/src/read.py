import pandas as pd
import sys
import os

# Read data downloaded from the crawler
def xls(path):
    print(path)
    try:
        data = pd.read_excel(path, engine=None)
        return data
    except Exception as excep:
        sys.stderr.write(
            "'Não foi possível ler o arquivo: "
            + path
            + ". O seguinte erro foi gerado: "
            + excep
        )
        os._exit(1)