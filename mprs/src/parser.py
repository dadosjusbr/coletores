import pandas as pd
import pathlib
import sys
import os
import json

# Lê os dados baixados pelo crawler
def read_data(path):
    try:
        with open((pathlib.Path(path)), 'r') as arq:
            data = json.load(arq)
            return data
    except Exception as excep:
        sys.stderr.write("'Não foi possível ler o arquivo: " +
                         path + '. O seguinte erro foi gerado: ' + excep)
        os._exit(1)

# Verifica se a chave existe no dicionário
def validates(row, column):
    try:
        test = row[column]
    except Exception:
        return ""
    return test

# Define o tipo do empregado, a partir do nome do arquivo
def type_employee(fn):
    if 'M-' in fn or 'MI-' in fn:
        return 'membro'
    if 'S-' in fn or 'SI-' in fn:
        return 'servidor'
    if 'P-' in fn:
        return 'pensionista'
    if 'estagiarios-' in fn:
        return 'colaborador'
    raise ValueError('Tipo inválido de funcionário público: ' + fn)

def parse_employees(file_name):
    rows = read_data(file_name)
    employees = {}
    
    for row in rows["response"]["docs"]:
        insert_employee(row, employees, file_name)

    return employees

def insert_employee(row, employees, file_name):
    type_e = type_employee(file_name)
    active_e = 'I-' not in file_name and "P-" not in file_name

    reg = row["numfunc_s"]
    name = row["nome_s"] 
    role = validates(row, "cargo_s")
    workplace = validates(row, "lotacao_s")
    income_total = float(row["total_creditos_tf"])
    wage = float(row["outras_verbas_tf"]) + float(row["vencimentos_tf"])
    # Indemnities
    perks_total = float(row["indenizacoes_tf"])
    # Gratifications 
    gratifications_total = float(row["fg_cc_tf"]) + float(row["gratificacao_natalina_tf"]) + float(row["ferias_tf"]) + float(row["abono_permanencia_tf"])
    trust_position = float(row["fg_cc_tf"])
    others_total = float(row["gratificacao_natalina_tf"]) + float(row["ferias_tf"]) + float(row["abono_permanencia_tf"])
    others_christmas_bonus = float(row["gratificacao_natalina_tf"])
    others_vacation = float(row["ferias_tf"])
    other_allowance_of_permanence = float(row["abono_permanencia_tf"])
    # Discounts
    discounts_total = abs(float(row["total_descontos_tf"]))
    discounts_prev_contribution = abs(float(row["previdencia_tf"]))
    discounts_ceil_retention = abs(float(row["estorno_de_teto_tf"]))
    discounts_income_tax = abs(float(row["ir_tf"]))
    
    employees[reg] = {
        'reg': reg,
        'name': name,
        'role': role,
        'type': type_e,
        'workplace': workplace,
        'active': active_e,
        "income": {
            'total': income_total,
            'wage': wage,
            'perks': {
                'total': perks_total,
            },
            'other': { 
                #Gratificações
                'total': gratifications_total,
                'trust_position': trust_position,
                'others_total': others_total,
                'others': {
                    'Gratificação Natalina': others_christmas_bonus,
                    'Férias (1/3 constitucional)': others_vacation,
                    'Abono de Permanência': other_allowance_of_permanence,
                }
            },
        },
        'discounts': {
            'total': discounts_total,
            'prev_contribution': discounts_prev_contribution,
            'ceil_retention': discounts_ceil_retention,
            'income_tax': discounts_income_tax
        }
    }

    return employees

def update_employees(file_name, employees):
    rows = read_data(file_name)

    for row in rows["response"]["docs"]:
        reg = row["numfunc_s"]
        income_total = float(row["total_creditos_tf"])
        wage = float(row["outras_verbas_tf"]) + float(row["vencimentos_tf"])
        # Indemnities
        perks_total = float(row["indenizacoes_tf"])
        # Gratifications 
        gratifications_total = float(row["fg_cc_tf"]) + float(row["gratificacao_natalina_tf"]) + float(row["ferias_tf"]) + float(row["abono_permanencia_tf"])
        trust_position = float(row["fg_cc_tf"])
        others_total = float(row["gratificacao_natalina_tf"]) + float(row["ferias_tf"]) + float(row["abono_permanencia_tf"])
        others_christmas_bonus = float(row["gratificacao_natalina_tf"])
        others_vacation = float(row["ferias_tf"])
        other_allowance_of_permanence = float(row["abono_permanencia_tf"])
        # Discounts
        discounts_total = abs(float(row["total_descontos_tf"]))
        discounts_prev_contribution = abs(float(row["previdencia_tf"]))
        discounts_ceil_retention = abs(float(row["estorno_de_teto_tf"]))
        discounts_income_tax = abs(float(row["ir_tf"]))
        
        try:
            emp = employees[reg]
        except Exception:
            insert_employee(row, employees, file_name)
            continue

        emp['income'].update({
            'total': emp['income']['total'] + income_total,
            'wage': emp['income']['wage'] + wage
        })
        emp['income']['perks'].update({
            'total': emp['income']['perks']['total'] + perks_total
        })
        emp['income']['other'].update({
            'total': emp['income']['other']['total'] + gratifications_total,
            'trust_position': emp['income']['other']['trust_position'] + trust_position,
            'others_total': emp['income']['other']['others_total'] + others_total
        })
        emp['income']['other']['others'].update({
            'Gratificação Natalina': emp['income']['other']['others']['Gratificação Natalina'] + others_christmas_bonus,
            'Férias (1/3 constitucional)': emp['income']['other']['others']['Férias (1/3 constitucional)'] + others_vacation,
            'Abono de Permanência': emp['income']['other']['others']['Abono de Permanência'] + other_allowance_of_permanence
        })
        emp['discounts'].update({
            'total': emp['discounts']['total'] + discounts_total,
            'prev_contribution': emp['discounts']['prev_contribution'] + discounts_prev_contribution,
            'ceil_retention': emp['discounts']['ceil_retention'] + discounts_ceil_retention,
            'income_tax': emp['discounts']['income_tax'] + discounts_income_tax
        })
        employees[reg] = emp

    return employees

def parse(file_names):
    employees = {}
    # As tabelas de "Colaboradores" e de "Verbas Indenizatórias e Outras 
    # Remunerações Temporárias" precisam de um parser distinto
    for fn in file_names:
        if ('NORMAL' in fn):
            employees.update(parse_employees(fn))
    # Atualização dos employees com a folha complementar e a de 13º salário
    for fn in file_names:
        if ('COMPLEMENTAR' in fn) | ('13' in fn):
            update_employees(fn, employees)
    return list(employees.values())