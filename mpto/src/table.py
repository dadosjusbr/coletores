import check

# After extracting the data, we need to delete the 'nan' fields, 
# resulting in lists with only valid data.
# Ex: [12345, Maria, nan, nan, 29000] -> [12345, Maria, 29000]
def treat_rows(table): 
    emps_clean = []
    for row in table:
        emp_clean = [x for x in row if str(x) != 'nan']
        if emp_clean and (str(emp_clean[0]).isdigit() and len(str(emp_clean[0])) > 2):  # Delete placeholder fields | Ex: ['Página 5']
            emps_clean.append(emp_clean)

    return emps_clean


# Function to find the first useful row of the table,
# looking for the string "MATRÍCULA".
def begin_row(table):
    begin_string = "MATRÍCULA"
    begin_row = 0
    for row in table:
        begin_row += 1
        if row[0] == begin_string:
            break
    # We need to continue interate until wee a value that is not
    # whitespace. That happen due to the spreadsheet formatting.
    while check.is_nan(table[begin_row][0]):
        begin_row += 1
    return begin_row


# Function to find the last useful row of the table,
# looking for a blank row. 
def end_row(table, begin_row):
    end_row = 0
    for row in table:
        # First goes to begin_row.
        if end_row < begin_row:
            end_row += 1
            continue
        # Then keep moving until find a blank row.
        if check.is_nan(row[0]):
            break
        end_row += 1
    end_row -= 1
    return end_row


def clean_cell(element):
    # A value was found with incorrect formatting. (3,045.99 instead of 3045.99)
    if check.is_nan(element):
        return 0.0
    if type(element) == str:
        if "." in element and "," in element:
            element = element.replace(".", "").replace(",", ".")
        elif "," in element:
            element = element.replace(",", ".")

    return float(element)
