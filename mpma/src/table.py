def is_nan(string):
    return string != string

def clean_cell(element):
    if is_nan(element):
        return 0.0

    # A value was found with incorrect formatting. (3.045,99 instead of 3045.99)
    if type(element) == str:
        if "." in element and "," in element:
            element = element.replace(".", "").replace(",", ".")       
        elif "." in element:
            element = element.replace(".", "")
    return round(float(element),2)


def test_error(row, value):
    """
        Nesta função, quando der erro de Keyerror, ela vai retornar 0.0, 
        caso não der erro retorna o valor formatado.
    """
    try:
        new_value = clean_cell(row[value])
    except:
        return 0.0
    return new_value