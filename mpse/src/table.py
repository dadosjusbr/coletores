def is_nan(string):
    return string != string


def get_begin_row(data, begin_string):
    begin_row = 0

    for row in data:
        begin_row += 1
        if(row[0] == begin_string):
            break

    while is_nan(data[begin_row][0]):
        begin_row += 1

    return begin_row


def get_end_row(data, end_string):
    end_row = 0

    for row in data:
        end_row += 1
        if row[0] == end_string:
            break
    return end_row - 2


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