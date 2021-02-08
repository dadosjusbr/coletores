import pandas as pd
import math
import parser

# Due to the different format of the spreadsheets, a specific parser is required for a few months
# This class contains the parsers for inactive servants:
# parse_jan_to_april_19: January to April 2019
# parse_may_19: May 2019
# parse_june_19: June 2019

# It also contains the parser for worksheet of indemnification funds and temporary remuneration from August to November 2020

# Adjust existing spreadsheet variations
def format_value(element):
    if element == None:
        return 0.0
    elif type(element) == str and "-" in element:
        return 0.0
    elif element == "#N/DISP":
        return 0.0
    return element


def parse_jan_to_april_19(file_name):
    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)

    typeE = parser.type_employee(file_name)
    activeE = "inativos" not in file_name
    employees = {}
    curr_row = 0
    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = str(int(row[0]))  # convert to string by removing the '.0'
        name = row[1].strip()  # removes blank spaces present in some cells
        role = row[2]  # cargo
        workplace = row[3]  # Lotação
        total_bruto = format_value(row[7])  # Total de Rendimentos Brutos
        sal_base = format_value(row[4])  # Salário Base
        outras_remuneracoes = format_value(
            row[5]
        )  # Outras Verbas Remuneratórias, Legais ou Judiciais
        grat_natal = format_value(row[6])  # Gratificação Natalina (13º  sal.)
        total_descontos = format_value(row[10])
        contribuicao_previdenciaria = format_value(row[8])
        imposto_renda = format_value(row[9])

        employees[matricula] = {
            "reg": matricula,
            "name": name,
            "role": role,
            "type": typeE,
            "workplace": workplace,
            "active": activeE,
            "income": {
                "total": total_bruto,
                "wage": sal_base + outras_remuneracoes,
                "other": {  # Gratificações
                    "total": grat_natal,
                    "others_total": grat_natal,
                    "others": {
                        "Gratificação Natalina": grat_natal,
                    },
                },
            },
            "discounts": {  # Discounts Object. Using abs to garantee numbers are positivo (spreadsheet have negative discounts).
                "total": abs(total_descontos),
                "prev_contribution": abs(contribuicao_previdenciaria),
                "income_tax": abs(imposto_renda),
            },
        }

        curr_row += 1
        if curr_row >= end_row:
            break
    return employees


# May 2019
def parse_may_19(file_name):
    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)

    typeE = parser.type_employee(file_name)
    activeE = "inativos" not in file_name
    employees = {}
    curr_row = 0
    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = str(int(row[0]))  # convert to string by removing the '.0'
        name = row[1].strip()  # removes blank spaces present in some cells
        role = row[2]  # cargo
        workplace = row[3].strip()  # Lotação
        sal_base = format_value(row[4])  # Salário Base
        outras_remuneracoes = format_value(
            row[5]
        )  # Outras Verbas Remuneratórias, Legais ou Judiciais
        comissao = format_value(row[6])  # Função de Confiança ou Cargo em Comissão
        grat_natal = format_value(row[7])  # Gratificação Natalina (13º  sal.)
        permanencia = format_value(row[8])  # Abono de Permanência
        contribuicao_previdenciaria = format_value(row[10])
        imposto_renda = format_value(row[11])
        total_descontos = format_value(row[12])
        alimentacao = format_value(row[14])  # Auxilio alimentação
        transporte = format_value(row[15])  # Auxilio transporte
        ferias_pc = format_value(row[16])  # Férias em pecunia
        remuneracoes_temporarias = format_value(
            row[17]
        )  # Outras Remunerações Temporárias
        total_indenizacoes = alimentacao + ferias_pc + transporte
        total_gratificacoes = (
            grat_natal + comissao + permanencia + remuneracoes_temporarias
        )
        total_bruto = (
            total_gratificacoes + total_indenizacoes + sal_base + outras_remuneracoes
        )

        employees[matricula] = {
            "reg": matricula,
            "name": name,
            "role": role,
            "type": typeE,
            "workplace": workplace,
            "active": activeE,
            "income": {
                "total": round(total_bruto, 2),
                "wage": sal_base + outras_remuneracoes,
                "perks": {
                    "total": round(total_indenizacoes, 2),
                    "food": alimentacao,
                    "transportation": transporte,
                    "ferias em pecunia": ferias_pc,
                },
                "other": {  # Gratificações
                    "total": round(total_gratificacoes, 2),
                    "trust_position": comissao,
                    "others_total": grat_natal + permanencia + remuneracoes_temporarias,
                    "others": {
                        "Gratificação Natalina": grat_natal,
                        "Abono de Permanência": permanencia,
                        "Outras Remunerações Temporárias": remuneracoes_temporarias,
                    },
                },
            },
            "discounts": {  # Discounts Object. Using abs to garantee numbers are positivo (spreadsheet have negative discounts).
                "total": abs(total_descontos),
                "prev_contribution": abs(contribuicao_previdenciaria),
                "income_tax": abs(imposto_renda),
            },
        }
        curr_row += 1
        if curr_row >= end_row:
            break

    return employees


# June 2019
def parse_june_19(file_name):
    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)

    typeE = parser.type_employee(file_name)
    activeE = "inativos" not in file_name
    employees = {}
    curr_row = 0
    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = str(int(row[0]))  # convert to string by removing the '.0'
        name = row[1].strip()  # removes blank spaces present in some cells
        role = row[2]  # cargo
        workplace = row[3]  # Lotação
        sal_base = format_value(row[4])  # Salário Base
        outras_remuneracoes = format_value(
            row[5]
        )  # Outras Verbas Remuneratórias, Legais ou Judiciais
        comissao = format_value(row[6])  # Função de Confiança ou Cargo em Comissão
        grat_natal = format_value(row[7])  # Gratificação Natalina (13º  sal.)
        qualificacao = format_value(row[8])  # Gratificação de qualificação
        permanencia = format_value(row[9])  # Abono de Permanência
        contribuicao_previdenciaria = format_value(row[11])
        imposto_renda = format_value(row[12])
        total_descontos = format_value(row[13])
        alimentacao = format_value(row[15])  # Auxilio alimentação
        transporte = format_value(row[16])  # Auxilio transporte
        total_indenizacoes = alimentacao + transporte
        total_gratificacoes = grat_natal + comissao + permanencia + qualificacao
        total_bruto = (
            total_gratificacoes + total_indenizacoes + sal_base + outras_remuneracoes
        )

        employees[matricula] = {
            "reg": matricula,
            "name": name,
            "role": role,
            "type": typeE,
            "workplace": workplace,
            "active": activeE,
            "income": {
                "total": round(total_bruto, 2),
                "wage": sal_base + outras_remuneracoes,
                "perks": {
                    "total": total_indenizacoes,
                    "food": alimentacao,
                    "transportation": transporte,
                },
                "other": {  # Gratificações
                    "total": grat_natal + comissao + permanencia + qualificacao,
                    "trust_position": comissao,
                    "others_total": grat_natal + permanencia + qualificacao,
                    "others": {
                        "Gratificação Natalina": grat_natal,
                        "Abono de Permanência": permanencia,
                        "Gratificação de Qualificação": qualificacao,
                    },
                },
            },
            "discounts": {  # Discounts Object. Using abs to garantee numbers are positivo (spreadsheet have negative discounts).
                "total": abs(total_descontos),
                "prev_contribution": abs(contribuicao_previdenciaria),
                "income_tax": abs(imposto_renda),
            },
        }
        curr_row += 1
        if curr_row >= end_row:
            break

    return employees
