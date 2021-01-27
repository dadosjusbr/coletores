import pandas as pd
from pandas_ods_reader import read_ods
from openpyxl import load_workbook
import math
import sys
import os
import pathlib

cwd = os.getcwd()

def read_data(path):
    if('ods' in path):
        try:
            data = read_ods(cwd + path, 1)
        except Exception as excep:
            sys.stderr('Não foi possível fazer a leitura do arquivo: ' + path +'e o seguinte error foi gerado:' + str(excep))
            os._exit(1)
    else:
        try:
             data = pd.read_excel(cwd + path, engine='openpyxl')
        except Exception as excep:
            sys.stderr('Não foi possível fazer a leitura do arquivo: ' + path +'e o seguinte error foi gerado:' + str(excep))
            os._exit(1)

    return data

# Strange way to check nan. Only I managed to make work
# Source: https://stackoverflow.com/a/944712/5822594
def isNaN(string):
    return string != string

def get_begin_row(rows):
    begin_row = 0

    # We need to continue interate until wee a value that is not
    # None or NaN. That happen due to the spreadsheet formatting.
    while rows[begin_row][0] == None or isNaN(rows[begin_row][0]):
        begin_row += 1

    return begin_row


def get_end_row(rows, begin_row, file_name):
    end_row = begin_row 
    array_len = len(rows)
   
    #There are variations at the end of the worksheets. Different conditions are needed
    if 'Pensionistas' in file_name:
        end_row = array_len
    elif(type(rows[array_len-1][0]) == float):
        end_row = array_len
    else: 
        # Then keep moving until find a different type of float.  
        while type(rows[end_row][0]) == float:
            end_row += 1
       
    end_row -= 1
    return end_row 

def type_employee(fn):
    if 'Membros' in fn:
        return 'membro'
    if 'Servidores' in fn:
        return 'servidor'
    if 'Pensionistas' in fn:
        return 'pensionista'
    if 'Colaboradores' in fn:
        return 'colaborador'
    raise ValueError('Tipo de inválido de funcionário público: ' + fn)

# Adjust existing spreadsheet variations
def format_value(element):
    if(element == None):
        return 0.0
    if(type(element) == str and '-' in element):
        return 0.0
    return element

# Parser for the months from July 2019 to November 2020 
def parse_employees(file_name):
    rows = read_data(file_name).to_numpy()
    begin_row = get_begin_row(rows)
    end_row = get_end_row(rows, begin_row, file_name)

    typeE = type_employee(file_name)
    activeE = 'inativos' not in file_name 
    employees = {}
    curr_row = 0
    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue
    
        employees[str(int(row[0]))] = {
            'reg': str(int(row[0])),
            'name': row[1],
            'role': row[2],
            'type': typeE,
            'workplace': row[3],
        
            'active': activeE,
            "income":
            {
                'total': row[12],
                # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                'wage': format_value(row[4]) + format_value(row[5]),
                'perks': {
                    'total': row[11],
                },
                'other':
                {  # Gratificações
                    'total': format_value(row[6]) + format_value(row[7]) + format_value(row[8])+ format_value(row[9]),
                    'trust_position': row[6],
                    'others_total': format_value(row[7]) + format_value(row[8]) + format_value(row[9]),
                    'others': {
                        'Gratificação Natalina': row[7],
                        'Férias (1/3 constitucional)': row[8],
                        'Abono de Permanência': row[9],
                    }
                },
            },
            'discounts':
            {  # Discounts Object. Using abs to garantee numbers are positivo (spreadsheet have negative discounts).
                'total': abs(format_value(row[16])),
                'prev_contribution': abs(format_value(row[13])),
                # Retenção por teto constitucional
                'ceil_retention': abs(format_value(row[15])),
                'income_tax':abs(format_value(row[14])),
            }
        }

        curr_row += 1
        if curr_row >= end_row:
            break
    
    
    return employees

def parse(file_names):
    print(file_names)
    employees = {}
    for fn in file_names:
        if 'Verbas Indenizatorias' not in fn and 'Pensionistas' not in fn:
            # Puts all parsed employees in the big map
   
            employees.update(parse_employees(fn))
       

    return list(employees.values())