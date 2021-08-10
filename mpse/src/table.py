def is_nan(string):
    return string != string

# Usado pra pegar a primeira linha das tabelas normais
def get_begin_row(data, begin_string):
    begin_row = 0

    for row in data:
        begin_row += 1
        if(row[0] == begin_string):
            break

    while is_nan(data[begin_row][0]):
        begin_row += 1

    return begin_row

# Usado pra pegar a primeira linha das tabelas diferentes que começam com um valor "nan"
def get_begin_row_nan(data, begin_string):
    begin_row = 0

    for row in data:
        begin_row += 1
        if(row[1] == begin_string):
            break

    while is_nan(data[begin_row][1]):
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

# Usado pra pegar a última linha das tabelas diferentes que começam com um valor "nan"
def get_end_row_nan(data, end_string):
    end_row = 0

    for row in data:
        end_row += 1
        if row[1] == end_string:
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