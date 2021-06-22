import pandas as pd
from datetime import datetime
import math
import pathlib
import sys
import os
import parser_jun_to_aug_2019
import parser_apr_may_2019

# Read data downloaded from the crawler

def read_data(path):
    try:
        data = pd.read_excel(path, engine=None)
        return data
    except Exception as excep:
        sys.stderr.write(
            "'Não foi possível ler o arquivo: "
            + path
            + ". O seguinte erro foi gerado: "
            + excep
        )
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


def get_end_row(rows, begin_row):
    end_row = 0
    for row in rows:
        # First goes to begin_row.
        if end_row < begin_row:
            end_row += 1
            continue
        # Then keep moving until find a blank row.
        if isNaN(row[0]):
            break
        end_row += 1
    end_row -= 1
    return end_row

def format_value(element):
    # A value was found with incorrect formatting. (3,045.99 instead of 3045.99)
    if isNaN(element):
        return 0.0
    if type(element) == str:
        if "." in element and "," in element:
            element = element.replace(".", "").replace(",", ".")
        elif "," in element:
            element = element.replace(",", ".")

    return float(element)

# Used when the employee is not on the indemnity list
def parse_employees(file_name):
    rows = read_data(file_name).to_numpy()
    begin_string = "MATRÍCULA"
    begin_row = get_begin_row(rows, begin_string)
    end_row = get_end_row(rows, begin_row)
    employees = {}
    curr_row = 0
    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = row[0]
        if type(matricula) != str:
            matricula = str(matricula)
        nome = row[1]
        cargo_efetivo = row[3]
        if isNaN(cargo_efetivo):
            cargo_efetivo = "Não informado"
        lotacao = row[5]
        if isNaN(lotacao):
            lotacao = "Não informado"
        remuneracao_cargo_efetivo = format_value(row[6])
        outras_verbas_remuneratorias = format_value(row[7])
        confianca_comissao = format_value(row[8])  # Função de Confiança ou Cargo em Comissão
        grat_natalina = abs(format_value(row[9]))  # Gratificação Natalina
        ferias = format_value(row[10])
        permanencia = format_value(row[11])  # Abono de Permanência
        outras_remuneracoes_temporarias = abs(format_value(row[12]))
        total_indenizacao = format_value(row[13])
        total_bruto = format_value(row[14])
        previdencia = abs(format_value(row[16]))  # Contribuição Previdenciária
        imp_renda = abs(format_value(row[18]))  # Imposto de Renda
        teto_constitucional = abs(format_value(row[20]))  # Retenção por Teto Constitucional
        total_desconto = abs(format_value(row[22]))
        total_gratificacoes = (
            grat_natalina
            + ferias
            + permanencia
            + confianca_comissao
            + outras_remuneracoes_temporarias
        )
        employees[matricula] = {
            "reg": matricula,
            "name": nome,
            "role": cargo_efetivo,
            "type": "membro",
            "workplace": lotacao,
            "active": True,
            "income": {
                "total": round(total_bruto, 2),
                # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                "wage": round(
                    remuneracao_cargo_efetivo + outras_verbas_remuneratorias, 2
                ),
                "perks": {
                    "total": total_indenizacao,
                },
                "other": {  # Gratificações
                    "total": round(total_gratificacoes, 2),
                    "trust_position": confianca_comissao,
                    "others_total": round(grat_natalina + ferias + permanencia, 2),
                    "others": {
                        "Gratificação Natalina": grat_natalina,
                        "Férias (1/3 constitucional)": ferias,
                        "Abono de Permanência": permanencia,
                        "Outras Remunerações Temporárias": outras_remuneracoes_temporarias,
                    },
                },
            },
            "discounts": {  # Discounts Object. Using abs to garantee numbers are positive (spreadsheet have negative discounts).
                "total": round(total_desconto, 2),
                "prev_contribution": previdencia,
                # Retenção por teto constitucional
                "ceil_retention": teto_constitucional,
                "income_tax": imp_renda,
            },
        }

        curr_row += 1
        if curr_row > end_row:
            break

    return employees

def update_employee_indemnity(file_name, employees):
    rows = read_data(file_name).to_numpy()

    begin_string = "MATRÍCULA"  # word before starting data
    begin_row = get_begin_row(rows, begin_string)
    end_row = get_end_row(rows, begin_row)
    curr_row = 0
    # If the spreadsheet does not contain employees

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue
        matricula = row[0]
        if type(matricula) != str:
            matricula = str(matricula)
        if matricula in employees.keys():
            lotacao = row[4]
            alimentacao = format_value(row[5])
            moradia = format_value(row[6])
            ferias_indenizada = format_value(row[7])
            licenca_premio_indenizada = format_value(row[8])
            aposentadoria_incentivada = format_value(row[9])
            verbas_rescisorias = format_value(row[10])
            cumulacao = format_value(row[11])
            complemento = format_value(row[12])
            emp = employees[matricula]

            emp["income"].update(
                {
                    "perks": {
                        "food": alimentacao,
                        "housing_aid": moradia,
                        "vacation": ferias_indenizada,
                    }
                }
            )
            emp['income']['other']['others'].update(
                {
                    "Licença Prêmio Indenizada": licenca_premio_indenizada,
                    "Programa de Aposentadoria Incentivada": aposentadoria_incentivada,
                    "Verbas Rescisórias": verbas_rescisorias,
                    "Cumulação": cumulacao,
                    "Complemento por Entrância": complemento
                }
            )

            employees[matricula] = emp

            curr_row += 1
            if curr_row > end_row:
                break

    return employees

def parse(file_names, year, month):
    employees = {}
    esp_months = ['6', '7', '8']    # June, July, August
    esp_months2 = ['4', '5']    # April and May
    if year == '2019' and month in esp_months2:
        for fn in file_names:
            if "Verbas Indenizatorias" not in fn:
                # Puts all parsed employees in the big map
                employees.update(parser_apr_may_2019.parse_employees(fn))
        try:
            for fn in file_names:
                if "Verbas Indenizatorias" in fn:
                    parser_apr_may_2019.update_employee_indemnity(fn, employees)
        except KeyError as e:
            sys.stderr.write(
                "Registro inválido ao processar verbas indenizatórias: {}".format(e)
            )
            os._exit(1)

    elif year == '2019' and month in esp_months:
        for fn in file_names:
            if "Verbas Indenizatorias" not in fn:
                # Puts all parsed employees in the big map
                employees.update(parse_employees(fn))
        try:
            for fn in file_names:
                if "Verbas Indenizatorias" in fn:
                    parser_jun_to_aug_2019.update_employee_indemnity(fn, employees)
        except KeyError as e:
            sys.stderr.write(
                "Registro inválido ao processar verbas indenizatórias: {}".format(e)
            )
            os._exit(1)

    else:     
        for fn in file_names:
            if "Verbas Indenizatorias" not in fn:
                # Puts all parsed employees in the big map
                employees.update(parse_employees(fn))   
        try:
            for fn in file_names:
                if "Verbas Indenizatorias" in fn:
                    update_employee_indemnity(fn, employees)
        except KeyError as e:
            sys.stderr.write(
                "Registro inválido ao processar verbas indenizatórias: {}".format(e)
            )
            os._exit(1)

    return list(employees.values())
