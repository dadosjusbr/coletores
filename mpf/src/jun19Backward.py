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
    if year == "2019" and month == "6":
        eng = 'odf'
    else:
        eng = 'xlrd'
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
    employees = {}
    curr_row = 0
    for row in emps_clean:
        name = str(row[0])
        cargo = str(row[1])
        workplace = str(row[3])
        remuneracao = row[4]+row[5]   # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
        total_indenizacao = row[16]
        cargo_confianca = row[6]
        grat_natalina = row[7]
        ferias = row[8]
        abono_permanencia = row[9]
        total_temporario = cargo_confianca + grat_natalina + ferias + abono_permanencia
        previdencia = abs(row[11])
        teto_constitucional = abs(row[13])
        imposto_de_renda = abs(row[12])
        total_descontos = previdencia + teto_constitucional + imposto_de_renda
        total_bruto = total_indenizacao + total_temporario + remuneracao
        if name not in employees.keys():
            employees[row[0]] = {
                'name': name,
                'role': cargo,
                'type': "membro",
                'workplace': workplace,
                'active': True,
                "income":
                {
                    #Soma de todos os recebidos do funcionário
                    'total': round(total_bruto, 2),
                    # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                    'wage': remuneracao,
                    'perks': {
                        'total': total_indenizacao,
                    },
                    'other':
                    {  # Gratificações e remuneraçoes temporárias
                        'total': round(total_temporario, 2),
                        'trust_position': cargo_confianca,
                        'others_total': round(grat_natalina + ferias + abono_permanencia,2),
                        'others': {
                            'Gratificação Natalina': grat_natalina,
                            'Férias (1/3 constitucional)': ferias,
                            'Abono de Permanência': abono_permanencia,
                        }
                    },
                },
                'discounts':
                {  # Discounts Object. Using abs to garantee numbers are positivo (spreadsheet have negative discounts).
                    'total': round(total_descontos, 2),
                    'prev_contribution': previdencia,
                    # Retenção por teto constitucional
                    'ceil_retention': teto_constitucional,
                    'income_tax': imposto_de_renda,
                }
            }
        else:
            emp = employees[name]
            emp['income'].update({
                'total': round(emp['income']['total'] + remuneracao + total_indenizacao + total_temporario ,2)
            })
            emp['income'].update({
                'wage': round(emp['income']['wage'] + remuneracao ,2)
            })
            emp['income']['perks'].update({
                'total': round(emp['income']['perks']['total'] + total_indenizacao,2)
            })
            emp['income']['other'].update({
                'total': round(emp['income']['other']['total'] + total_temporario,2),
                'trust_position': round(emp['income']['other']['trust_position'] + cargo_confianca,2),
                'others_total': round(emp['income']['other']['others_total'] + grat_natalina + ferias + abono_permanencia, 2)
            })
            emp['income']['other']['others'].update({
               'Gratificação Natalina': round(emp['income']['other']['others']['Gratificação Natalina'] + grat_natalina, 2),
               'Férias (1/3 constitucional)': round(emp['income']['other']['others']['Férias (1/3 constitucional)'] + ferias, 2),
               'Abono de Permanência': round(emp['income']['other']['others']['Abono de Permanência'] + abono_permanencia, 2)
            })

            emp['discounts'].update({
               'total': round(emp['discounts']['total'] + total_descontos, 2),
               'prev_contribution': round(emp['discounts']['prev_contribution'] + previdencia, 2),
               'ceil_retention': round(emp['discounts']['ceil_retention'] + teto_constitucional, 2),
               'income_tax': round(emp['discounts']['income_tax'] + imposto_de_renda, 2)
            })

    return employees

def parse(file_names, year, month):
    employees = {}
    for fn in file_names:
            # Puts all parsed employees in the big map
            employees.update(parse_employees(fn, year, month))
    return list(employees.values())