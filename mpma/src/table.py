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