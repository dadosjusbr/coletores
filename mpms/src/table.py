import pandas as pd
import sys, os


# Para ler arquivos excel
def read_xlsx(file):
    try:
        table_excel = pd.read_excel(file, engine='openpyxl').to_numpy()
    except Exception as excep:
        sys.stderr(
            f"Não foi possível fazer a leitura do arquivo: {file}. Erro gerado: {str(excep)}"
        )
        os._exit(1)
    
    return table_excel


def is_nan(string):
    return string != string


# Usado para limpar a tabela, remover vírgulas de valores e colocar ponto, e onde tem nan colocar 0.0,
# caso for número
def clean_cell(element):

    if element < 0.01:
        return 0.0

    if is_nan(element):
        return 0.0

    # A value was found with incorrect formatting. (3,045.99 instead of 3045.99)
    if type(element) == str:
        if "." in element and "," in element:
            element = element.replace(".", "").replace(",", ".")       
        elif "," in element:
            element = element.replace(",", ".")

    return round(float(element),2)