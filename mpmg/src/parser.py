import os
import math
import pathlib
import sys
import xlrd2
import numpy as np
import pandas as pd
from datetime import datetime
from openpyxl import Workbook, load_workbook
import parser_april20_backward
import parser_may20_forward



def read_data(path):

    try:
        data = pd.read_html(path, decimal=',', thousands='.')
        return data[0]
    except Exception as excep:
        sys.stderr.write("'Não foi possível ler o arquivo: " +
                        path + '. O seguinte erro foi gerado: ' + excep)
        os._exit(1)
    


# Strange way to check nan. Only I managed to make work
# Source: https://stackoverflow.com/a/944712/5822594
def isNaN(string):
    return string != string


def get_begin_row(rows, begin_string):
    begin_row = 0
    if(type(rows[0][1]) == str):
        return begin_row
    else:
        for row in rows:
            
            if row[1] == begin_string:
                begin_row += 1
                break
            begin_row += 1

        # We need to continue interate until wee a value that is not
        # whitespace. That happen due to the spreadsheet formatting.
        while isNaN(rows[begin_row][1]):
            begin_row += 1
        return begin_row


def get_end_row(rows, begin_row, end_string):
    end_row = 0
    if("MPMG" not in rows[0]):
        for row in rows:
            # First goes to begin_row.
            if end_row < begin_row:
                end_row += 1
                continue
            # Then keep moving until find the name TOTAL row.
            if row[0] == end_string:
                end_row -= 1
                break
            end_row += 1
    return end_row 


def parse(month, year, file_names):
    employees = {}
    for fn in file_names:
        if "Verbas Indenizatorias" not in fn:
            # Puts all parsed employees in the big map
            if (int(year) < 2020) or (int(month) <= 4 and year == "2020"):
                employees.update(parser_april20_backward.parse_employees(fn))
            else:
                employees.update(parser_may20_forward.parse_employees(fn))
    try:
        for fn in file_names:
            if "Verbas Indenizatorias" in fn:
                if (int(year) < 2020) or (int(month) <= 4 and year == "2020"):
                    parser_april20_backward.update_employee_indemnity(fn, employees)
                else:
                    parser_may20_forward.update_employee_indemnity(fn, employees)

    except KeyError as e:
        sys.stderr.write(
            "Registro inválido ao processar verbas indenizatórias: {}".format(e)
        )
        os._exit(1)
    return list(employees.values())
