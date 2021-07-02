import sys
import os
import check
import read
import table

# Used when the employee is not on the indemnity list
def parse_employees(file_name):
    rows = read.xls(file_name).to_numpy()
    emps_clean = table.treat_rows(rows)
    employees = {}
    for row in emps_clean:
        matricula = str(row[0])
        if not check.is_nan(matricula) and matricula != "nan":
            if "Membros" not in str(matricula) and "Matrícula" not in matricula:
                nome = row[1]
                cargo_efetivo = row[2]
                if check.is_nan(cargo_efetivo):
                    cargo_efetivo = "Não informado"
                lotacao = row[3]
                if check.is_nan(lotacao):
                    lotacao = "Não informado"
                remuneracao_cargo_efetivo = table.clean_cell(row[4])
                outras_verbas_remuneratorias = table.clean_cell(row[5])
                confianca_comissao = table.clean_cell(
                    row[6]
                )  # Função de Confiança ou Cargo em Comissão
                grat_natalina = abs(table.clean_cell(row[7]))  # Gratificação Natalina
                ferias = table.clean_cell(row[8])
                permanencia = table.clean_cell(row[9])  # Abono de Permanência
                total_bruto = (
                    remuneracao_cargo_efetivo
                    + outras_verbas_remuneratorias
                    + confianca_comissao
                    + grat_natalina
                    + ferias
                    + permanencia
                )
                previdencia = abs(
                    table.clean_cell(row[11])
                )  # Contribuição Previdenciária
                imp_renda = abs(table.clean_cell(row[12]))  # Imposto de Renda
                teto_constitucional = abs(
                    table.clean_cell(row[13])
                )  # Retenção por Teto Constitucional
                total_desconto = abs(table.clean_cell(row[14]))
                total_gratificacoes = (
                    grat_natalina + ferias + permanencia + confianca_comissao
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
                            "others_total": round(
                                grat_natalina + ferias + permanencia, 2
                            ),
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
    rows = read.xls(file_name).to_numpy()
    emps_clean = table.treat_rows(rows)

    for row in emps_clean:
        matricula = row[0]
        if type(matricula) != str:
            matricula = str(matricula)
        if matricula in employees.keys():
            alimentacao = table.clean_cell(row[2])
            moradia = table.clean_cell(row[3])
            ferias_indenizada = table.clean_cell(row[4])
            licenca_premio_indenizada = table.clean_cell(row[5])
            cumulacao = table.clean_cell(row[6])
            complemento = table.clean_cell(row[7])
            total_temporario = licenca_premio_indenizada + cumulacao + complemento
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
            emp["income"]["other"]["others"].update(
                {
                    "Licença Prêmio Indenizada": licenca_premio_indenizada,
                    "Cumulação": cumulacao,
                    "Complemento por Entrância": complemento,
                }
            )
            emp["income"]["other"].update(
                {
                    "others_total": round(
                        emp["income"]["other"]["others_total"] + total_temporario, 2
                    ),
                    "total": round(
                        emp["income"]["other"]["total"] + total_temporario, 2
                    ),
                }
            )

            employees[matricula] = emp

    return employees
