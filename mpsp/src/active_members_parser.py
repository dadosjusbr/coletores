import pandas as pd
import math
import parser

# Due to the different format of the spreadsheets, a specific parser is required for a few months
# Contains the parsers for monthly remuneration worksheets for active members:
# parse_jan_19: January 2019
# parse_feb_to_may_19: February to May 2019
# parse_jun_19: June 2019

# Adjust existing spreadsheet variations
def format_value(element):
    if element == None:
        return 0.0
    if type(element) == str and "-" in element:
        return 0.0
    if element == "#N/DISP":
        return 0.0
    return element


# Parser for Active Members - January 2019
def parse_jan_19(file_name):
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
        alimentacao = format_value(row[16])  # Auxilio alimentação
        moradia = format_value(row[17])  # Auxilio moradia
        comissao = format_value(row[6])  # Função de Confiança ou Cargo em Comissão
        grat_natal = format_value(row[7])  # Gratificação Natalina (13º  sal.)
        ferias = format_value(row[8])  # Férias (1/3 Constiticional)
        permanencia = format_value(row[9])  # Abono de Permanência
        remuneracoes_temporarias = format_value(
            row[18]
        )  # Outras Remunerações Temporárias
        total_descontos = format_value(row[14])
        contribuicao_previdenciaria = format_value(row[11])
        teto_constitucional = format_value(row[13])  # Retenção por teto constitucional
        imposto_renda = format_value(row[12])
        total_indenizacoes = alimentacao + moradia
        total_gratificacoes = (
            comissao + grat_natal + ferias + permanencia + remuneracoes_temporarias
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
                "wage": sal_base + outras_remuneracoes,
                "perks": {
                    "total": round(total_indenizacoes, 2),
                    "food": alimentacao,
                    "housing_aid": moradia,
                },
                "other": {  # Gratificações
                    "total": round(total_gratificacoes, 2),
                    "trust_position": comissao,
                    "others_total": grat_natal
                    + ferias
                    + permanencia
                    + remuneracoes_temporarias,
                    "others": {
                        "Gratificação Natalina": grat_natal,
                        "Férias (1/3 constitucional)": ferias,
                        "Abono de Permanência": permanencia,
                        "Outras remunerações temporárias": remuneracoes_temporarias,
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
        if curr_row > end_row:
            break

    return employees


# Parser for Active Members - February to May 2019
def parse_feb_to_may_19(file_name):
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
        alimentacao = format_value(row[16])  # Auxilio alimentação
        ferias_pc = format_value(row[17])  # Férias em pecunia
        comissao = format_value(row[6])  # Função de Confiança ou Cargo em Comissão
        grat_natal = format_value(row[7])  # Gratificação Natalina (13º  sal.)
        ferias = format_value(row[8])  # Férias (1/3 Constiticional)
        permanencia = format_value(row[9])  # Abono de Permanência
        remuneracoes_temporarias = format_value(
            row[18]
        )  # Outras Remunerações Temporárias
        total_descontos = format_value(row[14])
        contribuicao_previdenciaria = format_value(row[11])
        teto_constitucional = format_value(row[13])  # Retenção por teto constitucional
        imposto_renda = format_value(row[12])
        total_indenizacoes = alimentacao + ferias_pc
        total_gratificacoes = (
            comissao + grat_natal + ferias + permanencia + remuneracoes_temporarias
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
                    "ferias em pecunia": ferias_pc,
                },
                "other": {  # Gratificações
                    "total": round(total_gratificacoes, 2),
                    "trust_position": comissao,
                    "others_total": grat_natal
                    + ferias
                    + permanencia
                    + remuneracoes_temporarias,
                    "others": {
                        "Gratificação Natalina": grat_natal,
                        "Férias (1/3 constitucional)": ferias,
                        "Abono de Permanência": permanencia,
                        "Outras remunerações temporárias": remuneracoes_temporarias,
                    },
                },
            },
            "discounts": {  # Discounts Object. Using abs to garantee numbers are positivo (spreadsheet have negative discounts).
                "total": abs(total_descontos),
                "prev_contribution": abs(contribuicao_previdenciaria),
                "ceil_retention": abs(teto_constitucional),
                "income_tax": abs(imposto_renda),
            },
        }

        curr_row += 1
        if curr_row > end_row:
            break

    return employees


# Parser for Active Members - June 2019
def parse_jun_19(file_name):
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
        alimentacao = format_value(row[15])  # Auxilio alimentação
        ferias_pc = format_value(row[16])  # Férias em pecunia
        licensa_pc = format_value(row[17])  # Licença Prêmio em Pecúnia
        comissao = format_value(row[6])  # Função de Confiança ou Cargo em Comissão
        grat_natal = format_value(row[7])  # Gratificação Natalina (13º  sal.)
        ferias = format_value(row[8])  # Férias (1/3 Constiticional)
        permanencia = format_value(row[9])  # Abono de Permanência
        remuneracoes_temporarias = format_value(
            row[18]
        )  # Outras Remunerações Temporárias
        total_descontos = format_value(row[13])
        contribuicao_previdenciaria = format_value(row[11])
        imposto_renda = format_value(row[12])
        total_indenizacoes = alimentacao + ferias_pc + licensa_pc
        total_gratificacoes = (
            comissao + grat_natal + ferias + permanencia + remuneracoes_temporarias
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
                "wage": sal_base + outras_remuneracoes,
                "perks": {
                    "total": round(total_indenizacoes, 2),
                    "food": alimentacao,
                    "ferias em pecunia": ferias_pc,
                    "LP em pecunia": licensa_pc,
                },
                "other": {  # Gratificações
                    "total": round(total_gratificacoes, 2),
                    "trust_position": comissao,
                    "others_total": grat_natal
                    + ferias
                    + permanencia
                    + remuneracoes_temporarias,
                    "others": {
                        "Gratificação Natalina": grat_natal,
                        "Férias (1/3 constitucional)": ferias,
                        "Abono de Permanência": permanencia,
                        "Outras remunerações temporarias": remuneracoes_temporarias,
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
        if curr_row > end_row:
            break

    return employees

# January  to  May - 2018
def parse_jan_to_may_18(file_name):
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
        ferias = format_value(row[8])  # Férias (1/3 Constiticional)
        permanencia = format_value(row[9])  # Abono de Permanência
        contribuicao_previdenciaria = format_value(row[11])
        imposto_renda = format_value(row[12])
        teto_constitucional = format_value(row[13])  # Retenção por teto constitucional
        total_descontos = format_value(row[14])
        
        alimentacao = format_value(row[16])  # Auxilio alimentação
        moradia = format_value(row[17])  # Auxilio moradia
        ferias_pc = format_value(row[18])
        licensa_pc = format_value(row[19])
        outras_remuneracoes_temporarias = format_value(
            row[20]
        )  # Gratificação Cumulativa, Gratific. Serv. Nat. Especial Art. 2 Ato 40, Gratific. Atuação Especial Ato 709/2011
        total_indenizacoes = alimentacao + moradia + ferias_pc + licensa_pc
        total_gratificacoes = (
            comissao + grat_natal + ferias + permanencia + outras_remuneracoes_temporarias
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
                "wage": sal_base + outras_remuneracoes,
                "perks": {
                    "total": round(total_indenizacoes, 2),
                    "food": alimentacao,
                    "housing_aid": moradia,
                    "vacation_pecuniary": ferias_pc,
                    "premium_license_pecuniary": licensa_pc
                },
                "other": {  # Gratificações
                    "total": round(total_gratificacoes, 2),
                    "trust_position": comissao,
                    "others_total": grat_natal
                    + ferias
                    + permanencia
                    + outras_remuneracoes_temporarias,
                    "others": {
                        "Gratificação Natalina": grat_natal,
                        "Férias (1/3 constitucional)": ferias,
                        "Abono de Permanência": permanencia,
                        "Outras remunerações temporárias": outras_remuneracoes_temporarias,
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
        if curr_row > end_row:
            break

    return employees

# Juny to December - 2018
def parse_june_to_dec_18(file_name):
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
        ferias = format_value(row[8])  # Férias (1/3 Constiticional)
        permanencia = format_value(row[9])  # Abono de Permanência
        contribuicao_previdenciaria = format_value(row[11])
        imposto_renda = format_value(row[12])
        teto_constitucional = format_value(row[13])  # Retenção por teto constitucional
        total_descontos = format_value(row[14])
        
        alimentacao = format_value(row[16])  # Auxilio alimentação
        moradia = format_value(row[17])  # Auxilio moradia
        ferias_pc = format_value(row[18])
        outras_remuneracoes_temporarias = format_value(
            row[19]
        )  # Gratificação Cumulativa, Gratific. Serv. Nat. Especial Art. 2 Ato 40, Gratific. Atuação Especial Ato 709/2011
        total_indenizacoes = alimentacao + moradia + ferias_pc
        total_gratificacoes = (
            comissao + grat_natal + ferias + permanencia + outras_remuneracoes_temporarias
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
                "wage": sal_base + outras_remuneracoes,
                "perks": {
                    "total": round(total_indenizacoes, 2),
                    "food": alimentacao,
                    "housing_aid": moradia,
                    "vacation_pecuniary": ferias_pc,
                },
                "other": {  # Gratificações
                    "total": round(total_gratificacoes, 2),
                    "trust_position": comissao,
                    "others_total": grat_natal
                    + ferias
                    + permanencia
                    + outras_remuneracoes_temporarias,
                    "others": {
                        "Gratificação Natalina": grat_natal,
                        "Férias (1/3 constitucional)": ferias,
                        "Abono de Permanência": permanencia,
                        "Outras remunerações temporárias": outras_remuneracoes_temporarias,
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
        if curr_row > end_row:
            break

    return employees