# After extracting the data, we need to delete the 'nan' fields, 
# resulting in lists with only valid data.
# Ex: [12345, Maria, nan, nan, 29000] -> [12345, Maria, 29000]
def treat_rows(path): 
    emps_clean = []
    for row in path:
        emp_clean = [x for x in row if str(x) != 'nan']
        if emp_clean and (str(emp_clean[0]).isdigit() and len(str(emp_clean[0])) > 2):  # Delete placeholder fields | Ex: ['Página 5']
            emps_clean.append(emp_clean)

    return emps_clean


def begin_row(rows):
    begin_string = "MATRÍCULA"
    begin_row = 0
    for row in rows:
        begin_row += 1
        if row[0] == begin_string:
            break
    # We need to continue interate until wee a value that is not
    # whitespace. That happen due to the spreadsheet formatting.
    while utils.is_nan(rows[begin_row][0]):
        begin_row += 1
    return begin_row


def end_row(rows, begin_row):
    end_row = 0
    for row in rows:
        # First goes to begin_row.
        if end_row < begin_row:
            end_row += 1
            continue
        # Then keep moving until find a blank row.
        if utils.is_nan(row[0]):
            break
        end_row += 1
    end_row -= 1
    return end_row
