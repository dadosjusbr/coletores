import pandas as pd
from datetime import datetime
from openpyxl import load_workbook
import math
import pathlib
import sys
import os

# Read data downloaded from the crawler


def read_data(path):
    try:
        data = pd.read_excel(pathlib.Path('./' + path), engine='openpyxl')
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
        if row[0] == begin_string:
            break

    # We need to continue interate until wee a value that is not
    # whitespace. That happen due to the spreadsheet formatting.
    while isNaN(rows[begin_row][0]):
        begin_row += 1

    return begin_row


def get_end_row(rows, end_string):
    end_row = 0
    for row in rows:
        end_row += 1
        if row[0] == end_string:
            break

    return end_row - 3


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


# Used when the employee is not on the indemnity list
def parse_employees(file_name):
    rows = read_data(file_name).to_numpy()

    begin_string = "Matrícula"
    begin_row = get_begin_row(rows, begin_string)

    end_string = "1  Remuneração do cargo efetivo - Subsídio, Vencimento, GAMPU, V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza."
    end_row = get_end_row(rows, end_string)

    typeE = type_employee(file_name)
    activeE = 'inativos' not in file_name and 'Pensionistas' not in file_name
    employees = {}
    curr_row = 0
    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        employees[row[0]] = {
            'reg': row[0],
            'name': row[1],
            'role': row[2],
            'type': typeE,
            'workplace': row[3],
            'active': activeE,
            "income":
            {
                'total': row[12],
                # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                'wage': row[4]+row[5],
                'perks': {
                    'total': row[11],
                },
                'other':
                {  # Gratificações
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

        curr_row += 1
        if curr_row >= end_row:
            break

    return employees


def update_employee_indemnity(file_name, employees):
    rows = read_data(file_name).to_numpy()

    begin_string = "Matrícula"  # word before starting data
    begin_row = get_begin_row(rows, begin_string)

    end_string = '1 Auxílio-alimentação, Auxílio-transporte, Auxílio-Moradia, Ajuda de Custo e outras dessa natureza, exceto diárias, que serão divulgadas no Portal da Transparência, discriminada de forma individualizada.'
    end_row = get_end_row(rows, end_string)
    curr_row = 0

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        emp = employees[row[0]]
        emp['income']['perks'].update({
            'food': row[5],
            'transportation': row[7],
            'birth_aid': row[6],
            'housing_aid': row[4],
        })
        emp['income']['other'].update({
            'total': round(emp['income']['other']['total'] + row[8] + row[9] + row[10] + row[11] + row[12], 3),
            'others_total': round(emp['income']['other']['others_total'] + row[8] + row[9] + row[10] + row[11] + row[12], 3),
        })
        emp['income']['other']['others'].update({
            'INSALUBRIDADE 10%': row[8],
            'ATIVIDADE PENOSA': row[9],
            'SUBSTITUIÇÃO FC/CC': row[10],
            'GRAT ENCARGO CURSO OU CONCURSO': row[11],
            'GECO': row[12],
        })
        employees[row[0]] = emp

        curr_row += 1
        if curr_row >= end_row:
            break

    return employees


def parse(year, month, file_names, crawler_version):
    employees = {}
    for fn in file_names:
        if 'Verbas Indenizatorias' not in fn:
            # Puts all parsed employees in the big map
            employees.update(parse_employees(fn))

    try:
        for fn in file_names:
            if 'Verbas Indenizatorias' in fn:
                update_employee_indemnity(fn, employees)
    except KeyError as e:
        sys.stderr.write('Registro inválido ao processar verbas indenizatórias: {}'.format(e))
        sys.stderr.write('Mapa de funcionários: {}'.format(employees))
        os._exit(1)

    return {
        'agencyID': 'mpm',
        'month': month,
        'year': year,
        'crawler': {
            'id': 'mpm',
            'version': crawler_version,
        },
        'employees': list(employees.values()),
        'timestamp': datetime.now().strftime("%H:%M:%S")
    }
