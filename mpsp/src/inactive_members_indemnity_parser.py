import pandas as pd
import math
import parser

# Worksheets with indemnification funds and temporary remuneration

# For inactive members there are spreadsheets as of August 2020

# Adjust existing spreadsheet variations
def format_value(element):
    if element == None:
        return 0.0
    elif type(element) == str and "-" in element:
        return 0.0
    elif element == "#N/DISP":
        return 0.0
    return element


# August and October 2020
def update_employee_indemnity_aug_oct_2020(file_name, employees):

    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)

    curr_row = 0

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = str(int(row[0]))  # convert to string by removing the '.0'
        ferias_pc = format_value(row[4])

        emp = employees[matricula]
        emp["income"]["perks"].update(
            {
                "total": ferias_pc,
                "vacation_pecuniary": ferias_pc,
            }
        )

        employees[matricula] = emp

        curr_row += 1
        if curr_row >= end_row:
            break

    return employees


# September 2020
def update_employee_indemnity_sept_2020(file_name, employees):

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
        ferias_pc = format_value(row[5])

        emp = employees[matricula]
        emp["income"]["perks"].update(
            {
                "total": alimentacao + ferias_pc,
                "food": alimentacao,
                "vacation_pecuniary": ferias_pc,
            }
        )

        employees[matricula] = emp

        curr_row += 1
        if curr_row >= end_row:
            break

    return employees


# November 2020
def update_employee_indemnity_nov_dec_2020(file_name, employees):

    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)

    curr_row = 0

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = str(int(row[0]))  # convert to string by removing the '.0'
        ferias_pc = format_value(row[4])
        licensa_pc = format_value(row[5])

        emp = employees[matricula]

        emp["income"]["perks"].update(
            {
                "total": round(ferias_pc + licensa_pc, 2),
                "vacation_pecuniary": ferias_pc,
                "premium_license_pecuniary": licensa_pc,
            }
        )

        employees[matricula] = emp

        curr_row += 1
        if curr_row >= end_row:
            break

    return employees
