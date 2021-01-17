import pandas as pd
from pandas_ods_reader import read_ods
import pyexcel_ods
from datetime import datetime
import math
import numpy
import pathlib
import sys
import os
nan = float('nan')

def read_data(path, year, month):
    if year == 2019 and month == 6:
        eng = 'odf'
    else:
        eng = 'xlrd'
    path = './src/' + path
    try:
        data = pd.read_excel(path, engine=eng)
        return data
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
    for row in rows:
        begin_row += 1
        if isinstance(row[0], str) and begin_string in row[0]:
            break
    # We need to continue interate until wee a value that is not
    # whitespace. That happen due to the spreadsheet formatting.
    while isNaN(rows[begin_row][0]):
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
        if isinstance(row[0], str) and end_string in row[0]:
            break
        if isNaN(row[0]):
            break
        end_row += 1
    return end_row

def type_employee(fn):
    if 'membros' in fn:
        return 'membro'
    if 'servidores' in fn:
        return 'servidor'
    if 'pensionistas' in fn:
        return 'pensionista'
    if 'colaboradores' in fn:
        return 'colaborador'
    raise ValueError('Tipo de inválido de funcionário público: ' + fn)

def treat_rows(rows): 
  emps_clean = []
  begin_string = "Matrícula"
  end_string = "TOTAL GERAL"
  begin_row = get_begin_row(rows, begin_string)
  end_row = get_end_row(rows, begin_row, end_string)
  for row in rows:
    emp_clean = [x for x in row if str(x) != 'nan']
    emps_clean.append(emp_clean)
  return emps_clean[begin_row:end_row]


def parse_employees(file_name, year, month):
    rows = read_data(file_name, year, month).to_numpy()
    emps_clean = treat_rows(rows)
    typeE = type_employee(file_name)
    activeE = 'inativos' not in file_name and 'pensionistas' not in file_name
    employees = {}
    curr_row = 0
    for row in emps_clean:
        employees[row[0]] = {
            'name': row[0],
            'role': row[1],
            'type': typeE,
            'workplace': row[3],
            'active': activeE,
            "income":
            {
                #Soma de todos os recebidos do funcionário
                'total': row[4]+row[5]+row[6]+row[7]+row[8]+row[9]+row[16],
                # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                'wage': row[4]+row[5],
                'perks': {
                    'total': row[16],
                },
                'other':
                {  # Gratificações e remuneraçoes temporárias
                    'total': row[6] + row[7] + row[8]+row[9],
                    'trust_position': row[6],
                    'others_total': row[7]+row[8]+row[9],
                    'others': {
                        'Gratificação Natalina': row[7],
                        'Férias (1/3 constitucional)': row[8],
                        'Abono de Permanência': row[9],
                    }
                },
            },
            'discounts':
            {  # Discounts Object. Using abs to garantee numbers are positivo (spreadsheet have negative discounts).
                'total': abs(row[11]+ row[12] + row[13]),
                'prev_contribution': abs(row[11]),
                # Retenção por teto constitucional
                'ceil_retention': abs(row[13]),
                'income_tax': abs(row[12]),
            }
        }
    return employees

def parse(file_names, year, month):
    employees = {}
    for fn in file_names:
            # Puts all parsed employees in the big map
            employees.update(parse_employees(fn, year, month))
    return list(employees.values())