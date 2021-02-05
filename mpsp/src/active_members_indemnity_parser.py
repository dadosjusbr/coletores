import pandas as pd
import math
import parser

# Worksheets with indemnification funds and temporary remuneration

# For active members there are spreadsheets as of July 2019 

# Adjust existing spreadsheet variations
def format_value(element):
    if(element == None):
        return 0.0
    if(type(element) == str and '-' in element):
        return 0.0
    if(element == '#N/DISP'):
        return 0.0
    return element



# July and August 2019 
def update_employee_indemnity_jul_aug(file_name, employees):
    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)
 
    curr_row = 0

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = str(int(row[0])) # convert to string by removing the '.0'
        alimentacao = format_value(row[4])
        ferias_pc = format_value(row[5])
        cumulativa = format_value(row[6]) # Gratificação Cumulativa
        grat_natureza = format_value(row[7]) # Gratificação de Natureza Especial

        if(matricula in employees.keys()): # Realiza o update apenas para os servidores que estão na planilha de remuneração mensal

            emp = employees[matricula]
            emp['income'].update({
                'total': round(emp['income']['total'] + cumulativa + grat_natureza, 2)
            })

            emp['income']['perks'].update({
                'total': round(ferias_pc + alimentacao, 2),
                'food': alimentacao,
                'vacation_pecuniary': ferias_pc,
            })

            emp['income']['other'].update({
                'total': round(emp['income']['other']['total'] + cumulativa + grat_natureza, 2),
                'others_total': round(emp['income']['other']['others_total'] + cumulativa + grat_natureza, 2),
            })


            emp['income']['other']['others'].update({
                'GRAT. CUMULATIVA': cumulativa,
                'GRAT. NATUREZA ESPECIAL': grat_natureza,
            })
        
            employees[matricula] = emp

        curr_row += 1
        if curr_row >= end_row:
            break

    return employees

# September to December 2019 / January and November 2020
def update_employee_indemnity_sept_to_jan_nov(file_name, employees):
    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)
 
    curr_row = 0

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = str(int(row[0])) # convert to string by removing the '.0'
        alimentacao = format_value(row[4])
        ferias_pc = format_value(row[5])
        licensa_pc = format_value(row[6])
        cumulativa = format_value(row[7]) # Gratificação Cumulativa
        grat_natureza = format_value(row[8]) # Gratificação de Natureza Especial
        atuacao_especial = format_value(row[9]) #Gratificação de Grupo de Atuação Especial

        if(matricula in employees.keys()): # Realiza o update apenas para os servidores que estão na planilha de remuneração mensal

            emp = employees[matricula]
            emp['income'].update({
                'total': round(emp['income']['total'] + cumulativa + grat_natureza, 2)
            })

            emp['income']['perks'].update({
                'total': round(ferias_pc + alimentacao + licensa_pc, 2),
                'food': alimentacao,
                'vacation_pecuniary': ferias_pc,
                'premium_license_pecuniary': licensa_pc,
            })

            emp['income']['other'].update({
                'total': round(emp['income']['other']['total'] + cumulativa + grat_natureza + atuacao_especial, 2),
                'others_total': round(emp['income']['other']['others_total'] + cumulativa + grat_natureza + atuacao_especial, 2),
            })


            emp['income']['other']['others'].update({
                'GRAT. CUMULATIVA': cumulativa,
                'GRAT. NATUREZA ESPECIAL': grat_natureza,
                'GRAT. DE GRUPO DE ATUAÇÃO ESPECIAL': atuacao_especial
            })
        
            employees[matricula] = emp

        curr_row += 1
        if curr_row >= end_row:
            break

    return employees

# February and March 2020
def update_employee_indemnity_feb_mar(file_name, employees):
    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)
 
    curr_row = 0

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = str(int(row[0])) # convert to string by removing the '.0'
        alimentacao = format_value(row[4])
        licensa_compensatoria = format_value(row[5]) # Licença Compensatória ato 1124/18
        ferias_pc = format_value(row[6])
        licensa_pc = format_value(row[7])
        cumulativa = format_value(row[8]) # Gratificação Cumulativa
        grat_natureza = format_value(row[9]) # Gratificação de Natureza Especial
        atuacao_especial = format_value(row[10]) #Gratificação de Grupo de Atuação Especial

        if(matricula in employees.keys()): # Realiza o update apenas para os servidores que estão na planilha de remuneração mensal

            emp = employees[matricula]
            emp['income'].update({
                'total': round(emp['income']['total'] + cumulativa + grat_natureza + atuacao_especial, 2)
            })

            emp['income']['perks'].update({
                'total': round(ferias_pc + alimentacao + licensa_compensatoria, 2),
                'food': alimentacao,
                'compensatory_leave': licensa_compensatoria,
                'vacation_pecuniary': ferias_pc,
                'premium_license_pecuniary': licensa_pc,
            })

            emp['income']['other'].update({
                'total': round(emp['income']['other']['total'] + cumulativa + grat_natureza + atuacao_especial, 2),
                'others_total': round(emp['income']['other']['others_total'] + cumulativa + grat_natureza + atuacao_especial, 2),
            })


            emp['income']['other']['others'].update({
                'GRAT. CUMULATIVA': cumulativa,
                'GRAT. NATUREZA ESPECIAL': grat_natureza,
                'GRAT. DE GRUPO DE ATUAÇÃO ESPECIAL': atuacao_especial
            })
        
            employees[matricula] = emp

        curr_row += 1
        if curr_row >= end_row:
            break

    return employees

# April to July 2020
def update_employee_indemnity_apr_to_july(file_name, employees):
    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)
    curr_row = 0

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = str(int(row[0])) # convert to string by removing the '.0'
        alimentacao = format_value(row[4])
        licensa_compensatoria = format_value(row[5]) # Licença Compensatória ato 1124/18
        ferias_pc = format_value(row[6])
        cumulativa = format_value(row[7]) # Gratificação Cumulativa
        grat_natureza = format_value(row[8]) # Gratificação de Natureza Especial
        atuacao_especial = format_value(row[9]) #Gratificação de Grupo de Atuação Especial

        if(matricula in employees.keys()): # Realiza o update apenas para os servidores que estão na planilha de remuneração mensal

            emp = employees[matricula]
            emp['income'].update({
                'total': round(emp['income']['total'] + cumulativa + grat_natureza + atuacao_especial, 2)
            })

            emp['income']['perks'].update({
                'total': round(ferias_pc + alimentacao + licensa_compensatoria, 2),
                'food': alimentacao,
                'compensatory_leave': licensa_compensatoria,
                'vacation_pecuniary': ferias_pc,
            })

            emp['income']['other'].update({
                'total': round(emp['income']['other']['total'] + cumulativa + grat_natureza + atuacao_especial, 2),
                'others_total': round(emp['income']['other']['others_total'] + cumulativa + grat_natureza + atuacao_especial, 2),
            })


            emp['income']['other']['others'].update({
                'GRAT. CUMULATIVA': cumulativa,
                'GRAT. NATUREZA ESPECIAL': grat_natureza,
                'GRAT. DE GRUPO DE ATUAÇÃO ESPECIAL': atuacao_especial
            })
        
            employees[matricula] = emp

        curr_row += 1
        if curr_row >= end_row:
            break

    return employees

# August and September 2020
def update_employee_indemnity_aug_sept(file_name, employees):
    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)
 
    curr_row = 0

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = str(int(row[0])) # convert to string by removing the '.0'
        alimentacao = format_value(row[4])
        transporte = format_value(row[5]) # Auxilio Transporte
        creche = format_value(row[6]) # Auxilio Creche
        ferias_pc = format_value(row[7])
        licensa_pc = format_value(row[8]) #Licensa em pecunia
        licensa_compensatoria = format_value(row[9]) # Licença Compensatória ato 1124/18     
        insalubridade = format_value(row[10]) #Adicional de Insalubridade
        subs_funcao  = format_value(row[11]) # Substituição de Função
        viatura = format_value(row[12]) # Viatura 
        cumulativa = format_value(row[13]) # Gratificação Cumulativa
        grat_qualificacao = format_value(row[14])
        grat_natureza = format_value(row[15]) # Gratificação de Natureza Especial
        atuacao_especial = format_value(row[16]) #Gratificação de Grupo de Atuação Especial

        if(matricula in employees.keys()): # Realiza o update apenas para os servidores que estão na planilha de remuneração mensal

            emp = employees[matricula]
            emp['income'].update({
                'total': round(emp['income']['total'] + cumulativa + grat_natureza + atuacao_especial + grat_qualificacao + viatura + insalubridade + subs_funcao, 2)
            })

            emp['income']['perks'].update({
                'total': round(ferias_pc + alimentacao + transporte + creche +licensa_compensatoria + licensa_pc, 2),
                'food': alimentacao,
                'transportation': transporte,
                'pre_school': creche,
                'vacation_pecuniary': ferias_pc,
                'premium_license_pecuniary': licensa_pc,
                'compensatory_leave': licensa_compensatoria,
            })

            emp['income']['other'].update({
                'total': round(emp['income']['other']['total'] + cumulativa + grat_natureza + atuacao_especial + grat_qualificacao + viatura + insalubridade + subs_funcao, 2),
                'others_total': round(emp['income']['other']['others_total'] + cumulativa + grat_natureza + atuacao_especial + grat_qualificacao + viatura + insalubridade + subs_funcao, 2),
            })


            emp['income']['other']['others'].update({
                'INSALUBRIDADE': insalubridade,
                'SUBS. DE FUNÇÃO': subs_funcao,
                'VIATURA': viatura,
                'GRAT. CUMULATIVA': cumulativa,
                'GRAT. DE QUALIFICAÇÃO': grat_qualificacao,
                'GRAT. NATUREZA ESPECIAL': grat_natureza,
                'GRAT. DE GRUPO DE ATUAÇÃO ESPECIAL': atuacao_especial
            })
        
            employees[matricula] = emp
        
        curr_row += 1
        if curr_row >= end_row:
            break

    return employees

# October 2020
def update_employee_indemnity_oct(file_name, employees):
    rows = parser.read_data(file_name).to_numpy()
    begin_row = parser.get_begin_row(rows)
    end_row = parser.get_end_row(rows, begin_row, file_name)
 
    curr_row = 0

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        matricula = str(int(row[0])) # convert to string by removing the '.0'
        ferias_pc = format_value(row[4])
        cumulativa = format_value(row[5]) # Gratificação Cumulativa
        grat_natureza = format_value(row[6]) # Gratificação de Natureza Especial
        atuacao_especial = format_value(row[7]) #Gratificação de Grupo de Atuação Especial

        if(matricula in employees.keys()): # Realiza o update apenas para os servidores que estão na planilha de remuneração mensal

            emp = employees[matricula]
            emp['income'].update({
                'total': round(emp['income']['total'] + cumulativa + grat_natureza + atuacao_especial, 2)
            })

            emp['income']['perks'].update({
                'vacation_pecuniary': ferias_pc,
            })

            emp['income']['other'].update({
                'total': round(emp['income']['other']['total'] + cumulativa + grat_natureza + atuacao_especial,  2),
                'others_total': round(emp['income']['other']['others_total'] + cumulativa + grat_natureza + atuacao_especial, 2),
            })


            emp['income']['other']['others'].update({
                'GRAT. CUMULATIVA': cumulativa,
                'GRAT. NATUREZA ESPECIAL': grat_natureza,
                'GRAT. DE GRUPO DE ATUAÇÃO ESPECIAL': atuacao_especial
            })
        
            employees[matricula] = emp

        curr_row += 1
        if curr_row >= end_row:
            break

    return employees