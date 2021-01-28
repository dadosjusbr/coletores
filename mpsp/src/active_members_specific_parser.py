import pandas as pd
import math
import parser

# Due to the different format of the spreadsheets, a specific parser is required for a few months
# This class contains the parsers for active members:
    # parse_active_members_1: January 2019
    # parse_active_members_2: February to May 2019
    # parse_active_members_3: June 2019

# Adjust existing spreadsheet variations
def format_value(element):
    if(element == None):
        return 0.0
    if(type(element) == str and '-' in element):
        return 0.0
    return element

# Parser for Active Members - January 2019
def parse_active_members_1(file_name):
    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)

    typeE = parser.type_employee(file_name)
    activeE = 'inativos' not in file_name 
    employees = {}
    curr_row = 0
    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue
    
        employees[str(int(row[0]))] = {
            'reg': str(int(row[0])),
            'name': row[1],
            'role': row[2],
            'type': typeE,
            'workplace': row[3],
        
            'active': activeE,
            "income":
            {
                'total': row[10],
                # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                'wage': format_value(row[4]) + format_value(row[5]),
                'perks': {
                    'total': format_value(row[18]) + format_value(row[16]) + format_value(row[17]),
                    'food': row[16],
                    'housing_aid': row[17],
                },
                'other':
                {  # Gratificações
                    'total': format_value(row[6]) + format_value(row[7]) + format_value(row[8])+ format_value(row[9]) + format_value(row[18]),
                    'trust_position': row[6],
                    'others_total': format_value(row[7]) + format_value(row[8]) + format_value(row[9]) + format_value(row[18]), 
                    'others': {
                        'Gratificação Natalina': row[7],
                        'Férias (1/3 constitucional)': row[8],
                        'Abono de Permanência': row[9],
                        'Outras remunerações temporárias': row[18]
                    }
                },
            },
            'discounts':
            {  # Discounts Object. Using abs to garantee numbers are positivo (spreadsheet have negative discounts).
                'total': abs(format_value(row[14])),
                'prev_contribution': abs(format_value(row[11])),
                # Retenção por teto constitucional
                'ceil_retention': abs(format_value(row[13])),
                'income_tax':abs(format_value(row[12])),
            }
        }

        curr_row += 1
        if curr_row >= end_row:
            break
    
    return employees

# Parser for Active Members - February to May 2019
def parse_active_members_2(file_name):
    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)

    typeE = parser.type_employee(file_name)
    activeE = 'inativos' not in file_name 
    employees = {}
    curr_row = 0
    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue
    
        employees[str(int(row[0]))] = {
            'reg': str(int(row[0])),
            'name': row[1],
            'role': row[2],
            'type': typeE,
            'workplace': row[3],
        
            'active': activeE,
            "income":
            {
                'total': row[10],
                # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                'wage': format_value(row[4]) + format_value(row[5]),
                'perks': {
                    'total': format_value(row[16]) + format_value(row[17]),
                    'food': row[16],
                    'ferias em pecunia': row[17],
                },  
                'other':
                {  # Gratificações
                    'total': format_value(row[6]) + format_value(row[7]) + format_value(row[8])+ format_value(row[9]) + format_value(row[18]),
                    'trust_position': row[6],
                    'others_total': format_value(row[7]) + format_value(row[8]) + format_value(row[9]) + format_value(row[18]),
                    'others': {
                        'Gratificação Natalina': row[7],
                        'Férias (1/3 constitucional)': row[8],
                        'Abono de Permanência': row[9],
                        'Outras remunerações temporárias': row[18],
                    }
                },
            },
            'discounts':
            {  # Discounts Object. Using abs to garantee numbers are positivo (spreadsheet have negative discounts).
                'total': abs(format_value(row[14])),
                'prev_contribution': abs(format_value(row[11])),
                # Retenção por teto constitucional
                'ceil_retention': abs(format_value(row[13])),
                'income_tax':abs(format_value(row[12])),
            }
        }

        curr_row += 1
        if curr_row >= end_row:
            break
    
    return employees

# Parser for Active Members - June 2019
def parse_active_members_3(file_name):
    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)

    typeE = parser.type_employee(file_name)
    activeE = 'inativos' not in file_name 
    employees = {}
    curr_row = 0
    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue
    
        employees[str(int(row[0]))] = {
            'reg': str(int(row[0])),
            'name': row[1],
            'role': row[2],
            'type': typeE,
            'workplace': row[3],
        
            'active': activeE,
            "income":
            {
                'total': row[10],
                # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                'wage': format_value(row[4]) + format_value(row[5]),
                'perks': {
                    'total': format_value(row[15]) + format_value(row[16]) + format_value(row[17]),
                    'food': row[15],
                    'ferias em pecunia': row[16],
                    'LP em pecunia': row[17],
                },
                'other':
                {  # Gratificações
                    'total': format_value(row[6]) + format_value(row[7]) + format_value(row[8])+ format_value(row[9]) + + format_value(row[18]),
                    'trust_position': row[6],
                    'others_total': format_value(row[7]) + format_value(row[8]) + format_value(row[9]) + format_value(row[18]),
                    'others': {
                        'Gratificação Natalina': row[7],
                        'Férias (1/3 constitucional)': row[8],
                        'Abono de Permanência': row[9],
                        'Outras remunerações temporarias': row[18], 

                    }
                },
            },
            'discounts':
            {  # Discounts Object. Using abs to garantee numbers are positivo (spreadsheet have negative discounts).
                'total': abs(format_value(row[13])),
                'prev_contribution': abs(format_value(row[11])),
                'income_tax':abs(format_value(row[12])),
            }
        }

        curr_row += 1
        if curr_row >= end_row:
            break
    
    return employees
