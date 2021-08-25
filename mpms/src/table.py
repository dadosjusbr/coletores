import pandas as pd;


# Para ler ods
def read_ods(file_ods):
    df = pd.read_excel(file_ods, engine='openpyxl').to_numpy()
    return df


def is_nan(string):
    return string != string


# Usado pra pegar a primeira linha das tabelas
def get_begin_row(data, begin_string):
    begin_row = 0

    for row in data:
        print(row[0])
        if(row[0] == begin_string):
            break
        begin_row += 1
    print(begin_row)
    while is_nan(data[begin_row][0]):
        begin_row += 1

    return begin_row


# Usado pra pegar a última linha das tabelas normais
def get_end_row(data, end_string):
    end_row = 0

    for row in data:
        end_row += 1
        if row[0] == end_string:
            break
    return end_row - 2


# Usado para limpar a tabela, remover vírgulas de valores e colocar ponto, e onde tem nan colocar 0.0,
# caso for número
def clean_cell(element):
    # A value was found with incorrect formatting. (3,045.99 instead of 3045.99)
    if is_nan(element):
        return 0.0

    if type(element) == str:
        if "." in element and "," in element:
            element = element.replace(".", "").replace(",", ".")
        elif "," in element:
            element = element.replace(",", ".")

    return float(element)