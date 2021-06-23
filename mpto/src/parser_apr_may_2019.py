import pandas as pd
from datetime import datetime
import math
import pathlib
import sys
import os
import utils

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
    emps_clean = utils.treat_rows(rows)
    employees = {}
    for row in emps_clean:
        matricula = str(row[0])
        if not isNaN(matricula) and matricula != "nan":
            if "Membros" not in str(matricula) and "Matrícula" not in matricula:
                nome = row[1]
                cargo_efetivo = row[2]
                if isNaN(cargo_efetivo):
                    cargo_efetivo = "Não informado"
                lotacao = row[3]
                if isNaN(lotacao):
                    lotacao = "Não informado"
                remuneracao_cargo_efetivo = format_value(row[4])
                outras_verbas_remuneratorias = format_value(row[5])
                confianca_comissao = format_value(row[6])  # Função de Confiança ou Cargo em Comissão
                grat_natalina = abs(format_value(row[7]))  # Gratificação Natalina
                ferias = format_value(row[8])
                permanencia = format_value(row[9])  # Abono de Permanência
                total_bruto = format_value(row[10])
                previdencia = abs(format_value(row[11]))  # Contribuição Previdenciária
                imp_renda = abs(format_value(row[12]))  # Imposto de Renda
                teto_constitucional = abs(format_value(row[13]))  # Retenção por Teto Constitucional
                total_desconto = abs(format_value(row[14]))
                total_gratificacoes = (
                    grat_natalina
                    + ferias
                    + permanencia
                    + confianca_comissao
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
                    "discounts": {  # Discounts Object. Using abs to garantee numbers are positive (spreadsheet have negative discounts).
                        "total": round(total_desconto, 2),
                        "prev_contribution": previdencia,
                        # Retenção por teto constitucional
                        "ceil_retention": teto_constitucional,
                        "income_tax": imp_renda,
                    },
                }

    return employees

def update_employee_indemnity(file_name, employees):
    rows = read_data(file_name).to_numpy()
    emps_clean = utils.treat_rows(rows)

    for row in emps_clean:
        matricula = row[0]
        if type(matricula) != str:
            matricula = str(matricula)
        if matricula in employees.keys():
            alimentacao = format_value(row[2])
            moradia = format_value(row[3])
            ferias_indenizada = format_value(row[4])
            licenca_premio_indenizada = format_value(row[5])
            cumulacao = format_value(row[6])
            complemento = format_value(row[7])
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
                    "Cumulação": cumulacao,
                    "Complemento por Entrância": complemento
                }
            )

            employees[matricula] = emp

    return employees