import pandas as pd
from pandas_ods_reader import read_ods
import pyexcel_ods
from datetime import datetime
import math
import numpy
import utils
import pathlib
import sys
import os

def read_data(path):
    path = './src/' + path
    try:
        data = pd.read_excel(path, engine='odf')
        return data
    except Exception as excep:
        sys.stderr.write("'Não foi possível ler o arquivo: " +
                         path + '. O seguinte erro foi gerado: ' + excep)
        os._exit(1)

def parse_employees(file_name):
    rows = read_data(file_name).to_numpy()
    emps_clean = utils.treat_rows(rows)
    typeE = utils.type_employee(file_name)
    activeE = 'inativos' not in file_name and 'pensionistas' not in file_name
    employees = {}
    curr_row = 0
    for row in emps_clean:
        employees[row[0]] = {
            'reg': row[0],
            'name': row[1],
            'role': row[2],
            'type': typeE,
            'workplace': row[3],
            'active': activeE,
            "income":
            {
                #Soma de todos os recebidos do funcionário
                'total': row[4]+row[5]+row[6]+row[7]+row[8]+row[9]+row[10]+row[11],
                # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                'wage': row[4]+row[5],
                'perks': {
                    'total': row[11],
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
                'total': abs(row[16]),
                'prev_contribution': abs(row[13]),
                # Retenção por teto constitucional
                'ceil_retention': abs(row[15]),
                'income_tax': abs(row[14]),
            }
        }
    return employees

def update_employee_indemnity(file_name, employees):
    rows = read_data(file_name).to_numpy()
    emp_idemnity = utils.treat_rows(rows)
    for row in emp_idemnity:
        emp = employees[row[0]]
        emp['income']['perks'].update({
            'total': sum(row[4:14]),
            'vacation': row[4],
            'food': row[5],
            'pre_school': row[6],
            'transportation': row[7],
            'furniture_transport': row[8],
            'birth_aid': row[9],
            'subsistence': row[10],
            'housing_aid': row[11],
            'pecuniary': row[12],
            'premium_license_pecuniary': row[13],
        })
        emp['income']['other'].update({
            'total': round(emp['income']['other']['total'] + row[15] + row[16] + row[17] + row[18] + row[20] + row[22] + row[23] + row[24] + row[25] + row[26], 3),
            'others_total': round(emp['income']['other']['others_total'] + row[15] + row[16] + row[17] + row[18] + row[20] + row[22] + row[23] + row[24] + row[25] + row[26], 3),
        })
        emp['income']['other']['others'].update({
            'Gratificação de Perícia e Projeto': row[15],
            'Gratificação Exercício Cumulativo de Ofício': row[16],
            'Gratificação Encargo de Curso e Concurso': row[17],
            'Gratificação Local de Trabalho': row[18],
            'Hora Extra': row[20],
            'Adicional Noturno': row[22],
            'Adicional Atividade Penosa': row[23],
            'Adicional Insalubridade': row[24],
            'Outras Verbas Remuneratórias': row[25],
            'Outras Verbas Remuneratórias Retroativas/Temporárias': row[26],

        })
        employees[row[0]] = emp

    return employees

def parse(file_names):
    employees = {}
    for fn in file_names:
        if 'verbas-indenizatorias' not in fn:
            # Puts all parsed employees in the big map
            employees.update(parse_employees(fn))
    try:
        for fn in file_names:
            if 'verbas-indenizatorias' in fn:
                update_employee_indemnity(fn, employees)
    except KeyError as e:
        sys.stderr.write('Registro inválido ao processar verbas indenizatórias: {}'.format(e))
        sys.stderr.write('Mapa de funcionários: {}'.format(employees))
        os._exit(1)

    return list(employees.values())