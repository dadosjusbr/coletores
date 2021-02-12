import pandas as pd
import pathlib
import sys
import os
import json

# Lê os dados baixados pelo crawler
def read_data(path):
    if 'verbas' not in path and 'estagiarios' not in path:
        try:
            with open((pathlib.Path(path)), 'r') as arq:
                data = json.load(arq)
                return data
        except Exception as excep:
            sys.stderr.write("'Não foi possível ler o arquivo: " +
                            path + '. O seguinte erro foi gerado: ' + excep)
            os._exit(1)
    elif 'verbas' in path:
        try:
            with open((pathlib.Path(path)), 'r') as arq:
                data = pd.read_html(arq, decimal=',', thousands='.')
                df = data[0]
                df.columns = ['Matrícula', 'Nome', 'Cargo', 'Lotação', 'Abono Família', 'Vale Alimentação', 'Auxílio Transporte', 'Auxílio Creche', 'Conversões em Pecúnia', 'Comissão Especial', 'Gratificação Setor', 'Adicional Insal / Periculosidae', 'Difícil Provimento', 'Honorário Concurso', 'Substituição', 'Diretor Promotoria', 'Hora Extra', 'Acúmulo funções']
                return df
        except Exception as excep:
            sys.stderr.write("'Não foi possível ler o arquivo: " +
                            path + '. O seguinte erro foi gerado: ' + excep)
            os._exit(1)

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
        reg = row["numfunc_s"]
        employee = generates_employee(row, file_name)
        employees[reg] = employee

    return employees

def generates_employee(row, file_name):
    type_e = type_employee(file_name)
    active_e = 'I-' not in file_name and "P-" not in file_name

    reg = row["numfunc_s"]
    name = row["nome_s"] 
    if "cargo_s" in row:
        role = row["cargo_s"]
    else:
        role = ""
    if "lotacao_s" in row:
        workplace = row["lotacao_s"]
    else:
        workplace = ""
    wage = round(float(row["outras_verbas_tf"]) + float(row["vencimentos_tf"]), 2)
    # Indemnities
    perks_total = round(float(row["indenizacoes_tf"]), 2)
    # Gratifications 
    trust_position = round(float(row["fg_cc_tf"]), 2)
    others_christmas_bonus = round(float(row["gratificacao_natalina_tf"]), 2)
    others_vacation = round(float(row["ferias_tf"]), 2)
    others_allowance_of_permanence = round(float(row["abono_permanencia_tf"]), 2)
    others_total = others_christmas_bonus + others_vacation + others_allowance_of_permanence
    gratifications_total = round(trust_position + others_christmas_bonus + others_vacation + others_allowance_of_permanence, 2)
    # Discounts
    discounts_prev_contribution = round(abs(float(row["previdencia_tf"])), 2)
    discounts_ceil_retention = round(abs(float(row["estorno_de_teto_tf"])), 2)
    discounts_income_tax = round(abs(float(row["ir_tf"])), 2)
    discounts_total = round(discounts_prev_contribution + discounts_ceil_retention + discounts_income_tax, 2)
    # Total
    income_total = round(wage + perks_total + gratifications_total, 2)
    
    employee = {
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
                    'Abono de Permanência': others_allowance_of_permanence,
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

    return employee

def update_employees(file_name, employees):
    rows = read_data(file_name)

    for row in rows["response"]["docs"]:
        reg = row["numfunc_s"]
        wage = round(float(row["outras_verbas_tf"]) + float(row["vencimentos_tf"]), 2)
        # Indemnities
        perks_total = round(float(row["indenizacoes_tf"]), 2)
        # Gratifications 
        trust_position = round(float(row["fg_cc_tf"]), 2)
        others_christmas_bonus = round(float(row["gratificacao_natalina_tf"]), 2)
        others_vacation = round(float(row["ferias_tf"]), 2)
        others_allowance_of_permanence = round(float(row["abono_permanencia_tf"]), 2)
        others_total = others_christmas_bonus + others_vacation + others_allowance_of_permanence
        gratifications_total = round(trust_position + others_christmas_bonus + others_vacation + others_allowance_of_permanence, 2)
        # Discounts
        discounts_prev_contribution = round(abs(float(row["previdencia_tf"])), 2)
        discounts_ceil_retention = round(abs(float(row["estorno_de_teto_tf"])), 2)
        discounts_income_tax = round(abs(float(row["ir_tf"])), 2)
        discounts_total = round(discounts_prev_contribution + discounts_ceil_retention + discounts_income_tax, 2)
        # Total
        income_total = round(wage + perks_total + gratifications_total, 2)

        try:
            emp = employees[reg]
        except Exception:
            employee = generates_employee(row, file_name)
            employees[reg] = employee
            continue
        
        # Faz-se necessário somar novos valores aos valores atuais dos campos, dada a disposição
        # dos valores remuneratórios ao longo de três folhas de pagamento (normal, complementar
        # e 13º salário).
        emp['income'].update({
            'total': emp['income']['total'] + income_total,
            'wage': round(emp['income']['wage'] + wage, 2)
        })
        emp['income']['perks'].update({
            'total': round(emp['income']['perks']['total'] + perks_total, 2)
        })
        emp['income']['other'].update({
            'total': round(emp['income']['other']['total'] + gratifications_total, 2),
            'trust_position': round(emp['income']['other']['trust_position'] + trust_position, 2),
            'others_total': round(emp['income']['other']['others_total'] + others_total, 2)
        })
        emp['income']['other']['others'].update({
            'Gratificação Natalina': round(emp['income']['other']['others']['Gratificação Natalina'] + others_christmas_bonus, 2),
            'Férias (1/3 constitucional)': round(emp['income']['other']['others']['Férias (1/3 constitucional)'] + others_vacation, 2),
            'Abono de Permanência': round(emp['income']['other']['others']['Abono de Permanência'] + others_allowance_of_permanence, 2)
        })
        emp['discounts'].update({
            'total': round(emp['discounts']['total'] + discounts_total, 2),
            'prev_contribution': round(emp['discounts']['prev_contribution'] + discounts_prev_contribution, 2),
            'ceil_retention': round(emp['discounts']['ceil_retention'] + discounts_ceil_retention, 2),
            'income_tax': round(emp['discounts']['income_tax'] + discounts_income_tax, 2)
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