import pandas as pd
import numpy as np
import sys
import os
import datetime
import json


def parse(court, year, file_names, output_path, crawler_version):
    now = datetime.datetime.now()
    current_month = now.month
    current_year = now.year
    months = list(range(1, 13))
    files = []

    for month in months:
        if year == current_year and month >= current_month:
            break
        employees = {}
        employees.update(parse_files(court, file_names, month, year))
        file_path = save_file(court, month, year, output_path, crawler_version, employees)
        files.append(file_path)

    return files


def parse_files(court, file_name, month, year):
    employees = {}
    files = select_month(file_name, str(month))
    print(files)
    data = read_data(files[0])
    data_indemnities = read_data(files[1])
    if year == '2018':
        print(month)
        if month in [1]:
            if "-Membros Ativos" in files[0]:
                employees.update(parse_employees_jan_2018(data))
            if "-Verbas Indenizatórias" in files[1]:
                employees.update(update_employees_indemnities(data_indemnities, employees))
        elif month in [2, 3, 4]:
            if "-Membros Ativos" in files[0]:
                employees.update(parse_employees_feb_2018(data))
            if "-Verbas Indenizatórias" in files[1]:
                employees.update(update_employees_indemnities(data_indemnities, employees))
        elif month in [5]:
            if "-Membros Ativos" in files[0]:
                employees.update(parse_employees_may_2018(data))
            if "-Verbas Indenizatórias" in files[1]:
                employees.update(update_employees_indemnities(data_indemnities, employees))
        elif month in [6]:
            if "-Membros Ativos" in files[0]:
                employees.update(parse_employees_jun_2018(data))
            if "-Verbas Indenizatórias" in files[1]:
                employees.update(update_employees_indemnities(data_indemnities, employees))
        elif month in [7, 10, 11]:
            if "-Membros Ativos" in files[0]:
                employees.update(parse_employees_jul_2018(data))
            if "-Verbas Indenizatórias" in files[1]:
                employees.update(update_employees_indemnities(data_indemnities, employees))
        elif month in [8]:
            if "-Membros Ativos" in files[0]:
                employees.update(parse_employees_aug_2018(data))
            if "-Verbas Indenizatórias" in files[1]:
                employees.update(update_employees_indemnities(data_indemnities, employees))
        elif month in [9]:
            if "-Membros Ativos" in files[0]:
                employees.update(parse_employees_set_2018(data))
            if "-Verbas Indenizatórias" in files[1]:
                employees.update(update_employees_indemnities(data_indemnities, employees))
        elif month in [12]:
            if "-Membros Ativos" in files[0]:
                employees.update(parse_employees_dec_2018(data))
            if "-Verbas Indenizatórias" in files[1]:
                employees.update(update_employees_indemnities(data_indemnities, employees))

    return employees


def parse_employees_jan_2018(data):
    rows = data.to_numpy()
    employees = {}

    for row in rows[3:]:  # Linhas iniciais são cabeçalhos, dados a partir da terceira linha
        row = np.where(row == "-", 0, row)
        nome = row[0]
        if nome != "0":
            cargo_efetivo = row[1]
            # if "Cargo: " in cargo_efetivo:
            #     holder = cargo_efetivo.split("\n")
            #     cargo_efetivo = holder[0][7:]
            lotacao = row[2]
            remuneracao_cargo_efetivo = float(row[4])
            outras_verbas_legais = float(row[5])
            confianca_comissao = float(
                row[6]
            )  # Função de Confiança ou Cargo em Comissão
            ferias = float(row[7])
            permanencia = float(row[8])  # Abono de Permanência
            indenizatorias = float(row[9])
            outras_remuneracoes_temporarias = float(row[10])
            teto_constitucional = abs(
                float(row[12])
            )  # Retenção por Teto Constitucional
            imp_renda = abs(float(row[13]))  # Imposto de Renda
            previdencia = abs(float(row[14]))  # Contribuição Previdenciária
            total_gratificacoes = confianca_comissao + ferias + permanencia
            total_desconto_folha = teto_constitucional + imp_renda + previdencia
            total_folha = (
                remuneracao_cargo_efetivo
                + indenizatorias
                + outras_remuneracoes_temporarias
                + total_gratificacoes
                + outras_verbas_legais
            )  # Total da folha
            indenizatorias_suplementar = float(row[16])
            outras_remuneracoes_temporarias_suplementar = float(row[17])
            total_indenizacao = abs(indenizatorias + indenizatorias_suplementar)
            total_bruto = (
                total_folha
                + indenizatorias_suplementar
                + outras_remuneracoes_temporarias_suplementar
            )

            employees[nome] = {
                "reg": "",
                "name": nome,
                "role": cargo_efetivo,
                "type": "membro",
                "workplace": lotacao,
                "active": True,
                "income": {
                    "total": round(total_bruto, 2),
                    # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                    "wage": round(
                        remuneracao_cargo_efetivo + outras_remuneracoes_temporarias + outras_verbas_legais, 2
                    ),
                    "perks": {"total": round(total_indenizacao, 2)},
                    "other": {  # Gratificações
                        "total": round(total_gratificacoes, 2),
                        "trust_position": confianca_comissao,
                        "others_total": round(ferias + permanencia, 2),
                        "others": {
                            "Férias (1/3 constitucional)": ferias,
                            "Abono de Permanência": permanencia,
                        },
                    },
                },
                "discounts": {  # Discounts Object. Using abs to garantee numbers are positive (spreadsheet have negative discounts).
                    "total": round(total_desconto_folha, 2),
                    "prev_contribution": previdencia,
                    # Retenção por teto constitucional
                    "ceil_retention": teto_constitucional,
                    "income_tax": round(imp_renda, 2),
                },
            }
    # print(employees)
    return employees


def parse_employees_feb_2018(data):
    rows = data.to_numpy()
    employees = {}

    for row in rows[3:]:  # Linhas iniciais são cabeçalhos, dados a partir da terceira linha
        row = np.where(row == "-", 0, row)
        nome = row[0]
        if nome != "0":
            cargo_efetivo = row[1]
            # if "Cargo: " in cargo_efetivo:
            #     holder = cargo_efetivo.split("\n")
            #     cargo_efetivo = holder[0][7:]
            lotacao = row[2]
            remuneracao_cargo_efetivo = float(row[4])
            outras_verbas_legais = float(row[5])
            confianca_comissao = float(
                row[6]
            )  # Função de Confiança ou Cargo em Comissão
            ferias = float(row[7])
            permanencia = float(row[8])  # Abono de Permanência
            indenizatorias = float(row[9])
            outras_remuneracoes_temporarias = float(row[10])
            teto_constitucional = abs(
                float(row[12])
            )  # Retenção por Teto Constitucional
            imp_renda = abs(float(row[13]))  # Imposto de Renda
            previdencia = abs(float(row[14]))  # Contribuição Previdenciária
            total_gratificacoes = confianca_comissao + ferias + permanencia
            total_desconto_folha = teto_constitucional + imp_renda + previdencia
            total_folha = (
                remuneracao_cargo_efetivo
                + indenizatorias
                + outras_remuneracoes_temporarias
                + total_gratificacoes
                + outras_verbas_legais
            )  # Total da folha
            indenizatorias_suplementar = float(row[16])
            total_indenizacao = abs(indenizatorias + indenizatorias_suplementar)
            total_bruto = (
                total_folha
                + indenizatorias_suplementar
            )

            employees[nome] = {
                "reg": "",
                "name": nome,
                "role": cargo_efetivo,
                "type": "membro",
                "workplace": lotacao,
                "active": True,
                "income": {
                    "total": round(total_bruto, 2),
                    # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                    "wage": round(
                        remuneracao_cargo_efetivo + outras_remuneracoes_temporarias + outras_verbas_legais, 2
                    ),
                    "perks": {"total": round(total_indenizacao, 2)},
                    "other": {  # Gratificações
                        "total": round(total_gratificacoes, 2),
                        "trust_position": confianca_comissao,
                        "others_total": round(ferias + permanencia, 2),
                        "others": {
                            "Férias (1/3 constitucional)": ferias,
                            "Abono de Permanência": permanencia,
                        },
                    },
                },
                "discounts": {  # Discounts Object. Using abs to garantee numbers are positive (spreadsheet have negative discounts).
                    "total": round(total_desconto_folha, 2),
                    "prev_contribution": previdencia,
                    # Retenção por teto constitucional
                    "ceil_retention": teto_constitucional,
                    "income_tax": round(imp_renda, 2),
                },
            }
    # print(employees)
    return employees


def parse_employees_may_2018(data):
    rows = data.to_numpy()
    employees = {}

    for row in rows[3:]:  # Linhas iniciais são cabeçalhos, dados a partir da terceira linha
        row = np.where(row == "-", 0, row)
        nome = row[0]
        if nome != "0":
            cargo_efetivo = row[1]
            # if "Cargo: " in cargo_efetivo:
            #     holder = cargo_efetivo.split("\n")
            #     cargo_efetivo = holder[0][7:]
            lotacao = row[2]
            remuneracao_cargo_efetivo = float(row[4])
            outras_verbas_legais = float(row[5])
            confianca_comissao = float(
                row[6]
            )  # Função de Confiança ou Cargo em Comissão
            ferias = float(row[7])
            permanencia = float(row[8])  # Abono de Permanência
            indenizatorias = float(row[9])
            outras_remuneracoes_temporarias = float(row[10])
            teto_constitucional = abs(
                float(row[12])
            )  # Retenção por Teto Constitucional
            imp_renda = abs(float(row[13]))  # Imposto de Renda
            previdencia = abs(float(row[14]))  # Contribuição Previdenciária
            gratificacao_natalina = float(row[16])
            total_gratificacoes = confianca_comissao + ferias + permanencia + gratificacao_natalina
            total_desconto_folha = teto_constitucional + imp_renda + previdencia
            total_folha = (
                remuneracao_cargo_efetivo
                + indenizatorias
                + outras_remuneracoes_temporarias
                + total_gratificacoes
                + outras_verbas_legais
            )  # Total da folha
            indenizatorias_suplementar = float(row[18])
            total_indenizacao = abs(indenizatorias + indenizatorias_suplementar)
            total_bruto = (
                total_folha
                + indenizatorias_suplementar
            )

            employees[nome] = {
                "reg": "",
                "name": nome,
                "role": cargo_efetivo,
                "type": "membro",
                "workplace": lotacao,
                "active": True,
                "income": {
                    "total": round(total_bruto, 2),
                    # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                    "wage": round(
                        remuneracao_cargo_efetivo + outras_remuneracoes_temporarias + outras_verbas_legais, 2
                    ),
                    "perks": {"total": round(total_indenizacao, 2)},
                    "other": {  # Gratificações
                        "total": round(total_gratificacoes, 2),
                        "trust_position": confianca_comissao,
                        "others_total": round(ferias + permanencia, 2),
                        "others": {
                            "Gratificação Natalina": gratificacao_natalina,
                            "Férias (1/3 constitucional)": ferias,
                            "Abono de Permanência": permanencia,
                        },
                    },
                },
                "discounts": {  # Discounts Object. Using abs to garantee numbers are positive (spreadsheet have negative discounts).
                    "total": round(total_desconto_folha, 2),
                    "prev_contribution": previdencia,
                    # Retenção por teto constitucional
                    "ceil_retention": teto_constitucional,
                    "income_tax": round(imp_renda, 2),
                },
            }
    # print(employees)
    return employees


def parse_employees_jun_2018(data):
    rows = data.to_numpy()
    employees = {}

    for row in rows[3:]:  # Linhas iniciais são cabeçalhos, dados a partir da terceira linha
        row = np.where(row == "-", 0, row)
        nome = row[0]
        if nome != "0":
            cargo_efetivo = row[1]
            # if "Cargo: " in cargo_efetivo:
            #     holder = cargo_efetivo.split("\n")
            #     cargo_efetivo = holder[0][7:]
            lotacao = row[2]
            remuneracao_cargo_efetivo = float(row[4])
            outras_verbas_legais = float(row[5])
            confianca_comissao = float(
                row[6]
            )  # Função de Confiança ou Cargo em Comissão
            ferias = float(row[7])
            permanencia = float(row[8])  # Abono de Permanência
            indenizatorias = float(row[9])
            outras_remuneracoes_temporarias = float(row[10])
            teto_constitucional = abs(
                float(row[12])
            )  # Retenção por Teto Constitucional
            imp_renda = abs(float(row[13]))  # Imposto de Renda
            previdencia = abs(float(row[14]))  # Contribuição Previdenciária
            total_gratificacoes = confianca_comissao + ferias + permanencia
            total_desconto_folha = teto_constitucional + imp_renda + previdencia
            total_folha = (
                remuneracao_cargo_efetivo
                + indenizatorias
                + outras_remuneracoes_temporarias
                + total_gratificacoes
                + outras_verbas_legais
            )  # Total da folha
            ferias_suplementar = float(row[16])
            indenizatorias_suplementar = float(row[17])
            outras_remuneracoes_temporarias_suplementar = float(row[18])
            total_indenizacao = abs(indenizatorias + indenizatorias_suplementar)
            total_bruto = (
                total_folha
                + indenizatorias_suplementar
                + outras_remuneracoes_temporarias_suplementar
                + ferias_suplementar
            )

            employees[nome] = {
                "reg": "",
                "name": nome,
                "role": cargo_efetivo,
                "type": "membro",
                "workplace": lotacao,
                "active": True,
                "income": {
                    "total": round(total_bruto, 2),
                    # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                    "wage": round(
                        remuneracao_cargo_efetivo + outras_remuneracoes_temporarias + outras_verbas_legais, 2
                    ),
                    "perks": {"total": round(total_indenizacao, 2)},
                    "other": {  # Gratificações
                        "total": round(total_gratificacoes, 2),
                        "trust_position": confianca_comissao,
                        "others_total": round(ferias + permanencia, 2),
                        "others": {
                            "Férias (1/3 constitucional)": ferias,
                            "Abono de Permanência": permanencia,
                        },
                    },
                },
                "discounts": {  # Discounts Object. Using abs to garantee numbers are positive (spreadsheet have negative discounts).
                    "total": round(total_desconto_folha, 2),
                    "prev_contribution": previdencia,
                    # Retenção por teto constitucional
                    "ceil_retention": teto_constitucional,
                    "income_tax": round(imp_renda, 2),
                },
            }
    # print(employees)
    return employees


def parse_employees_jul_2018(data):
    rows = data.to_numpy()
    employees = {}

    for row in rows[3:]:  # Linhas iniciais são cabeçalhos, dados a partir da terceira linha
        row = np.where(row == "-", 0, row)
        nome = row[0]
        if nome != "0":
            cargo_efetivo = row[1]
            # if "Cargo: " in cargo_efetivo:
            #     holder = cargo_efetivo.split("\n")
            #     cargo_efetivo = holder[0][7:]
            lotacao = row[2]
            remuneracao_cargo_efetivo = float(row[4])
            outras_verbas_legais = float(row[5])
            confianca_comissao = float(
                row[6]
            )  # Função de Confiança ou Cargo em Comissão
            ferias = float(row[7])
            permanencia = float(row[8])  # Abono de Permanência
            indenizatorias = float(row[9])
            outras_remuneracoes_temporarias = float(row[10])
            teto_constitucional = abs(
                float(row[12])
            )  # Retenção por Teto Constitucional
            imp_renda = abs(float(row[13]))  # Imposto de Renda
            previdencia = abs(float(row[14]))  # Contribuição Previdenciária
            indenizatorias_suplementar = float(row[16])
            outras_remuneracoes_temporarias_suplementar = float(row[17])
            imp_renda_suplementar = abs(float(row[19]))
            total_gratificacoes = confianca_comissao + ferias + permanencia
            total_desconto_folha = teto_constitucional + imp_renda + previdencia + imp_renda_suplementar
            total_folha = (
                remuneracao_cargo_efetivo
                + indenizatorias
                + outras_remuneracoes_temporarias
                + total_gratificacoes
                + outras_verbas_legais
            )  # Total da folha
            total_indenizacao = abs(indenizatorias + indenizatorias_suplementar)
            total_bruto = (
                total_folha
                + indenizatorias_suplementar
                + outras_remuneracoes_temporarias_suplementar
            )

            employees[nome] = {
                "reg": "",
                "name": nome,
                "role": cargo_efetivo,
                "type": "membro",
                "workplace": lotacao,
                "active": True,
                "income": {
                    "total": round(total_bruto, 2),
                    # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                    "wage": round(
                        remuneracao_cargo_efetivo + outras_remuneracoes_temporarias + outras_verbas_legais, 2
                    ),
                    "perks": {"total": round(total_indenizacao, 2)},
                    "other": {  # Gratificações
                        "total": round(total_gratificacoes, 2),
                        "trust_position": confianca_comissao,
                        "others_total": round(ferias + permanencia, 2),
                        "others": {
                            "Férias (1/3 constitucional)": ferias,
                            "Abono de Permanência": permanencia,
                        },
                    },
                },
                "discounts": {  # Discounts Object. Using abs to garantee numbers are positive (spreadsheet have negative discounts).
                    "total": round(total_desconto_folha, 2),
                    "prev_contribution": previdencia,
                    # Retenção por teto constitucional
                    "ceil_retention": teto_constitucional,
                    "income_tax": round(imp_renda, 2),
                },
            }
    # print(employees)
    return employees


def parse_employees_aug_2018(data):
    rows = data.to_numpy()
    employees = {}

    for row in rows[3:]:  # Linhas iniciais são cabeçalhos, dados a partir da terceira linha
        row = np.where(row == "-", 0, row)
        nome = row[0]
        if nome != "0":
            cargo_efetivo = row[1]
            # if "Cargo: " in cargo_efetivo:
            #     holder = cargo_efetivo.split("\n")
            #     cargo_efetivo = holder[0][7:]
            lotacao = row[2]
            remuneracao_cargo_efetivo = float(row[4])
            outras_verbas_legais = float(row[5])
            confianca_comissao = float(
                row[6]
            )  # Função de Confiança ou Cargo em Comissão
            ferias = float(row[7])
            permanencia = float(row[8])  # Abono de Permanência
            indenizatorias = float(row[9])
            outras_remuneracoes_temporarias = float(row[10])
            teto_constitucional = abs(
                float(row[12])
            )  # Retenção por Teto Constitucional
            imp_renda = abs(float(row[13]))  # Imposto de Renda
            previdencia = abs(float(row[14]))  # Contribuição Previdenciária
            ferias_suplementar = float(row[16])
            indenizatorias_suplementar = float(row[17])
            imp_renda_suplementar = abs(float(row[19]))
            total_gratificacoes = confianca_comissao + ferias + permanencia
            total_desconto_folha = teto_constitucional + imp_renda + previdencia + imp_renda_suplementar
            total_folha = (
                remuneracao_cargo_efetivo
                + indenizatorias
                + outras_remuneracoes_temporarias
                + total_gratificacoes
                + outras_verbas_legais
            )  # Total da folha
            total_indenizacao = abs(indenizatorias + indenizatorias_suplementar)
            total_bruto = (
                total_folha
                + indenizatorias_suplementar
                + ferias_suplementar
            )

            employees[nome] = {
                "reg": "",
                "name": nome,
                "role": cargo_efetivo,
                "type": "membro",
                "workplace": lotacao,
                "active": True,
                "income": {
                    "total": round(total_bruto, 2),
                    # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                    "wage": round(
                        remuneracao_cargo_efetivo + outras_remuneracoes_temporarias + outras_verbas_legais, 2
                    ),
                    "perks": {"total": round(total_indenizacao, 2)},
                    "other": {  # Gratificações
                        "total": round(total_gratificacoes, 2),
                        "trust_position": confianca_comissao,
                        "others_total": round(ferias + permanencia, 2),
                        "others": {
                            "Férias (1/3 constitucional)": ferias,
                            "Abono de Permanência": permanencia,
                        },
                    },
                },
                "discounts": {  # Discounts Object. Using abs to garantee numbers are positive (spreadsheet have negative discounts).
                    "total": round(total_desconto_folha, 2),
                    "prev_contribution": previdencia,
                    # Retenção por teto constitucional
                    "ceil_retention": teto_constitucional,
                    "income_tax": round(imp_renda, 2),
                },
            }
    # print(employees)
    return employees


def parse_employees_set_2018(data):
    rows = data.to_numpy()
    employees = {}

    for row in rows[3:]:  # Linhas iniciais são cabeçalhos, dados a partir da terceira linha
        row = np.where(row == "-", 0, row)
        nome = row[0]
        if nome != "0":
            cargo_efetivo = row[1]
            # if "Cargo: " in cargo_efetivo:
            #     holder = cargo_efetivo.split("\n")
            #     cargo_efetivo = holder[0][7:]
            lotacao = row[2]
            remuneracao_cargo_efetivo = float(row[4])
            outras_verbas_legais = float(row[5])
            gratificacao_natalina = float(row[6])
            confianca_comissao = float(
                row[7]
            )  # Função de Confiança ou Cargo em Comissão
            ferias = float(row[8])
            permanencia = float(row[9])  # Abono de Permanência
            indenizatorias = float(row[10])
            outras_remuneracoes_temporarias = float(row[11])
            teto_constitucional = abs(
                float(row[13])
            )  # Retenção por Teto Constitucional
            imp_renda = abs(float(row[14]))  # Imposto de Renda
            previdencia = abs(float(row[15]))  # Contribuição Previdenciária
            total_gratificacoes = confianca_comissao + ferias + permanencia + gratificacao_natalina
            total_desconto_folha = teto_constitucional + imp_renda + previdencia
            total_folha = (
                remuneracao_cargo_efetivo
                + indenizatorias
                + outras_remuneracoes_temporarias
                + total_gratificacoes
                + outras_verbas_legais
            )  # Total da folha
            indenizatorias_suplementar = float(row[17])
            total_indenizacao = abs(indenizatorias + indenizatorias_suplementar)
            total_bruto = (
                total_folha
                + indenizatorias_suplementar
            )

            employees[nome] = {
                "reg": "",
                "name": nome,
                "role": cargo_efetivo,
                "type": "membro",
                "workplace": lotacao,
                "active": True,
                "income": {
                    "total": round(total_bruto, 2),
                    # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                    "wage": round(
                        remuneracao_cargo_efetivo + outras_remuneracoes_temporarias + outras_verbas_legais, 2
                    ),
                    "perks": {"total": round(total_indenizacao, 2)},
                    "other": {  # Gratificações
                        "total": round(total_gratificacoes, 2),
                        "trust_position": confianca_comissao,
                        "others_total": round(ferias + permanencia, 2),
                        "others": {
                            "Gratificação Natalina": gratificacao_natalina,
                            "Férias (1/3 constitucional)": ferias,
                            "Abono de Permanência": permanencia,
                        },
                    },
                },
                "discounts": {  # Discounts Object. Using abs to garantee numbers are positive (spreadsheet have negative discounts).
                    "total": round(total_desconto_folha, 2),
                    "prev_contribution": previdencia,
                    # Retenção por teto constitucional
                    "ceil_retention": teto_constitucional,
                    "income_tax": round(imp_renda, 2),
                },
            }
    # print(employees)
    return employees


def parse_employees_dec_2018(data):
    rows = data.to_numpy()
    employees = {}

    for row in rows[3:]:  # Linhas iniciais são cabeçalhos, dados a partir da terceira linha
        row = np.where(row == "-", 0, row)
        nome = row[0]
        if nome != "0":
            cargo_efetivo = row[1]
            # if "Cargo: " in cargo_efetivo:
            #     holder = cargo_efetivo.split("\n")
            #     cargo_efetivo = holder[0][7:]
            lotacao = row[2]
            remuneracao_cargo_efetivo = float(row[4])
            outras_verbas_legais = float(row[5])
            confianca_comissao = float(
                row[6]
            )  # Função de Confiança ou Cargo em Comissão
            ferias = float(row[7])
            permanencia = float(row[8])  # Abono de Permanência
            indenizatorias = float(row[9])
            outras_remuneracoes_temporarias = float(row[10])
            teto_constitucional = abs(
                float(row[12])
            )  # Retenção por Teto Constitucional
            imp_renda = abs(float(row[13]))  # Imposto de Renda
            previdencia = abs(float(row[14]))  # Contribuição Previdenciária
            gratificacao_natalina_13 = float(row[16])
            permanencia_13 = float(row[17])
            teto_constitucional_13 = abs(float(row[19]))
            imp_renda_13 = abs(float(row[20]))
            previdencia_13 = abs(float(row[21]))
            gratificacao_natalina_suplementar = float(row[23])
            ferias_suplementar = float(row[24])
            permanencia_suplementar = float(row[25])
            indenizatorias_suplementar = float(row[26])
            outras_remuneracoes_temporarias_suplementar = float(row[27])
            imp_renda_suplementar = abs(float(row[29]))
            previdencia_suplementar = abs(float(row[30]))
            total_gratificacoes = confianca_comissao + ferias + permanencia + gratificacao_natalina_13 + permanencia_13 + gratificacao_natalina_suplementar + ferias_suplementar + permanencia_suplementar + outras_remuneracoes_temporarias_suplementar
            total_desconto_folha = teto_constitucional + imp_renda + previdencia + teto_constitucional_13 + imp_renda_13 + previdencia_13 + imp_renda_suplementar + previdencia_suplementar
            total_folha = (
                remuneracao_cargo_efetivo
                + indenizatorias
                + outras_remuneracoes_temporarias
                + total_gratificacoes
                + outras_verbas_legais
            )  # Total da folha

            total_indenizacao = abs(indenizatorias + indenizatorias_suplementar)
            total_bruto = (
                total_folha
                + total_indenizacao
            )

            employees[nome] = {
                "reg": "",
                "name": nome,
                "role": cargo_efetivo,
                "type": "membro",
                "workplace": lotacao,
                "active": True,
                "income": {
                    "total": round(total_bruto, 2),
                    # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                    "wage": round(
                        remuneracao_cargo_efetivo + outras_remuneracoes_temporarias + outras_verbas_legais, 2
                    ),
                    "perks": {"total": round(total_indenizacao, 2)},
                    "other": {  # Gratificações
                        "total": round(total_gratificacoes, 2),
                        "trust_position": confianca_comissao,
                        "others_total": round(ferias + permanencia, 2),
                        "others": {
                            "Gratificação Natalina": gratificacao_natalina_13,
                            "Férias (1/3 constitucional)": ferias,
                            "Abono de Permanência": permanencia,
                        },
                    },
                },
                "discounts": {  # Discounts Object. Using abs to garantee numbers are positive (spreadsheet have negative discounts).
                    "total": round(total_desconto_folha, 2),
                    "prev_contribution": previdencia,
                    # Retenção por teto constitucional
                    "ceil_retention": teto_constitucional,
                    "income_tax": round(imp_renda, 2),
                },
            }
    # print(employees)
    return employees

# def parse_employees(data):
#     rows = data.to_numpy()
#     employees = {}

#     for row in rows[3:]:  # Linhas iniciais são cabeçalhos, dados a partir da terceira linha
#         row = np.where(row == "-", 0, row)
#         nome = row[0]
#         if nome != "0":
#             cargo_efetivo = row[1]
#             # if "Cargo: " in cargo_efetivo:
#             #     holder = cargo_efetivo.split("\n")
#             #     cargo_efetivo = holder[0][7:]
#             lotacao = row[2]
#             remuneracao_cargo_efetivo = float(row[4])
#             confianca_comissao = float(
#                 row[5]
#             )  # Função de Confiança ou Cargo em Comissão
#             ferias = float(row[6])
#             permanencia = float(row[7])  # Abono de Permanência
#             indenizatorias = float(row[8])
#             outras_remuneracoes_temporarias = float(row[9])
#             teto_constitucional = abs(
#                 float(row[11])
#             )  # Retenção por Teto Constitucional
#             imp_renda = abs(float(row[12]))  # Imposto de Renda
#             previdencia = abs(float(row[13]))  # Contribuição Previdenciária
#             total_gratificacoes = confianca_comissao + ferias + permanencia
#             total_desconto_folha = teto_constitucional + imp_renda + previdencia
#             total_folha = (
#                 remuneracao_cargo_efetivo
#                 + indenizatorias
#                 + outras_remuneracoes_temporarias
#                 + total_gratificacoes
#             )  # Total da folha
#             indenizatorias_suplementar = float(row[15])
#             outras_remuneracoes_temporarias_suplementar = float(row[16])
#             imp_renda_suplementar = abs(float(row[18]))
#             total_indenizacao = abs(indenizatorias + indenizatorias_suplementar)
#             total_bruto = (
#                 total_folha
#                 + indenizatorias_suplementar
#                 + outras_remuneracoes_temporarias_suplementar
#             )
#             total_desconto = (
#                 total_desconto_folha + imp_renda_suplementar
#             )

#             employees[nome] = {
#                 "reg": "",
#                 "name": nome,
#                 "role": cargo_efetivo,
#                 "type": "membro",
#                 "workplace": lotacao,
#                 "active": True,
#                 "income": {
#                     "total": round(total_bruto, 2),
#                     # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
#                     "wage": round(
#                         remuneracao_cargo_efetivo + outras_remuneracoes_temporarias, 2
#                     ),
#                     "perks": {"total": round(total_indenizacao, 2)},
#                     "other": {  # Gratificações
#                         "total": round(total_gratificacoes, 2),
#                         "trust_position": confianca_comissao,
#                         "others_total": round(ferias + permanencia, 2),
#                         "others": {
#                             "Férias (1/3 constitucional)": ferias,
#                             "Abono de Permanência": permanencia,
#                         },
#                     },
#                 },
#                 "discounts": {  # Discounts Object. Using abs to garantee numbers are positive (spreadsheet have negative discounts).
#                     "total": round(total_desconto, 2),
#                     "prev_contribution": previdencia,
#                     # Retenção por teto constitucional
#                     "ceil_retention": teto_constitucional,
#                     "income_tax": round(imp_renda + imp_renda_suplementar, 2),
#                 },
#             }
#     # print(employees)
#     return employees


def update_employees_indemnities(data, employees):
    rows = rows = data.to_numpy()

    for row in rows[1:]:
        row = np.where(row == "-", 0, row)
        nome = row[1]
        # Indenizações
        ajuda_de_custo = round(float(row[6]), 2)
        auxilio_alimentacao = round(float(row[7]), 2)
        auxilio_pre_escolar = round(float(row[8]), 2)
        auxilio_educacao = round(float(row[9]), 2)
        auxilio_moradia = round(float(row[10]), 2)
        auxilio_saude = round(float(row[11]), 2)
        auxilio_transporte_estagiarios = round(float(row[12]), 2)
        licenca_premio = round(float(row[13]), 2)
        ferias = round(float(row[14]), 2)
        ressarcimento_veiculo = round(float(row[15]), 2)

        total_indenizatorio = round(ajuda_de_custo + auxilio_alimentacao + auxilio_pre_escolar + 
        auxilio_educacao + auxilio_saude + auxilio_transporte_estagiarios + 
        auxilio_moradia + licenca_premio + ferias + ressarcimento_veiculo, 2)
        
        ajuda_de_custo_temp = round(float(row[17]), 2)
        auxilio_educacao_temp = round(float(row[18]), 2)
        diferenca_entrancia = round(float(row[19]), 2)
        diferenca_salarial = round(float(row[20]), 2)
        estorno_tributo_contribuicao = round(float(row[21]), 2)
        gratificacao = round(float(row[22]), 2)
        turma_recursos = round(float(row[23]), 2)
        gratificacao_aula = round(float(row[24]), 2)
        gratificacao_cumulacao = round(float(row[25]), 2)
        indenizacao_ferias = round(float(row[26]), 2)
        ressarcimento_despesa = round(float(row[27]), 2)
        substituicao_cargo_comissionado = round(float(row[28]), 2)
        substituicao_funcao_gratificada = round(float(row[29]), 2)

        total_outros = round(ajuda_de_custo_temp + auxilio_educacao_temp + diferenca_entrancia + 
        diferenca_salarial + estorno_tributo_contribuicao + gratificacao + turma_recursos + 
        gratificacao_aula + gratificacao_cumulacao + indenizacao_ferias + 
        ressarcimento_despesa + substituicao_cargo_comissionado + substituicao_funcao_gratificada, 2)

        total = total_indenizatorio + total_outros
        
        # Atualização das indenizações
        if nome in employees.keys():
            emp = employees[nome]
            emp['income'].update({
                'total': round(emp['income']['total'] + total, 2)
            })
            emp['income']['perks'].update({
                'total': total_indenizatorio,
                'food': auxilio_alimentacao,
                'pre_school': auxilio_pre_escolar,
                'health': auxilio_saude,
                'housing_aid': auxilio_moradia,
                'subsistence': ajuda_de_custo,
                'vacations': round(ferias + indenizacao_ferias, 2),
                'premium_license_pecuniary': licenca_premio
            })
            emp['income']['other'].update({
                'gratification': gratificacao,
                'others_total': round(emp['income']['other']['others_total'] + total_outros, 2)
            })

            employees[nome] = emp
    print(employees)
    return employees


def select_month(files, month):
    data = []
    month_string = "-" + month + "_"
    for item in files:
        if month_string in item:
            data.append(item)
    return data


# Lê os dados baixados pelo crawler
def read_data(path):
    try:
        data = pd.read_excel(path, engine=None)
    except Exception as excep:
        sys.stderr(
            "Não foi possível fazer a leitura do arquivo: "
            + path
            + ". O seguinte erro foi gerado:"
            + str(excep)
        )
        os._exit(1)
    return data


def save_file(court, month, year, output_path, crawler_version, employees):
    now = datetime.datetime.now()
    # Não será feito backup dos arquivos de origem, dessa forma 'files' não será preenchido
    cr = {
        'aid': court.lower(),
        'month': int(month),
        'year': int(year),
        'files': [],
        'crawler': {
            'id': court.lower(),
            'version': crawler_version,
        },
        'employees': list(employees.values()),
        # https://hackernoon.com/today-i-learned-dealing-with-json-datetime-when-unmarshal-in-golang-4b281444fb67
        'timestamp': now.astimezone().replace(microsecond=0).isoformat(),
    }
   # print(json.dumps({'cr': cr}, ensure_ascii=False))

    final_file_name = court + "-" + str(month) + "-" + str(year) + ".json"
    file_path = "." + output_path + "/" + final_file_name
    with open(file_path, "w") as file:
        file.write(json.dumps({'cr': cr}, ensure_ascii=False))

    return file_path
