import sys
import os
import parser_jun_to_aug_2019
import parser_apr_may_2019
import read
import check
import table

# Used when the employee is not on the indemnity list
def parse_employees(file_name):
    rows = read.xls(file_name).to_numpy()
    begin_row = table.begin_row(rows)
    end_row = table.end_row(rows, begin_row)
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
        if check.is_nan(cargo_efetivo):
            cargo_efetivo = "Não informado"
        lotacao = row[5]
        if check.is_nan(lotacao):
            lotacao = "Não informado"
        remuneracao_cargo_efetivo = table.clean_cell(row[6])
        outras_verbas_remuneratorias = table.clean_cell(row[7])
        confianca_comissao = table.clean_cell(
            row[8]
        )  # Função de Confiança ou Cargo em Comissão
        grat_natalina = abs(table.clean_cell(row[9]))  # Gratificação Natalina
        ferias = table.clean_cell(row[10])
        permanencia = table.clean_cell(row[11])  # Abono de Permanência
        outras_remuneracoes_temporarias = abs(table.clean_cell(row[12]))
        total_indenizacao = table.clean_cell(row[13])
        total_bruto = table.clean_cell(row[14])
        previdencia = abs(table.clean_cell(row[16]))  # Contribuição Previdenciária
        imp_renda = abs(table.clean_cell(row[18]))  # Imposto de Renda
        teto_constitucional = abs(
            table.clean_cell(row[20])
        )  # Retenção por Teto Constitucional
        total_desconto = previdencia + teto_constitucional + imp_renda
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
                "perks": {"total": total_indenizacao},
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
    rows = read.xls(file_name).to_numpy()
    begin_row = table.begin_row(rows)
    end_row = table.end_row(rows, begin_row)
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
            alimentacao = table.clean_cell(row[5])
            moradia = table.clean_cell(row[6])
            ferias_indenizada = table.clean_cell(row[7])
            licenca_premio_indenizada = table.clean_cell(row[8])
            aposentadoria_incentivada = table.clean_cell(row[9])
            verbas_rescisorias = table.clean_cell(row[10])
            cumulacao = table.clean_cell(row[11])
            complemento = table.clean_cell(row[12])
            total_temporario = (
                licenca_premio_indenizada
                + aposentadoria_incentivada
                + verbas_rescisorias
                + cumulacao
                + complemento
            )
            emp = employees[matricula]

            emp["income"].update(
                {
                    "perks": {
                        "total": round(alimentacao + moradia + ferias_indenizada, 2),
                        "food": alimentacao,
                        "housing_aid": moradia,
                        "vacation": ferias_indenizada,
                    }
                }
            )
            emp["income"]["other"]["others"].update(
                {
                    "Licença Prêmio Indenizada": licenca_premio_indenizada,
                    "Programa de Aposentadoria Incentivada": aposentadoria_incentivada,
                    "Verbas Rescisórias": verbas_rescisorias,
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

            curr_row += 1
            if curr_row > end_row:
                break

    return employees


def parse(file_names, year, month):
    employees = {}
    if year == "2019" and month.zfill(2) in ["04", "05"]:  # 4 for April and 5 for May
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

    elif year == "2019" and month.zfill(2) in [
        "06",
        "07",
        "08",
    ]:  # 6 for June, 7 for July and 8 for August
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
