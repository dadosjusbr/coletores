import read
import check
import table


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
            cumulacao = table.clean_cell(row[10])
            complemento = table.clean_cell(row[11])
            total_temporario = (
                licenca_premio_indenizada
                + aposentadoria_incentivada
                + cumulacao
                + complemento
            )
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
                    "Programa de Aposentadoria Incentivada": aposentadoria_incentivada,
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
