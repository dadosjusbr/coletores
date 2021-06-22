import pandas as pd
import sys
import os

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


def get_begin_row(rows, begin_string):
    begin_row = 0
    for row in rows:
        begin_row += 1
        if row[0] == begin_string:
            break

    # We need to continue interate until wee a value that is not
    # whitespace. That happen due to the spreadsheet formatting.

    while isNaN(rows[begin_row][0]):
        begin_row += 1
    return begin_row


def get_end_row(rows, begin_row):
    end_row = 0
    for row in rows:
        # First goes to begin_row.
        if end_row < begin_row:
            end_row += 1
            continue
        # Then keep moving until find a blank row.
        if isNaN(row[0]):
            break
        end_row += 1
    end_row -= 1
    return end_row

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

def update_employee_indemnity(file_name, employees):
    rows = read_data(file_name).to_numpy()

    begin_string = "MATRÍCULA"  # word before starting data
    begin_row = get_begin_row(rows, begin_string)
    end_row = get_end_row(rows, begin_row)
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
            alimentacao = format_value(row[5])
            moradia = format_value(row[6])
            ferias_indenizada = format_value(row[7])
            licenca_premio_indenizada = format_value(row[8])
            aposentadoria_incentivada = format_value(row[9])
            cumulacao = format_value(row[10])
            complemento = format_value(row[11])
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
