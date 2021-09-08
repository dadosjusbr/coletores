def is_nan(string):
    return string != string


# Usado para pegar a primeira linha das tabelas que tem a coluna 0 
def get_begin_row(data, begin_string):
    begin_row = 0
    for row in data:
        begin_row += 1
        if(str(row[0]).lower() == begin_string):
            break

    while is_nan(data[begin_row][0]):
        begin_row += 1

    return begin_row 


# Usado para pegar a primeira linha das tabelas que não tem a coluna 0
def get_begin_row_1(data, begin_string):
    begin_row = 0
    for row in data:
        begin_row += 1
        if(str(row[0]).lower()== begin_string):
            break
    print(begin_row)
    while is_nan(data[begin_row][0]):
        begin_row += 1

    return begin_row


def this_nan(value):
    if type(value ) != str:
        return '-'
    return value


def clean_cell(element):
    if is_nan(element):
        return 0.0
    # A value was found with incorrect formatting. (3,045.99 instead of 3045.99)
    if type(element) == str:
        if "." in element and "," in element:
            element = element.replace(".", "").replace(",", ".")       
        elif "," in element:
            element = element.replace(",", ".")

    # return round(float(element),2)
    return element