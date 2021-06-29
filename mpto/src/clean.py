import utils

def cell(element):
    # A value was found with incorrect formatting. (3,045.99 instead of 3045.99)
    if utils.is_nan(element):
        return 0.0
    if type(element) == str:
        if "." in element and "," in element:
            element = element.replace(".", "").replace(",", ".")
        elif "," in element:
            element = element.replace(",", ".")

    return float(element)
