import pandas as pd
from datetime import datetime
from openpyxl import load_workbook
import math
import pathlib
import sys
import os

def read_data(path):
    try:
        data = pd.read_excel(path, engine='openpyxl')
        return data
    except Exception as excep:
        sys.stderr.write("Não foi possível ler o arquivo: " +
                         path + '. O seguinte erro foi gerado: ' + excep)
        os._exit(1)

# Strange way to check nan. Only I managed to make work
# Source: https://stackoverflow.com/a/944712/5822594
def isNaN(string):
    return string != string

def get_begin_row(rows, begin_string):
    begin_row = 0
    for row in rows:
        begin_row += 1
        if row[0] == begin_string:
            break

    # We need to continue interate until wee a value that is not
    # whitespace. That happen due to the spreadsheet formatting.
    while isNaN(rows[begin_row][0]):
        begin_row += 1

    return begin_row

def parse_employees(file_name):
    rows = read_data(file_name).to_numpy()
    print(rows)
    # begin_string = "Matrícula"
    # end_string = "1  Remuneração do cargo efetivo"
    # begin_row = get_begin_row(rows, begin_string)
    #end_row = get_end_row(rows, begin_row)
    employees = {}
  
    return employees

def parse(file_names):
    employees = {}
    for fn in file_names:
        if 'Verbas Indenizatorias' not in fn:
            # Puts all parsed employees in the big map
            employees.update(parse_employees(fn))

    # try:
    #     for fn in file_names:
    #         if 'Verbas Indenizatorias' in fn:
    #             update_employee_indemnity(fn, employees)
    # except KeyError as e:
    #     sys.stderr.write('Registro inválido ao processar verbas indenizatórias: {}'.format(e))
    #     os._exit(1)

    return list(employees.values())