import read
import utils
import clean
import table

def update_employee_indemnity(file_name, employees):
    rows = read.data(file_name).to_numpy()
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
            alimentacao = clean.cell(row[5])
            moradia = clean.cell(row[6])
            ferias_indenizada = clean.cell(row[7])
            licenca_premio_indenizada = clean.cell(row[8])
            aposentadoria_incentivada = clean.cell(row[9])
            cumulacao = clean.cell(row[10])
            complemento = clean.cell(row[11])
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
                    "Programa de Aposentadoria Incentivada": aposentadoria_incentivada,
                    "Cumulação": cumulacao,
                    "Complemento por Entrância": complemento
                }
            )

            employees[matricula] = emp

            curr_row += 1
            if curr_row > end_row:
                break

    return employees
