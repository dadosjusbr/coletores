import pandas as pd
from pandas_ods_reader import read_ods
from openpyxl import load_workbook
import math
import sys
import os
import active_members_parser
import inactive_members_parser
import active_servants_parser
import inactive_servants_parser
import inactive_members_indemnity_parser
import active_members_indemnity_parser
import active_servants_indemnity_parser
import inactive_servants_indemnity_parser


def read_data(path):
    if "ods" in path:
        try:
            # load a sheet based on its index (1 based)
            data = read_ods(path, 1)
        except Exception as excep:
            sys.stderr(
                "Não foi possível fazer a leitura do arquivo: "
                + path
                + "e o seguinte error foi gerado:"
                + str(excep)
            )
            os._exit(1)
    else:
        try:
            data = pd.read_excel(path, engine="openpyxl")
        except Exception as excep:
            sys.stderr(
                "Não foi possível fazer a leitura do arquivo: "
                + path
                + "e o seguinte error foi gerado:"
                + str(excep)
            )
            os._exit(1)
    return data


# Strange way to check nan. Only I managed to make work
# Source: https://stackoverflow.com/a/944712/5822594
def is_nan(string):
    return string != string


def get_begin_row(rows):
    begin_row = 0

    # We need to continue interate until wee a value that is not
    # None or NaN. That happen due to the spreadsheet formatting.
    while rows[begin_row][0] == None or is_nan(rows[begin_row][0]):
        begin_row += 1

    return begin_row


def get_end_row(rows, begin_row, file_name):
    end_row = begin_row
    array_len = len(rows)

    # There are variations at the end of the worksheets. Different conditions are needed
    if "Pensionistas" in file_name:
        end_row = array_len
    elif type(rows[array_len - 1][0]) == float:
        end_row = array_len
    else:
        # Then keep moving until find a different type of float.
        while type(rows[end_row][0]) == float:
            end_row += 1

    end_row -= 1
    return end_row


def type_employee(fn):
    if "Membros" in fn:
        return "membro"
    if "Servidores" in fn:
        return "servidor"
    if "Pensionistas" in fn:
        return "pensionista"
    if "Colaboradores" in fn:
        return "colaborador"
    raise ValueError("Tipo de inválido de funcionário público: " + fn)


# Adjust existing spreadsheet variations
def format_value(element):
    if element == None:
        return 0.0
    elif type(element) == str:
        if "-" in element:
            return 0.0
        elif "," in element:
            # A value was found with incorrect formatting. (3,045.99 instead of 3045.99)
            element = element.replace(".", "").replace(",", ".").replace(" ", "")
            return float(element)
        elif element == "#N/DISP":
            return 0.0
    elif type(element) == float:
        return element

    return element


# Parser for the months from July 2019 to November 2020
def parse_employees(file_name):
    rows = read_data(file_name).to_numpy()
    begin_row = get_begin_row(rows)
    end_row = get_end_row(rows, begin_row, file_name)

    typeE = type_employee(file_name)
    activeE = "inativos" not in file_name
    employees = {}
    curr_row = 0
    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = str(
            int(row[0])
        )  # The value is returned in float, to remove the '.0' this conversion is necessary
        name = row[1].strip()  # removes blank spaces present in some cells
        role = row[2]  # cargo
        workplace = row[3]  # Lotação
        remuneracao_cargo_efetivo = format_value(row[4])  # Remuneração Cargo Efetivo
        outras_verbas_remuneratorias = format_value(
            row[5]
        )  # Outras Verbas Remuneratórias, Legais ou Judiciais
        total_verbas_indenizatorias = format_value(row[11])  # VERBAS INDENIZATÓRIAS8
        trust_position = format_value(
            row[6]
        )  # Função de Confiança ou Cargo em Comissão³
        gratificacao_natalina = format_value(row[7])
        ferias = format_value(row[8])  # (1/3 constitucional)
        abono_permanencia = format_value(row[9])  # Abono de Permanência6
        total_discounts = abs(format_value(row[16]))  # TOTAL DE DESCONTOS
        prev_contribution = abs(format_value(row[13]))  # Contribuição Previdenciária
        ceil_retention = abs(format_value(row[15]))  # Retenção por teto constitucional
        income_tax = format_value(row[14])  # Imposto de Renda
        total_gratificacoes = (
            trust_position + gratificacao_natalina + ferias + abono_permanencia
        )
        total_bruto = (
            remuneracao_cargo_efetivo
            + outras_verbas_remuneratorias
            + total_verbas_indenizatorias
            + total_gratificacoes
        )

        employees[matricula] = {
            "reg": matricula,
            "name": name,
            "role": role,
            "type": typeE,
            "workplace": workplace,
            "active": activeE,
            "income": {
                "total": round(total_bruto, 2),
                "wage": round(
                    remuneracao_cargo_efetivo + outras_verbas_remuneratorias, 2
                ),
                "perks": {
                    "total": total_verbas_indenizatorias,
                },
                "other": {  # Gratificações
                    "total": round(total_gratificacoes, 2),
                    "trust_position": trust_position,
                    "others_total": gratificacao_natalina + ferias + abono_permanencia,
                    "others": {
                        "Gratificação Natalina": gratificacao_natalina,
                        "Férias (1/3 constitucional)": ferias,
                        "Abono de Permanência": abono_permanencia,
                    },
                },
            },
            "discounts": {  # Discounts Object. Using abs to garantee numbers are positivo (spreadsheet have negative discounts).
                "total": abs(total_discounts),
                "prev_contribution": abs(prev_contribution),
                "ceil_retention": abs(ceil_retention),
                "income_tax": abs(income_tax),
            },
        }

        curr_row += 1
        if curr_row >= end_row:
            break

    # print(employees)
    return employees


def parse(file_names, month, year):
    employees = {}
    for fn in file_names:
        if "Membros_ativos" in fn:
            if "Verbas Indenizatorias" not in fn:
                if year == "2020":
                    employees.update(parse_employees(fn))
                elif month in ["07", "08", "09", "10", "11", "12"] and year == "2019":
                    employees.update(parse_employees(fn))
                elif month == "01" and year == "2019":
                    employees.update(active_members_parser.parse_jan_19(fn))
                elif month in ["02", "03", "04", "05"] and year == "2019":
                    employees.update(active_members_parser.parse_feb_to_may_19(fn))
                elif month == "06" and year == "2019":
                    employees.update(active_members_parser.parse_jun_19(fn))

            elif "Verbas Indenizatorias" in fn:
                if year == "2019":
                    if month in ["07", "08"]:
                        employees.update(
                            active_members_indemnity_parser.update_employee_indemnity_jul_aug_2019(
                                fn, employees
                            )
                        )
                    elif month in ["09", "10", "11", "12"]:
                        employees.update(
                            active_members_indemnity_parser.update_employee_indemnity_sept_2019_to_jan_and_nov_2020(
                                fn, employees
                            )
                        )
                elif year == "2020":
                    if month == "01":
                        employees.update(
                            active_members_indemnity_parser.update_employee_indemnity_sept_2019_to_jan_and_nov_2020(
                                fn, employees
                            )
                        )
                    elif month in ["02", "03"]:
                        employees.update(
                            active_members_indemnity_parser.update_employee_indemnity_feb_mar_2020(
                                fn, employees
                            )
                        )
                    elif month in ["04", "05", "06", "07"]:
                        employees.update(
                            active_members_indemnity_parser.update_employee_indemnity_apr_to_july_2020(
                                fn, employees
                            )
                        )
                    elif month in ["08", "09"]:
                        employees.update(
                            active_members_indemnity_parser.update_employee_indemnity_aug_sept_2020(
                                fn, employees
                            )
                        )
                    elif month == "10":
                        employees.update(
                            active_members_indemnity_parser.update_employee_indemnity_oct_2020(
                                fn, employees
                            )
                        )
                    elif month == "11":
                        employees.update(
                            active_members_indemnity_parser.update_employee_indemnity_sept_2019_to_jan_and_nov_2020(
                                fn, employees
                            )
                        )
                    elif month == "12":
                        employees.update(
                            active_members_indemnity_parser.update_employee_indemnity_dec_2020(
                                fn, employees
                            )
                        )

        elif "Membros_inativos" in fn:
            if "Verbas Indenizatorias" not in fn:
                if year == "2020":
                    employees.update(parse_employees(fn))
                elif month in ["01", "02", "03", "04", "08"] and year == "2019":
                    employees.update(
                        inactive_members_parser.parse_jan_to_april_aug_19(fn)
                    )
                elif month == "05" and year == "2019":
                    employees.update(inactive_members_parser.parse_may_19(fn))
                elif month == "06" and year == "2019":
                    employees.update(inactive_members_parser.parse_june_19(fn))
                elif month in ["07", "08", "09", "10", "11", "12"] and year == "2019":
                    employees.update(parse_employees(fn))

            elif "Verbas Indenizatorias" in fn:
                if year == "2020":
                    if month in ["08", "10"]:
                        employees.update(
                            inactive_members_indemnity_parser.update_employee_indemnity_aug_oct_2020(
                                fn, employees
                            )
                        )
                    elif month == "09":
                        employees.update(
                            inactive_members_indemnity_parser.update_employee_indemnity_sept_2020(
                                fn, employees
                            )
                        )
                    elif month in ["11", "12"]:
                        employees.update(
                            inactive_members_indemnity_parser.update_employee_indemnity_nov_dec_2020(
                                fn, employees
                            )
                        )

        elif "Servidores_ativos" in fn:
            if "Verbas Indenizatorias" not in fn:
                if year == "2020":
                    employees.update(parse_employees(fn))
                elif month in ["01", "02", "03", "04", "05", "06"] and year == "2019":
                    employees.update(active_servants_parser.parse_jan_to_june_19(fn))
                elif month in ["07", "08", "10", "11", "12"] and year == "2019":
                    employees.update(parse_employees(fn))
            elif "Verbas Indenizatorias" in fn:
                if month in ["07", "08"] and year == "2019":
                    employees.update(
                        active_servants_indemnity_parser.update_employee_indemnity_jul_aug_2019(
                            fn, employees
                        )
                    )
                elif month == "10" and year == "2019":
                    employees.update(
                        active_servants_indemnity_parser.update_employee_indemnity_sept_oct_2019_feb_2020(
                            fn, employees
                        )
                    )
                elif month in ["11", "12"] and year == "2019":
                    employees.update(
                        active_servants_indemnity_parser.update_employee_indemnity_nov_2019_to_jan_2020(
                            fn, employees
                        )
                    )
                elif month == "02" and year == "2020":
                    employees.update(
                        active_servants_indemnity_parser.update_employee_indemnity_sept_oct_2019_feb_2020(fn, employees
                        )
                    )
                elif month == "01" and year == "2020":
                    employees.update(
                        active_servants_indemnity_parser.update_employee_indemnity_nov_2019_to_jan_2020(
                            fn, employees
                        )
                    )
                elif month == "03" and year == "2020":
                    employees.update(
                        active_servants_indemnity_parser.update_employee_indemnity_mar_2020(
                            fn, employees
                        )
                    )
                elif month in ["04", "05", "06", "07"] and year == "2020":
                    employees.update(
                        active_servants_indemnity_parser.update_employee_indemnity_apr_to_jul_2020(
                            fn, employees
                        )
                    )
                elif month in ["08", "11"] and year == "2020":
                    employees.update(
                        active_servants_indemnity_parser.update_employee_indemnity_aug_nov_2020(
                            fn, employees
                        )
                    )
                elif month == "10" and year == "2020":
                    employees.update(
                        active_servants_indemnity_parser.update_employee_indemnity_oct_2020(
                            fn, employees
                        )
                    )
                elif month == "12" and year == "2020":
                    employees.update(
                        active_servants_indemnity_parser.update_employee_indemnity_dec_2020(
                            fn, employees
                        )
                    )

        elif "Servidores_inativos" in fn:
            if "Verbas Indenizatorias" not in fn:
                if year == "2020":
                    employees.update(parse_employees(fn))
                elif month in ["01", "02", "03", "04"] and year == "2019":
                    employees.update(inactive_servants_parser.parse_jan_to_april_19(fn))
                elif month == "05" and year == "2019":
                    employees.update(inactive_servants_parser.parse_may_19(fn))
                elif month == "06" and year == "2019":
                    employees.update(inactive_servants_parser.parse_june_19(fn))
                elif month in ["07", "08", "09", "10", "11", "12"] and year == "2019":
                    employees.update(parse_employees(fn))
            elif "Verbas Indenizatorias" in fn:
                if year == "2020":
                    if month in ["09", "10", "11"]:
                        employees.update(
                            inactive_servants_indemnity_parser.update_employee_indemnity_sept_to_nov_2020(
                                fn, employees
                            )
                        )
                    elif month == "08":
                        employees.update(
                            inactive_servants_indemnity_parser.update_employee_indemnity_aug_2020(
                                fn, employees
                            )
                        )
                    elif month == "12":
                        employees.update(
                            inactive_servants_indemnity_parser.update_employee_indemnity_dec_2020(
                                fn, employees
                            )
                        )

    return list(employees.values())
