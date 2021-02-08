import pandas as pd
import math
import parser

# Due to the different format of the spreadsheets, a specific parser is required for a few months
# This class contains the parsers for active servants:
# parse_jan_to_june_19: January to June 2019


# Adjust existing spreadsheet variations
def format_value(element):
    if element == None:
        return 0.0
    elif type(element) == str and "-" in element:
        return 0.0
    elif element == "#N/DISP":
        return 0.0
    return element


# Parser for Active Members - January 2019
def parse_jan_to_june_19(file_name):
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
        sal_base = format_value(row[4])  # Remuneração Cargo Efetivo
        outras_remuneracoes = format_value(
            row[5]
        )  # Outras Verbas Remuneratórias, Legais ou Judiciais
        comissao = format_value(row[6])  # Função de Confiança ou Cargo em Comissão
        grat_natal = format_value(row[7])  # Gratificação Natalina (13º  sal.)
        ferias = format_value(row[8])  # Férias (1/3 Constiticional)
        grat_qualificacao = format_value(row[9])  # Gratificação de Qualificação
        permanencia = format_value(row[10])  # Abono de Permanência
        contribuicao_previdenciaria = format_value(row[12])
        imposto_renda = format_value(row[13])
        teto_constitucional = format_value(row[14])  # Retenção por teto constitucional
        total_descontos = format_value(row[15])
        transporte = format_value(row[17])  # Auxilio Transporte
        alimentacao = format_value(row[18])  # Auxilio alimentação
        creche = format_value(row[19])  # Auxílio Creche
        total_indenizacoes = alimentacao + transporte + creche
        total_gratificacoes = (
            comissao + grat_natal + ferias + permanencia + grat_qualificacao
        )
        total_bruto = (
            total_indenizacoes + total_gratificacoes + sal_base + outras_remuneracoes
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
                "wage": round(sal_base + outras_remuneracoes, 2),
                "perks": {
                    "total": total_indenizacoes,
                    "food": alimentacao,
                    "transportation": transporte,
                    "pre_school": creche,
                },
                "other": {  # Gratificações
                    "total": round(total_gratificacoes, 2),
                    "trust_position": comissao,
                    "others_total": grat_natal
                    + ferias
                    + permanencia
                    + grat_qualificacao,
                    "others": {
                        "Gratificação Natalina": grat_natal,
                        "Férias (1/3 constitucional)": ferias,
                        "Abono de Permanência": permanencia,
                        "Gratificação de Qualificação": grat_qualificacao,
                    },
                },
            },
            "discounts": {  # Discounts Object. Using abs to garantee numbers are positivo (spreadsheet have negative discounts).
                "total": abs(total_descontos),
                "prev_contribution": abs(contribuicao_previdenciaria),
                # Retenção por teto constitucional
                "ceil_retention": abs(teto_constitucional),
                "income_tax": abs(imposto_renda),
            },
        }

        curr_row += 1
        if curr_row >= end_row:
            break

    return employees
