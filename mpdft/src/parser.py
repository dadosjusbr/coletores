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
        nome = row[1].split("/")[0]
        cargo_efetivo = row[1].split("/")[1]
        lotacao = row[2]
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

    begin_string = "Matrícula"  # word before starting data
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
        abono_pecuniario = format_value(row[2])
        creche = format_value(row[3])
        ajuda_de_custo = format_value(row[4])
        natalidade = format_value(row[5])
        alimentacao = format_value(row[6])
        transporte = format_value(row[7])
        ferias_indenizada = format_value(row[8])
        banco_de_horas_indenizado = format_value(row[9])
        moradia = format_value(row[10])
        lp_pecunia = format_value(row[11])
        total_indenizacoes = (
            abono_pecuniario
            + creche
            + ajuda_de_custo
            + natalidade
            + alimentacao
            + transporte
            + ferias_indenizada
            + banco_de_horas_indenizado
            + moradia
            + lp_pecunia
        )

        emp = employees[matricula]
        emp["income"].update(
            {
                "total": round(emp["income"]["total"] + total_indenizacoes, 2),
            }
        )

        emp["income"].update(
            {
                "perks": {
                    "total": round(total_indenizacoes, 2),
                    "food": alimentacao,
                    "pre_school": creche,
                    "transportation": transporte,
                    "housing_aid": moradia,
                    "vacation": ferias_indenizada,
                    "pecuniary": round(abono_pecuniario + banco_de_horas_indenizado, 2),
                    "subsistence": ajuda_de_custo,
                    "birth_aid": natalidade,
                    "premium_license_pecuniary": lp_pecunia,
                }
            }
        )
        employees[matricula] = emp

        curr_row += 1
        if curr_row > end_row:
            break

    return employees


def update_employee_temporary_remuneration(file_name, employees):
    rows = read_data(file_name).to_numpy()

    begin_string = "Matrícula"  # word before starting data
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

        substituicao_membros = format_value(row[2])  # Substituição de Membros
        funcao_substituicao = format_value(row[3])  # Função de Substituição
        grat_encargo_curso = format_value(row[4])  # Gratificação por Encargo de Curso
        insalubridade = format_value(row[5])  # Adicional de Insalubridade
        grat_encargo_concurso = format_value(
            row[6]
        )  # Gratificação por Encargo de Concurso
        periculosidade = format_value(row[7])  # Periculosidade
        exercicio_cumulativo_sem_pass = format_value(
            row[8]
        )  # Gratificação de Exercício Cumulativo com Ofício Sem Psss
        exercicio_cumulativo_com_pass = format_value(
            row[9]
        )  # Gratificação Exercício Cumulativo com Ofício Com Psss
        membros_substituicao = format_value(row[10])  # Membros Substituição
        hora_extra_sem_pass = format_value(row[11])  # Hora Extra Sem Psss
        adic_noturno_sem_pass = format_value(row[12])  # Adicional Noturno Sem Psss
        subs_membros_ms2013 = format_value(row[13])  # Substituição Membros MS2013
        adic_penosidade = format_value(row[14])  # Adicional Penosidade

        total_temporario = (
            substituicao_membros
            + funcao_substituicao
            + grat_encargo_curso
            + insalubridade
            + grat_encargo_concurso
            + periculosidade
            + exercicio_cumulativo_sem_pass
            + exercicio_cumulativo_com_pass
            + membros_substituicao
            + hora_extra_sem_pass
            + adic_noturno_sem_pass
            + subs_membros_ms2013
            + adic_penosidade
        )

        emp = employees[matricula]
        emp["income"].update(
            {
                "total": round(emp["income"]["total"] + total_temporario, 2),
            }
        )

        emp["income"]["other"].update(
            {
                "others_total": round(
                    emp["income"]["other"]["others_total"] + total_temporario, 2
                ),
                "total": round(emp["income"]["other"]["total"] + total_temporario, 2),
            }
        )
        emp["income"]["other"]["others"].update(
            {
                "Substituição de Membros": substituicao_membros,
                "Função de Substituição": funcao_substituicao,
                "Gratificação por Encargo de Curso": grat_encargo_curso,
                "Adicional de Insalubridade": insalubridade,
                "Gratificação por Encargo de Concurso": grat_encargo_concurso,
                "Adicional de Periculosidade": periculosidade,
                "Gratificação de Exercício Cumulativo com Ofício Sem Psss": exercicio_cumulativo_sem_pass,
                "Gratificação Exercício Cumulativo com Ofício Com Psss": exercicio_cumulativo_com_pass,
                "Membros Substituição": membros_substituicao,
                "Hora Extra Sem Psss": hora_extra_sem_pass,
                "Adicional Noturno Sem Psss": adic_noturno_sem_pass,
                "Substituição Membros MS2013": subs_membros_ms2013,
                "Adicional Penosidade": adic_penosidade,
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
        if "Verbas Indenizatorias" not in fn and "Verbas Temporarias" not in fn:
            # Puts all parsed employees in the big map
            employees.update(parse_employees(fn))

    try:
        for fn in file_names:
            if "Verbas Indenizatorias" in fn:
                update_employee_indemnity(fn, employees)
            elif "Verbas Temporarias" in fn:
                update_employee_temporary_remuneration(fn, employees)
    except KeyError as e:
        sys.stderr.write(
            "Registro inválido ao processar verbas indenizatórias: {}".format(e)
        )
        os._exit(1)

    return list(employees.values())
