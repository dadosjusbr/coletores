import pyexcel_ods
import pyexcel_xls
import pandas as pd
import math
import sys
import os
import pathlib
import numpy as np

cwd = os.getcwd()

def read_data(path):
    if('ods' in path):
        try:
            data = pyexcel_ods.get_data(cwd + path)
        except Exception as excep:
            sys.stderr('Não foi possível fazer a leitura do arquivo: ' + path +'e o seguinte error foi gerado:' + str(excep))
            os._exit(1)
    else:
        try:
            data = pyexcel_xls.get_data(cwd + path)
        except Exception as excep:
            sys.stderr('Não foi possível fazer a leitura do arquivo: ' + path +'e o seguinte error foi gerado:' + str(excep))
            os._exit(1)
    #print(data)
    return data

def parse_employees(file_name):
    rows = np.asarray(read_data(file_name))

    # begin_string = "MATRÍCULA"
    # begin_row = get_begin_row(rows, begin_string)
    # end_row = get_end_row(rows, begin_row)

    # typeE = type_employee(file_name)
    # activeE = 'inativos' not in file_name and 'Pensionistas' not in file_name
    # employees = {}
    # curr_row = 0
    # for row in rows:
    #     if curr_row < begin_row:
    #         curr_row += 1
    #         continue

    #     employees[row[0]] = {
    #         'reg': row[0],
    #         'name': row[1],
    #         'role': row[2],
    #         'type': typeE,
    #         'workplace': row[3],
    #         'active': activeE,
    #         "income":
    #         {
    #             'total': row[12],
    #             # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
    #             'wage': row[4]+row[5],
    #             'perks': {
    #                 'total': row[11],
    #             },
    #             'other':
    #             {  # Gratificações
    #                 'total': row[6] + row[7] + row[8]+row[9],
    #                 'trust_position': row[6],
    #                 'others_total': row[7]+row[8]+row[9],
    #                 'others': {
    #                     'Gratificação Natalina': row[7],
    #                     'Férias (1/3 constitucional)': row[8],
    #                     'Abono de Permanência': row[9],
    #                 }
    #             },
    #         },
    #         'discounts':
    #         {  # Discounts Object. Using abs to garantee numbers are positivo (spreadsheet have negative discounts).
    #             'total': abs(row[16]),
    #             'prev_contribution': abs(row[13]),
    #             # Retenção por teto constitucional
    #             'ceil_retention': abs(row[15]),
    #             'income_tax': abs(row[14]),
    #         }
    #     }

    #     curr_row += 1
    #     if curr_row >= end_row:
    #         break

    return {'Sex': 'female', 'Age': 7, 'Name': 'Zara'}

def parse(file_names):
    print('FILES_NAMES')
    print(file_names)
    employees = {}
    for fn in file_names:
        if 'Verbas Indenizatorias' not in fn:
            # Puts all parsed employees in the big map
            print("PARSEE EMPLOYEE")
            print(parse_employees(fn))
            employees.update(parse_employees(fn))
    print("EMPLOYEE")
    print(employees)
    # try:
    #     for fn in file_names:
    #         if 'Verbas Indenizatorias' in fn:
    #             update_employee_indemnity(fn, employees)
    # except KeyError as e:
    #     sys.stderr.write('Registro inválido ao processar verbas indenizatórias: {}'.format(e))
    #     sys.stderr.write('Mapa de funcionários: {}'.format(employees))
    #     os._exit(1)

    return list(employees.values())