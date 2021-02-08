import pandas as pd
import math
import parser

# Worksheets with indemnification funds and temporary remuneration

# For active members there are spreadsheets as of August 2020

# Adjust existing spreadsheet variations
def format_value(element):
    if element == None:
        return 0.0
    if type(element) == str and "-" in element:
        return 0.0
    if element == "#N/DISP":
        return 0.0
    return element


# August 2020
def update_employee_indemnity_aug(file_name, employees):

    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)

    curr_row = 0

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = str(int(row[0]))  # convert to string by removing the '.0'
        alimentacao = format_value(row[4])
        transporte = format_value(row[5])  # Auxilio Transporte
        ferias_pc = format_value(row[6])
        insalubridade = format_value(row[7])  # Adicional de Insalubridade
        grat_qualificacao = format_value(row[8])  # Gratificação de Qualificação

        emp = employees[matricula]

        emp["income"].update(
            {
                "total": round(
                    emp["income"]["total"]
                    + alimentacao
                    + transporte
                    + ferias_pc
                    + insalubridade
                    + grat_qualificacao,
                    2,
                )
            }
        )
        emp["income"]["perks"].update(
            {
                "total": alimentacao + transporte,
                "food": alimentacao,
                "transportation": transporte,
                "vacation_pecuniary": ferias_pc,
            }
        )
        emp["income"]["other"].update(
            {
                "total": round(
                    emp["income"]["other"]["total"] + insalubridade + grat_qualificacao,
                    2,
                ),
                "others_total": round(
                    emp["income"]["other"]["others_total"]
                    + insalubridade
                    + grat_qualificacao,
                    2,
                ),
            }
        )

        emp["income"]["other"]["others"].update(
            {
                "INSALUBRIDADE": insalubridade,
                "QUALIFICACAO": grat_qualificacao,
            }
        )

        employees[matricula] = emp

        curr_row += 1
        if curr_row >= end_row:
            break

    return employees


# September to November 2020
def update_employee_indemnity_sept_to_nov(file_name, employees):

    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)

    curr_row = 0

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = str(int(row[0]))  # convert to string by removing the '.0'
        alimentacao = format_value(row[4])
        transporte = format_value(row[5])  # Auxilio Transporte
        insalubridade = format_value(row[6])  # Adicional de Insalubridade
        grat_qualificacao = format_value(row[7])  # Gratificação de Qualificação

        emp = employees[matricula]
        emp["income"].update(
            {
                "total": round(
                    emp["income"]["total"]
                    + alimentacao
                    + transporte
                    + insalubridade
                    + grat_qualificacao,
                    2,
                )
            }
        )
        emp["income"]["perks"].update(
            {
                "total": alimentacao + transporte,
                "food": alimentacao,
                "transportation": transporte,
            }
        )
        emp["income"]["other"].update(
            {
                "total": round(
                    emp["income"]["other"]["total"] + insalubridade + grat_qualificacao,
                    2,
                ),
                "others_total": round(
                    emp["income"]["other"]["others_total"]
                    + insalubridade
                    + grat_qualificacao,
                    2,
                ),
            }
        )

        emp["income"]["other"]["others"].update(
            {
                "INSALUBRIDADE": insalubridade,
                "QUALIFICACAO": grat_qualificacao,
            }
        )

        employees[matricula] = emp

        curr_row += 1
        if curr_row >= end_row:
            break

    return employees

# December
def update_employee_indemnity_dec(file_name, employees):

    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)

    curr_row = 0

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = str(int(row[0]))  # convert to string by removing the '.0'
        alimentacao = format_value(row[4])
        transporte = format_value(row[5])  # Auxilio Transporte
        ferias_pc = format_value(row[6]) # Férias em pecunia
        licensa_pc = format_value(row[7]) # Licença Prêmio em Pecúnia
        insalubridade = format_value(row[8])  # Adicional de Insalubridade

        emp = employees[matricula]
       
        emp["income"]["perks"].update(
            {
                "total": alimentacao + transporte,
                "food": alimentacao,
                "transportation": transporte,
                "vacation_pecuniary": ferias_pc,
                "premium_license_pecuniary": licensa_pc
            }
        )
        emp["income"]["other"].update(
            {
                "total": round(
                    emp["income"]["other"]["total"] + insalubridade,
                    2,
                ),
                "others_total": round(
                    emp["income"]["other"]["others_total"]
                    + insalubridade,
                    2,
                ),
            }
        )

        emp["income"]["other"]["others"].update(
            {
                "INSALUBRIDADE": insalubridade,
            }
        )

        employees[matricula] = emp

        curr_row += 1
        if curr_row >= end_row:
            break

    return employees
