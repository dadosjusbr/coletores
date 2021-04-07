import pandas as pd
import pyexcel_ods
from datetime import datetime
import math
import numpy
import utils
import pathlib
import sys
import os

def read_data(path):
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
 
    employees = {}
    curr_row = 0
    for row in emps_clean:
        matricula = str(row[0])
        nome = str(row[1])
        cargo = str(row[2])
        workplace = str(row[3])
        remuneracao = row[4]+row[5]   # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
        total_indenizacao = row[11]
        cargo_confianca = row[6]
        grat_natalina = row[7]
        ferias = row[8]
        abono_permanencia = row[9]
        total_temporario = cargo_confianca + grat_natalina + ferias + abono_permanencia
        previdencia = abs(row[13])
        teto_constitucional = abs(row[15])
        imposto_de_renda = abs(row[14])
        total_descontos = previdencia + teto_constitucional + imposto_de_renda
        total_bruto = total_indenizacao + total_temporario + remuneracao
        employees[row[0]] = {
            'reg': matricula,
            'name': nome,
            'role': cargo,
            'type': "membro",
            'workplace': workplace,
            'active': True,
            "income":
            {
                #Soma de todos os recebidos do funcionário
                'total': round(total_bruto, 2),
                'wage': round(remuneracao, 2),
                'perks': {
                    'total': total_indenizacao,
                },
                'other':
                {  # Gratificações e remuneraçoes temporárias
                    'total': round(total_temporario, 2),
                    'trust_position': cargo_confianca,
                    'others_total': round(grat_natalina + ferias + abono_permanencia, 2),
                    'others': {
                        'Gratificação Natalina': grat_natalina,
                        'Férias (1/3 constitucional)': ferias,
                        'Abono de Permanência': abono_permanencia,
                    }
                },
            },
            'discounts':
            {  # Discounts Object. Using abs to garantee numbers are positivo (spreadsheet have negative discounts).
                'total':round(total_descontos, 2),
                'prev_contribution': previdencia ,
                'ceil_retention': teto_constitucional,
                'income_tax': imposto_de_renda ,
            }
        }
    return employees

def update_employee_indemnity(file_name, employees):
    rows = read_data(file_name).to_numpy()
    emp_idemnity = utils.treat_rows(rows)
    for row in emp_idemnity:
        exists_employee = employees.get(row[0])
        if exists_employee:
            ferias = row[4]
            alimentacao = row[5]
            creche = row[6]
            transporte = row[7]
            transporte_mobiliario = row[8]
            natalidade = row[9]
            ajuda_custo = row[10]
            moradia = row[11]
            pecunia = row[12]
            lp_pecunia = row[13]

            pericia_projeto =  row[15]
            grat_exercicio_cumulativo = row[16]
            encargo_de_curso_concurso = row[17]
            grat_local_de_trabalho = row[18]
            hora_extra = row[20]
            adic_noturno = row[22]
            adic_atividade_penosa = row[23]
            adic_insalubridade = row[24]
            outras_verbas_remuneratorias = row[25]
            outras_verbas_retroativas = row[26]
            total_temporario = pericia_projeto + grat_exercicio_cumulativo + encargo_de_curso_concurso + grat_local_de_trabalho + hora_extra + adic_noturno + adic_atividade_penosa + adic_insalubridade + outras_verbas_remuneratorias + outras_verbas_retroativas
           
            emp = employees[row[0]]
            emp['income'].update({
                'total': round(emp['income']['total'] + total_temporario,2)
            })
            emp['income']['perks'].update({
                'total': round(sum(row[4:14]),2),
                'vacation': ferias,
                'food': alimentacao,
                'pre_school': creche,
                'transportation': transporte,
                'furniture_transport': transporte_mobiliario,
                'birth_aid': natalidade,
                'subsistence': ajuda_custo ,
                'housing_aid': moradia ,
                'pecuniary': pecunia,
                'premium_license_pecuniary': lp_pecunia,
            })
            emp['income']['other'].update({
                'total': round(emp['income']['other']['total'] + total_temporario, 2),
                'others_total': round(emp['income']['other']['others_total'] + total_temporario, 2),
            })
            emp['income']['other']['others'].update({
                'Gratificação de Perícia e Projeto':pericia_projeto,
                'Gratificação Exercício Cumulativo de Ofício': grat_exercicio_cumulativo,
                'Gratificação Encargo de Curso e Concurso': encargo_de_curso_concurso,
                'Gratificação Local de Trabalho': grat_local_de_trabalho,
                'Hora Extra': hora_extra,
                'Adicional Noturno': adic_noturno,
                'Adicional Atividade Penosa': adic_atividade_penosa,
                'Adicional Insalubridade': adic_insalubridade,
                'Outras Verbas Remuneratórias': outras_verbas_remuneratorias,
                'Outras Verbas Remuneratórias Retroativas/Temporárias': outras_verbas_retroativas,

            })
            employees[row[0]] = emp
        else:
            continue
        

    return employees

def parse(file_names):
    employees = {}
    for fn in file_names:
        if 'Verbas Indenizatorias' not in fn:
            # Puts all parsed employees in the big map
            employees.update(parse_employees(fn))
    for fn in file_names:
        if 'Verbas Indenizatorias' in fn:
            update_employee_indemnity(fn, employees)
    return list(employees.values())