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
    data = read_data(file_name[0])
    if "-Membros Ativos" in file_name[0]:  # [0] remover depois
        employees.update(parse_employees(data))
    elif "-Verbas Indenizatórias" in file_name[0]:
        employees.update(update_employees_indemnities(data, employees))

    return employees


def parse_employees(data):
    rows = data.to_numpy()
    employees = {}

    for row in rows[
        3:
    ]:  # Linhas iniciais são cabeçalhos, dados a partir da terceira linha
        row = np.where(row == "-", 0, row)
        nome = row[0]
        if nome != "0":
            cargo_efetivo = row[1]
            if "Cargo: " in cargo_efetivo:
                holder = cargo_efetivo.split("\n")
                cargo_efetivo = holder[0][7:]
            lotacao = row[2]
            remuneracao_cargo_efetivo = float(row[4])
            confianca_comissao = float(
                row[5]
            )  # Função de Confiança ou Cargo em Comissão
            ferias = float(row[6])
            permanencia = float(row[7])  # Abono de Permanência
            indenizatorias = float(row[8])
            outras_verbas_remuneratorias = float(row[9])
            teto_constitucional = abs(
                float(row[11])
            )  # Retenção por Teto Constitucional
            imp_renda = abs(float(row[12]))  # Imposto de Renda
            previdencia = abs(float(row[13]))  # Contribuição Previdenciária
            total_gratificacoes = confianca_comissao + ferias + permanencia
            total_desconto_folha = teto_constitucional + imp_renda + previdencia
            total_folha = (
                remuneracao_cargo_efetivo
                + indenizatorias
                + outras_verbas_remuneratorias
                + total_gratificacoes
            )  # Total da folha
            indenizatorias_suplementar = float(row[15])
            outras_verbas_remuneratorias_suplementar = float(row[16])
            imp_renda_suplementar = abs(float(row[18]))
            previdencia_suplementar = abs(float(row[19]))
            total_indenizacao = indenizatorias + indenizatorias_suplementar
            total_bruto = (
                total_folha
                + indenizatorias_suplementar
                + outras_verbas_remuneratorias_suplementar
            )
            total_desconto = (
                total_desconto_folha + imp_renda_suplementar + previdencia_suplementar
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
                        remuneracao_cargo_efetivo + outras_verbas_remuneratorias, 2
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
                    "total": round(total_desconto, 2),
                    "prev_contribution": previdencia,
                    # Retenção por teto constitucional
                    "ceil_retention": teto_constitucional,
                    "income_tax": round(imp_renda + imp_renda_suplementar, 2),
                },
            }
    print(employees)
    return employees


# Lê os dados baixados pelo crawler
def read_data(path):
    try:
        data = pd.read_excel(path, engine="openpyxl")
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

    # a = {
    #     "reg": "",
    #     "name": "Adalberto Exterkötter",
    #     "role": "Promotor de Justiça",
    #     "type": "membro",
    #     "workplace": "4ª PJ de Rio do Sul",
    #     "active": True,
    #     "income": {
    #         "total": 96007.68,
    #         "wage": 38742.47,
    #         "perks": {"total": 52548.74},
    #         "other": {
    #             "total": 4716.47,
    #             "trust_position": 0.0,
    #             "others_total": 4716.47,
    #             "others": {
    #                 "Férias (1/3 constitucional)": 0.0,
    #                 "Abono de Permanência": 4716.47,
    #             },
    #         },
    #     },
    #     "discounts": {
    #         "total": 14344.87,
    #         "prev_contribution": 4716.47,
    #         "ceil_retention": 0.0,
    #         "income_tax": 9628.4,
    #     },
    # }