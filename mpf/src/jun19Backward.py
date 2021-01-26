import pandas as pd
import pyexcel_ods
from datetime import datetime
import math
import numpy
import utils
import pathlib
import sys
import os

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

def parse_employees(file_name, year, month):
    rows = read_data(file_name, year, month).to_numpy()
    emps_clean = utils.treat_rows(rows)
    typeE = utils.type_employee(file_name)
    activeE = 'inativos' not in file_name and 'pensionistas' not in file_name
    employees = {}
    curr_row = 0
    for row in emps_clean:
        employees[row[0]] = {
            'name': str(row[0]),
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