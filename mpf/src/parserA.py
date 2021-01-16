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

def read_data(path):
    path = './src/' + path
    try:
        data = pd.read_excel(path, engine='odf')
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


def parse_employees(file_name):
    rows = read_data(file_name).to_numpy()
    emps_clean = treat_rows(rows)
    typeE = type_employee(file_name)
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
    emp_idemnity = treat_rows(rows)
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