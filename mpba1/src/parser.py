import pandas as pd
from datetime import datetime
import math
import pathlib
import sys
import os

# Read data downloaded from the crawler


def read_data(path):
    try:
        data = pd.read_excel(path, engine="odf")
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
    end_string = "TOTAL"
    end_row = 0
    for row in rows:
        # First goes to begin_row.
        if end_row < begin_row:
            end_row += 1
            continue
        # Then keep moving until find a blank row.
        if end_string in str(row[0]):
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
    begin_string = "Matrícula"
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
        cargo_efetivo = row[2]
        lotacao = row[3]
        if isNaN(lotacao):
            lotacao = "Não informado"
        remuneracao_cargo_efetivo = format_value(row[4])
        outras_verbas_remuneratorias = format_value(row[5])
        confianca_comissao = format_value(
            row[6]
        )  # Função de Confiança ou Cargo em Comissão
        grat_natalina = format_value(row[7])  # Gratificação Natalina
        ferias = format_value(row[8])
        permanencia = format_value(row[9])  # Abono de Permanência
        previdencia = format_value(row[13])  # Contribuição Previdenciária
        imp_renda = format_value(row[14])  # Imposto de Renda
        teto_constitucional = format_value(row[15])  # Retenção por Teto Constitucional
        total_desconto = previdencia + imp_renda + teto_constitucional
        total_gratificacoes = grat_natalina + ferias + permanencia + confianca_comissao
        total_bruto = (
            remuneracao_cargo_efetivo
            + outras_verbas_remuneratorias
            + total_gratificacoes
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
                "other": {  # Gratificações
                    "total": round(total_gratificacoes, 2),
                    "trust_position": confianca_comissao,
                    "others_total": round(grat_natalina + ferias + permanencia, 2),
                    "others": {
                        "Gratificação Natalina": grat_natalina,
                        "Férias (1/3 constitucional)": ferias,
                        "Abono de Permanência": permanencia,
                    },
                },
            },
            "discounts": {  # Discounts Object. Using abs to garantee numbers are positivo (spreadsheet have negative discounts).
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

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = row[0]
        if type(matricula) != str:
            matricula = str(matricula)
   
        alimentacao = format_value(row[4])
        transporte = format_value(row[5])
        moradia = format_value(row[6])
        natalidade = format_value(row[7])
        subst_membros = format_value(row[8])
        ajuda_de_custo = format_value(row[9])
        servico_extraordinario = format_value(row[10])
        subst_funcao = format_value(row[11])
        grat_servicos_especiais = format_value(row[12])
        diferenca_de_entrancia = format_value(row[13])

        total_indenizacoes = (
            alimentacao + transporte + moradia + natalidade + ajuda_de_custo
        )
        total_remuneracao_temporaria = (
            servico_extraordinario
            + subst_funcao
            + grat_servicos_especiais
            + diferenca_de_entrancia
            + subst_membros
        )
        if (
            matricula in employees.keys()
        ):  # Realiza o update apenas para os servidores que estão na planilha de remuneração mensal

            emp = employees[matricula]

            emp["income"].update(
                {
                    "total": round(
                        emp["income"]["total"]
                        + total_indenizacoes
                        + total_remuneracao_temporaria,
                        2,
                    ),
                }
            )

            emp["income"].update(
                {
                    "perks": {
                        "total": round(total_indenizacoes, 2),
                        "food": alimentacao,
                        "transportation": transporte,
                        "housing_aid": moradia,
                        "birth_aid": natalidade,
                        "subsistence": ajuda_de_custo,
                    }
                }
            )

            emp["income"]["other"].update(
                {
                    "others_total": round(
                        emp["income"]["other"]["others_total"]
                        + total_remuneracao_temporaria,
                        2,
                    ),
                    "total": round(
                        emp["income"]["other"]["total"] + total_remuneracao_temporaria, 2
                    ),
                }
            )
            emp["income"]["other"]["others"].update(
                {
                    "Substituição de Membros": subst_membros,
                    "Serviço Extraordinário": servico_extraordinario,
                    "Substituição de Função": subst_funcao,
                    "Gratificação de Serviços Especiais": grat_servicos_especiais,
                    "Diferença de Entrância": diferenca_de_entrancia,
                }
            )

            employees[matricula] = emp

        curr_row += 1
        if curr_row > end_row:
            break
    return employees


def parse(file_names):
    employees = {}
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
