# Strange way to check nan. Only I managed to make work
# Source: https://stackoverflow.com/a/944712/5822594
def is_nan(string):
    return string != string

def get_begin_row(rows, begin_string):
    begin_row = 0
    for row in rows:
        begin_row += 1
        if isinstance(row[1], str) and begin_string in row[1]:
            break
    # We need to continue interate until wee a value that is not
    # whitespace. That happen due to the spreadsheet formatting.
    while is_nan(rows[begin_row][1]):
        begin_row += 1
    return begin_row

def get_end_row(rows, begin_row, end_string):
    end_row = 0
    for row in rows:
        # First goes to begin_row.
        if end_row < begin_row:
            end_row += 1
            continue
        # Then keep moving until find a blank row.
        if isinstance(row[1], str) and end_string in row[1]:
            break
        end_row += 1
    return end_row

# After extracting the data, we need to delete the 'nan' fields, 
# resulting in lists with only valid data.
# Ex: [Maria, nan, nan, 29000] -> [Maria, 29000]
def treat_rows(rows): 
    emps_clean = []
    begin_string = "Matrícula"
    end_string = "TOTAL GERAL"
    begin_row = get_begin_row(rows, begin_string)
    end_row = get_end_row(rows, begin_row, end_string)
    for row in rows:
        emp_clean = [x for x in row if str(x) != 'nan']
        if emp_clean and (str(emp_clean[0]).isdigit() and len(str(emp_clean[0])) > 2):  # Delete placeholder fields | Ex: ['Página 5']
            emps_clean.append(emp_clean)

    return emps_clean
