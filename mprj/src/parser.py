import pandas as pd
from datetime import datetime
import math
import pathlib
import sys
import os

#Lê os dados baixados pelo crawler
def read_data(path):
    try:
        data = pd.read_excel(pathlib.Path(path), engine= 'odf')
        return data
    except Exception as excep:
        sys.stderr.write("'Não foi possível ler o arquivo: " +
                         path + '. O seguinte erro foi gerado: ' + excep)
        os._exit(1)

# Strange way to check nan. Only I managed to make work
# Source: https://stackoverflow.com/a/944712/5822594
def is_nan(string):
    return string != string

def get_begin_row(rows, begin_string):
    begin_row  = 0
    for row in rows:
        begin_row += 1
        if row[0] == begin_string:
            break
    #Continua interando até encontrarmos um valor que não seja string em
    #branco. Isto ocorre pelo formato da planilha
    while is_nan(rows[begin_row][0]):
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
        if is_nan(row[0]):
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

        remuneration = float(row[4]) #Remuneração do cargo efetivo
        other_verbs = float(row[5]) #Outras verbas remuneratórias, legais ou judiciais
        trust_pos = float(row[6]) #Posição de Confiança
        christmas_bonus = float(row[7]) #Gratificação natalina
        abono_permanencia = float(row[9]) #Abono Permanência
        terco_ferias = float(row[8]) # Férias (1/3 constitucional)
        idemnity = float(row[10]) #Indenizações
        temp_remu = float(row[11]) # Outras remunerações retroativas/temporárias

        prev_contrib = float(row[13]) #Contribuição previdenciária
        ceil_ret = float(row[15]) #Retenção por teto constitucional
        income_tax = float(row[14]) #Imposto de renda

        employees[row[0]] = {
            'reg': row[0],
            'name': row[1],
            'role': row[2],
            'type': typeE,
            'workplace': row[3],
            'active': activeE,
            "income":
            {
                'total': remuneration + other_verbs + trust_pos + christmas_bonus + abono_permanencia + terco_ferias
                + idemnity + temp_remu,
                'wage': remuneration + other_verbs,
                'perks':{

                    'total': temp_remu,
                },
                'other':
                { #Gratificações
                        #Posição de confiança + Gratificação natalina + Férias (1/3 constitucional) + Abono de permanência
                    'total': trust_pos + christmas_bonus + terco_ferias + abono_permanencia,
                    'trust_position': trust_pos,
                        # Gratificação natalina + Férias (1/3 constitucional) + Abono Permanencia
                    'others_total': christmas_bonus + terco_ferias + abono_permanencia,
                    'others': {
                        'gratificação natalina': christmas_bonus,
                        'ferias (1/3 constitucional)': terco_ferias,
                        'abono de permanência': abono_permanencia,
                    }
                },

            },
            'discounts':
            {
                'total': prev_contrib + ceil_ret + income_tax ,
                'prev_contribution': prev_contrib,
                'ceil_retention': ceil_ret,
                'income_tax': income_tax
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
            #Descrição do serviço prestado e número do processo de pagamento ao servidor
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
                'total': float(row[4]),
                'income_tax': float(row[3])
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

        #Variáveis
        aux_ali =  float(row[4]) # AUXÍLIO-ALIMENTAÇÃO/VERBAS INDENIZATÓRIAS
        aux_ali_remu = float(row[11])  #AUXÍLIO-ALIMENTAÇÃO/OUTRAS REMUNERAÇÕES RETROATIVAS/TEMPORÁRIAS
        aux_saude = float(row[6]) #AUXÍLIO-SAÚDE/VERBAS INDENIZATÓRIAS
        aux_saude_remu = float(row[13]) #AUXÍLIO-SAÚDE/OUTRAS REMUNERAÇÕES RETROATIVAS/TEMPORÁRIAS
        aux_edu = float(row[5]) #AUXÍLIO-EDUCAÇÃO/VERBAS INDENIZATÓRIAS
        aux_edu_remu = float(row[12]) #AUXÍLIO-EDUCAÇÃO/OUTRAS REMUNERAÇÕES RETROATIVAS/TEMPORÁRIAS
        conversao_licenca = float(row[7]) #CONVERSÃO DE LICENÇA ESPECIAL
        devolucao_rra = float(row[8]) #DEVOLUÇÃO IR RRA
        indemnity_vacation = float(row[9]) #INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS
        indemnity_licence = float(row[10]) #INDENIZAÇÃO POR LICENÇA NÃO GOZADA
        devolucao_fundo = float(row[14]) #DEVOLUÇÃO FUNDO DE RESERVA
        diff_aux = float(row[15]) #DIFERENÇAS DE AUXÍLIOS
        gratification = float(row[16])
        parcelas_atraso = float(row[18]) #PARCELAS PAGAS EM ATRASO

        emp = employees[row[0]]
        emp['income']['perks'].update({
            #Auxilios saúde e alimentação estão dispostos em 2 colunas diferentes
            'food':  aux_ali + aux_ali_remu ,
            'transportation': float(row[17]),
            'health': aux_saude + aux_saude_remu,
        })
        emp['income']['other'].update({
            'total': round (emp['income']['other']['total'] + aux_edu + aux_edu_remu +
            conversao_licenca + devolucao_rra + indemnity_vacation + indemnity_licence +
            devolucao_fundo + diff_aux + parcelas_atraso + gratification, 3),
            'gratification': gratification,
            'others_total': round(emp['income']['other']['others_total'] +
            aux_edu + aux_edu_remu + conversao_licenca + devolucao_rra +
            indemnity_vacation + indemnity_licence + devolucao_fundo +
            diff_aux + parcelas_atraso, 3),
        })
        emp['income']['other']['others'].update({
            #Auxílio educação está disposto em 2 colunas diferentes
            'auxilio_educacao': aux_edu + aux_edu_remu,
            'conversao_licenca': conversao_licenca,
            'devolucao_rra': devolucao_rra,
            'indenizacao_ferias': indemnity_vacation,
            'indenizacao_licenca': indemnity_licence,
            'devolucao_fundo': devolucao_fundo,
            'diferencas_aux': diff_aux,
            'parcelas_atraso': parcelas_atraso
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
