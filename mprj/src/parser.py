import pandas as pd
from datetime import datetime
import math
import pathlib
import sys
import os


#Lê os dados baixados pelo crawler
def read_data(path):
    try:
        data = pd.read_excel(pathlib.Path('./' + path), engine= 'odf')
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
    begin_row  = 0
    for row in rows:
        begin_row += 1
        if row[0] == begin_string:
            break
    #Continua interando até encontrarmos um valor que não seja string em 
    #branco. Isto ocorre pelo formato da planilha
    while isNaN(rows[begin_row][0]):
        begin_row += 1

    return begin_row

def get_end_row(rows, begin_row):
    end_row = 0
    for row in rows:
        # Primeiro vamos ao row inicial
        if end_row < begin_row:
            end_row += 1
            continue 
        # Continuamos movendo até achar um row em branco
        if isNaN(row[0]):
            break
        end_row += 1
    
    return end_row

def type_employee(fn):
    if 'MATIV' in fn or 'MINAT' in fn:
        return 'membro'
    if 'SATIV' in fn or 'SINAT' in fn:
        return 'servidor'
    if 'PENSI' in fn:
        return 'pensionista'
    if 'COLAB' in fn:
        return 'colaborador'
    raise ValueError('Tipo inválido de funcionário público: ' + fn)

def clean_currency(value):
    if isinstance(value, str):
        return value.replace('R$', '').replace('.', '').replace(',', '.').replace(' ', '')
    return value

def clean_df(data):
    for col in data.columns[4:]:
        data[col] = data[col].apply(clean_currency)

def clean_colab_df(data):
    for col in data.columns[2:5]:
        data[col] = data[col].apply(clean_currency)

def parse_employees(file_name):
    rows = read_data(file_name)
    clean_df(rows)
    rows = rows.to_numpy()

    begin_string = 'Matrícula'
    begin_row  = get_begin_row(rows, begin_string)
    end_row = get_end_row(rows, begin_row)

    typeE = type_employee(file_name)
    activeE = 'INAT' not in file_name and "PENSI" not in file_name
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
                'total':float(row[12]),
                'wage': float(row[4]) + float(row[5]),
                'perks':{
                    'total': float(row[11]),
                },
                'other': 
                { #Gratificações
                    'total': float(row[6]) + float(row[7]) + float(row[8]) + float(row[9]),
                    'trust_position': float(row[6]),
                    'others_total': float(row[7]) + float(row[8]) + float(row[9]),
                    'others': {
                        'Gratificação Natalina': float(row[7]),
                        'Férias (1/3 constitucional)': float(row[8]),
                        'Abono de Permanência': float(row[9]),
                    }
                },

            },
            'discounts':
            {
                'total': abs(float(row[16])),
                'prev_contribution': abs(float(row[13])),
                'ceil_retention': abs(float(row[15])),
                'income_tax': abs(float(row[14]))
            }
        }

        curr_row += 1
        if curr_row >= end_row:
            break
    
    return employees

def parse_colab(file_name):
    rows  = read_data(file_name)
    clean_colab_df(rows)
    rows =  rows.to_numpy()

    begin_string = 'LOTAÇÃO'
    begin_row  =  get_begin_row(rows, begin_string)
    end_row = get_end_row(rows, begin_row)

    typeE = type_employee(file_name)
    activeE = True
    employees  = {}
    curr_row = 0

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue
        
        #O identificador de colaboradores é o nome 
        employees[row[1]] = {
            'name': row[1],
            #Descrição  + Processo  + Competência
            'role': str(row[9]) + ' ' + str(row[8]), 
            'type': typeE,
            'workplace': row[0],
            'active': activeE,
            "income":
            {
                'total': float(row[2]),
            },
            'discounts':
            {
                'total': abs(float(row[4])),
                'income_tax': abs(float(row[3]))
            }
        }
    
        curr_row += 1
        if curr_row >= end_row:
            break
    
    return employees

def update_employee_indemnity(file_name, employees):
    rows  = read_data(file_name)
    print(rows)
    clean_df(rows)

    begin_string = "MATRÍCULA"  # word before starting data
    begin_row = get_begin_row(rows, begin_string)
    end_row = get_end_row(rows, begin_row)
    curr_row = 0

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        emp = employees[row[0]]
        emp['income']['perks'].update({
            #Auxilios saúde e alimentação estão dispostos em 2 colunas diferentes 
            'food': float(row[4]) + float(row[11]),
            'transportation': float(row[17]),
            'health': float(row[6]) + float(row[13]),
        })
        emp['income']['other'].update({
            'total': round (emp['income']['other']['total'] + float(row[5]) + float(row[12]) 
            + float(row[7]) + float(row[8]) + float(row[9]) + float(row[10]) + float(row[14]) + float(row[15]) +
            float(row[18]), 3),
            'Gratification': float(row[16]),
            'others_total': round(emp['income']['other']['others_total'] + float(row[5]) + float(row[12]) 
            + float(row[7]) + float(row[8]) + float(row[9]) + float(row[10]) + float(row[14]) + float(row[15]) +
            float(row[18]), 3),
        })
        emp['income']['other']['others'].update({
            #Auxílio educação está disposto em 2 colunas diferentes 
            'AUXÍLIO-EDUCAÇÃO': float(row[5]) + float(row[12]),
            'CONVERSÃO DE LICENÇA ESPECIAL': float(row[7]),
            'DEVOLUÇÃO IR RRA': float(row[8]),
            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS': float(row[9]),
            'INDENIZAÇÃO POR LICENÇA NÃO GOZADA': float(row[10]),
            'DEVOLUÇÃO FUNDO DE RESERVA': float(row[14]),
            'DIFERENÇAS DE AUXÍLIOS': float(row[15]),
            'PARCELAS PAGAS EM ATRASO': float(row[18])
        })
        employees[row[0]] = emp
        curr_row += 1
        if curr_row >= end_row:
            break
    
    return employees

def parse(file_names):
    employees = {}
    # Colaboradores precisam de um parser distinto
    for fn in file_names:
        if ('Verbas Indenizatórias' not in fn) and ('COLAB' not in fn):
            employees.update(parse_employees(fn))
        elif ('COLAB' in fn):
            employees.update(parse_colab(fn))

    # for fn in file_names:
    #     if 'Verbas Indenizatórias' in fn:
    #         update_employee_indemnity(fn, employees)

    return list(employees.values())