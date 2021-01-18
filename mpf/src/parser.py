import pandas as pd
from datetime import datetime
import pyexcel_ods
import pyexcel_xls
import math
import sys
import os
nan = float('nan')

# Retorna a posição de um elemento de chave K em uma planilha.
def get_pos(key, sheet, row):
    if(key == 'Remuneração do     Cargo Efetivo (1)'):
        for i in range(len(sheet[row])):
            aux = str(sheet[row][i]).strip()
            if((aux == key) or( aux == 'Remuneração do Cargo Efetivo (1)')):
                return i
    elif(key =='Outras Verbas Remuneratórias Legais ou Judiciais (2)'):
        for i in range(len(sheet[row])):
            aux = str(sheet[row][i]).strip()
            if((aux == key) or( aux == 'Outras Verbas')):
                return i
    elif(key =='Gratificação Natalina (4)'):
        for i in range(len(sheet[row])):
            aux = str(sheet[row][i]).strip()
            if((aux == key) or( aux == 'Gratificação Natalina(4)')):
                return i
    elif(key == 'Férias (1/3 Constitucional) (5)'):
        for i in range(len(sheet[row])):
            aux = str(sheet[row][i]).strip()
            if((aux == key) or( aux == 'Férias (1/3 constitucional) (5)')):
                return i
    elif(key == 'Outras Remunerações Temporárias (7)'):
        for i in range(len(sheet[row])):
            aux = str(sheet[row][i]).strip()
            if((aux == key)):
                return i
        new_row = row -1 
        for i in range(len(sheet[new_row])):
            aux = str(sheet[new_row][i]).strip()
            if((aux == 'Outras Remunerações Retroativas/Temporárias (14)')):
                return i
    elif(key == 'Verbas Indenizatórias (8)'):
        for i in range(len(sheet[row])):
            aux = str(sheet[row][i]).strip()
            if((aux == key)):
                return i
        new_row = row -1 
        for i in range(len(sheet[new_row])):
            aux = str(sheet[new_row][i]).strip()
            if((aux == 'Indenizações (13)')):
                return i
    elif(key == 'Total de Rendimentos Brutos (9)'):
        for i in range(len(sheet[row])):
            aux = str(sheet[row][i]).strip()
            if((aux == key) or (aux == 'Total de Rendimentos Brutos (7)')):
                return i
    elif(key == 'Contribuição Previdenciária (10)'):
        for i in range(len(sheet[row])):
            aux = str(sheet[row][i]).strip()
            if((aux == key) or (aux == 'Contribuição Previdenciária (8)')):
                return i
    elif(key == 'Imposto de Renda (11)'):
        for i in range(len(sheet[row])):
            aux = str(sheet[row][i]).strip()
            if((aux == key) or (aux == 'Imposto de Renda (9)')):
                return i
    elif(key == 'Retenção por Teto Constitucional (12)'):
        for i in range(len(sheet[row])):
            aux = str(sheet[row][i]).strip()
            if((aux == key) or (aux == 'Retenção por Teto Constitucional (10)')):
                return i
    elif(key == 'Total de Descontos (13)'):
        for i in range(len(sheet[row])):
            aux = str(sheet[row][i]).strip()
            if((aux == key) or (aux == 'Total de Descontos (11)')):
                return i
    elif(key == 'Outras Verbas Remuneratórias Retroativas/Temporárias'):
        #print(sheet[row])
        for i in range(len(sheet[row])):
            aux = str(sheet[row][i]).strip()
            if((aux == key) or (aux == 'Outras Verbas Remuneratórias Retroativas/  Temporárias')or (aux =='Outras Verbas Remuneratórias Retroativas / Temporárias')):
                return i
    elif(key == 'Total de Verbas Temporárias'):
        alternative = True
        for i in range(len(sheet[row])):
            aux = str(sheet[row][i]).strip()
            if((aux == key)):
                alernative = False
        
        if(alternative):
            new_row = row - 1
            for i in range(len(sheet[new_row])):
                aux = str(sheet[new_row][i]).strip()
                if(aux == key):
                    return sheet[new_row].index(key)
        else:
            return sheet[row].index(key)

    elif(key == 'Rendimento Líquido Total * (14)'):
        alternative = True
        for i in range(len(sheet[row])):
            aux = str(sheet[row][i]).strip()
            if(key == aux):
                alternative = False
        
        if(alternative):
            alternative_key = 'Rendimento Líquido Total (12)'
            for i in range(len(sheet[row])):
                aux = str(sheet[row][i]).strip()
                if(alternative_key == aux):
                    return sheet[row].index(alternative_key)
        else:
            return sheet[row].index(key)
    elif((key == 'Matrícula')): 
        alternative = True
        for i in range(len(sheet[row])):
            aux = str(sheet[row][i]).strip()
            if(key == aux):
                alternative = False
        
        if(alternative):
            alternative_key = 'Nome ou Matrícula'
            for i in range(len(sheet[row])):
                aux = str(sheet[row][i]).strip()
                if(alternative_key == aux):
                    return sheet[row].index(alternative_key)
        else:
            return sheet[row].index(key)
    elif(key == 'Nome'):
        alternative = True
        for i in range(len(sheet[row])):
            aux = str(sheet[row][i]).strip()
            if(key == aux):
                alternative = False
        
        if(alternative):
            alternative_key = 'Nome ou Matrícula'
            for i in range(len(sheet[row])):
                aux = str(sheet[row][i]).strip()
                if(alternative_key == aux):
                    return sheet[row].index(alternative_key)
        else:
            return sheet[row].index(key)
  
    return sheet[row].index(key)

#Definindo primeira Linha iterável da planilha 
def get_begin_row(data, begin_string):
    line = 0 
    for row in data:
        if(len(row)!= 0):
            if(begin_string in row):
                return line
            else:
                line += 1
        else:
            line +=1
    
    #Buscando Begin_row Alternativo
    alt_line = 0
    begin_string = 'Nome ou Matrícula'
    for row in data:
        if(len(row)!= 0):
            if(begin_string in row):
                return alt_line
            else:
                alt_line += 1
        else:
            alt_line += 1
    
#Definindo ultima Linha Iterável da Planilha
def get_end_row(data,end_string):
    line = 0
    for row in data:
        if(len(row)!= 0):
            if(end_string in row):
                return line
            else:
                line += 1
        else:
            line += 1
     
#Define estratégia de leitura baseada na extensão do arquivo.
def read_data(path, extension):
    if('ods' in extension):
        try:
            data = pyexcel_ods.get_data(path)
        except Exception as excep:
            sys.stderr('Não foi possível fazer a leitura do arquivo: ' + path +'e o seguinte error foi gerado:' + str(excep))
            os._exit(1)
    else:
        try:
            data = pyexcel_xls.get_data(path)
        except Exception as excep:
            sys.stderr('Não foi possível fazer a leitura do arquivo: ' + path +'e o seguinte error foi gerado:' + str(excep))
            os._exit(1)

    return data

#Definindo primeira Linha iterável da planilha para planilhas sem Indenizações
def get_begin_row_notIn(data, rows, begin_string):
    for row in rows:
        if(data.iloc[row][0] == begin_string):
            new_begin = int(row)
    
#Parser,  convertendo os objetos para o formato exigido para empregados sem dados indenizatórios
def employees(file_name, outputPath, year, month, file_type):

    #Definindo main Data
    extension = file_name.split('.')
    path = './/' + outputPath +'//' + file_name

    data = read_data(path, extension)
    rows = list(data.index.values)

    #Definindo linhas Iteráveis da planilha Principal
    begin_string  = "Nome ou Matrícula" 
    begin_row = get_begin_row(data, rows, begin_string)

    end_string = "TOTAL GERAL"
    end_row = get_end_row(data, rows, end_string)

    return all_employees_novi(data, begin_row, end_row, file_type)

#Para empregados sem dados de verbas indenizatórias 
def all_employees_novi(data, begin_row, end_row, file_type):
    employees = []
    for i in range(begin_row, end_row):
        employee = {
            'reg' : data.iloc[i][0], 
            'name': data.iloc[i][0], 
            'role': data.iloc[i][3], 
            'type': file_type,   
            'workplace': data.iloc[i][13], 
            'active': True if ('Ativos' in file_type) else False, 
            "income": 
            #Income Details
            {'total' : format_string(data.iloc[i][25]),  # ? Total Liquido ??
             'wage'  : format_string(data.iloc[i][14]), 
             'perks' : 
            #Perks Object 
            { 'total' : format_string(data.iloc[i][27]), 
               'vacation_pecuniary':format_string(data.iloc[i][18]), #Férias
            }, 
            'other': 
            { #Funds Object 
              'total': format_string(data.iloc[i][26]), 
              'trust_position' : format_string(data.iloc[i][16]),  #Pericia e projeto
              'gratification': format_string(data.iloc[i][17]),  #Só existem dados da gratificação natalina
              'others': format_string(data.iloc[i][15]) + format_string(data.iloc[i][19]),  #Não encontrado
            } , 
            } , 
            'discounts':
            { #Discounts Object
              'total' : format_string(data.iloc[i][24]) * -1 if(format_string(data.iloc[i][24]) < 0) else format_string(data.iloc[i][24]), 
              'prev_contribution': format_string(data.iloc[i][21]) * -1 if(format_string(data.iloc[i][21]) < 0) else format_string(data.iloc[i][21]), 
              'ceil_retention': format_string(data.iloc[i][23]) * -1 if(format_string(data.iloc[i][24]) < 0) else format_string(data.iloc[i][23]), 
              'income_tax': format_string(data.iloc[i][22]) * - 1 if(format_string(data.iloc[i][22]) < 0) else format_string(data.iloc[i][22]), 
            }
        }
        employees.append(employee)

    return (employees)

#Para empregados no formato de mês com indenização mas sem match
def all_employees(data, begin_row, end_row, data_pos_dict, file_type):

    employees = []
    for i in range(begin_row, end_row):
        employee = {
            'reg' : data[i][data_pos_dict['Matrícula']], 
            'name': data[i][data_pos_dict['Nome']], 
            'role': data[i][data_pos_dict['Cargo']], 
            'type': file_type, 
            'workplace': data[i][data_pos_dict['Lotação']], 
            'active': True if ('Ativos' in file_type) else False, 
            "income": 
            #Income Details
            {'total' : format_string(data[i][data_pos_dict['Rendimento Líquido Total * (14)']]),  # ? Total Liquido ??
             'wage'  : format_string(data[i][data_pos_dict['Remuneração do Cargo Efetivo (1)']]), 
             'perks' : 
            #Perks Object 
            { 'total' : format_string(data[i][data_pos_dict['Verbas Indenizatórias (8)']]), 
               'compensatory_leave':format_string(data[i][data_pos_dict['Abono de Permanência (6)']]),  
               'vacation_pecuniary':format_string(data[i][data_pos_dict['Férias (1/3 Constitucional) (5)']]), #Férias
            }, 
            'other': 
            { #Funds Object 
              'total': format_string(data[i][data_pos_dict['Outras Remunerações Temporárias (7)']]), 
              'trust_position' : format_string(data[i][data_pos_dict['Função de Confiança ou Cargo em Comissão (3)']]),  #Pericia e projeto
              'gratification': format_string(data[i][data_pos_dict['Gratificação Natalina (4)']]),  #Só existem dados da gratificação natalina
              'others': format_string(data[i][data_pos_dict['Outras Verbas Remuneratórias Legais ou Judiciais (2)']]),  #Não encontrado
            } , 
            } , 
            'discounts':
            { #Discounts Object
              'total' : format_string(data[i][data_pos_dict['Total de Descontos (13)']]) * -1 if (format_string(data[i][data_pos_dict['Total de Descontos (13)']])) < 0 else format_string(data[i][data_pos_dict['Total de Descontos (13)']]), 
              'prev_contribution': format_string(data[i][data_pos_dict['Contribuição Previdenciária (10)']]) * -1 if(format_string(data[i][data_pos_dict['Contribuição Previdenciária (10)']]) < 0) else format_string(data[i][data_pos_dict['Contribuição Previdenciária (10)']]), 
              'ceil_retention': format_string(data[i][data_pos_dict['Retenção por Teto Constitucional (12)']]) * -1 if(format_string(data[i][data_pos_dict['Retenção por Teto Constitucional (12)']]) < 0) else format_string(data[i][data_pos_dict['Retenção por Teto Constitucional (12)']]), 
              'income_tax': format_string(data[i][data_pos_dict['Imposto de Renda (11)']]) * - 1 if (format_string(data[i][data_pos_dict['Imposto de Renda (11)']]) < 0) else format_string(data[i][data_pos_dict['Imposto de Renda (11)']]), 
            }
        }
        if(begin_row == end_row):
            return employee 
        else:
            employees.append(employee)
       
    return (employees)

# Retorna um dicionário mapeandoas posições das keys necessárias para indexar remunerações simples
def get_data_pos_dict(sheet, begin_row):
    data_position_dict = {
        'Matrícula': get_pos('Matrícula', sheet, begin_row),
        'Nome': get_pos('Nome', sheet, begin_row),
        'Cargo': get_pos('Cargo', sheet, begin_row),
        'Lotação': get_pos('Lotação', sheet, begin_row),
                
        "Remuneração do Cargo Efetivo (1)": get_pos('   Remuneração do     Cargo Efetivo (1)                                         '.strip(), sheet, begin_row + 2),
        "Outras Verbas Remuneratórias Legais ou Judiciais (2)": get_pos('Outras Verbas Remuneratórias Legais ou Judiciais (2)', sheet, begin_row +2),
        "Função de Confiança ou Cargo em Comissão (3)": get_pos('Função de Confiança ou Cargo em Comissão (3)', sheet, begin_row+2),
        "Gratificação Natalina (4)": get_pos('Gratificação Natalina (4)', sheet, begin_row+2),
        'Férias (1/3 Constitucional) (5)': get_pos('Férias (1/3 Constitucional) (5)', sheet, begin_row+2),
        'Abono de Permanência (6)': get_pos('Abono de Permanência (6)', sheet, begin_row+2),
        'Outras Remunerações Temporárias (7)': get_pos('Outras Remunerações Temporárias (7)', sheet, begin_row+1),
        'Verbas Indenizatórias (8)': get_pos('Verbas Indenizatórias (8)', sheet, begin_row+1),
        'Total de Rendimentos Brutos (9)': get_pos('Total de Rendimentos Brutos (9)', sheet, begin_row),
        
        'Contribuição Previdenciária (10)': get_pos('Contribuição Previdenciária (10)' , sheet, begin_row+2),
        'Imposto de Renda (11)': get_pos('Imposto de Renda (11)', sheet, begin_row+2),
        'Retenção por Teto Constitucional (12)': get_pos('Retenção por Teto Constitucional (12)', sheet, begin_row+2),
        'Total de Descontos (13)': get_pos('Total de Descontos (13)', sheet, begin_row+1),

        'Rendimento Líquido Total * (14)': get_pos('Rendimento Líquido Total * (14)', sheet, begin_row)
    }
    return data_position_dict

# Retorna um dicionário mapeando as keys necessárias para indexar Verbas indenizátorias
def get_indemnity_pos_dict(sheet, begin_row):
    indemnity_position_dict = {
            'Matrícula': get_pos('Matrícula', sheet,begin_row),
            'Nome': get_pos('Nome', sheet, begin_row),
            'Férias Indenizatórias': get_pos('Férias Indenizatórias', sheet, begin_row+1),
            'Auxílio-alimentação': get_pos('Auxílio-alimentação', sheet, begin_row+1),
            'Auxílio-creche': get_pos('Auxílio-creche', sheet, begin_row+1),
            'Auxílio-transporte': get_pos('Auxílio-transporte', sheet, begin_row+1),
            'Transporte Mobiliário': get_pos('Transporte Mobiliário', sheet, begin_row+1),
            'Auxílio-natalidade': get_pos('Auxílio-natalidade', sheet, begin_row+1),
            'Ajuda de Custo': get_pos('Ajuda de Custo', sheet, begin_row+1),
            'Auxílio-moradia': get_pos('Auxílio-moradia', sheet, begin_row+1),
            'Abono Pecuniário': get_pos('Abono Pecuniário', sheet, begin_row+1),
            'Licença Prêmio em Pecúnia': get_pos('Licença Prêmio em Pecúnia', sheet, begin_row +1),
            'Total de Indenizações': get_pos('Total de Indenizações', sheet, begin_row +1),
            'Gratificação de Perícia e Projeto': get_pos('Gratificação de Perícia e Projeto', sheet, begin_row+1),
            'Gratificação Exercício Cumulativo de Ofício': get_pos('Gratificação Exercício Cumulativo de Ofício', sheet, begin_row +1),
            'Gratificação Encargo de Curso e Concurso': get_pos('Gratificação Encargo de Curso e Concurso', sheet, begin_row +1),
            'Gratificação Local de Trabalho': get_pos('Gratificação Local de Trabalho', sheet, begin_row +1),
            'Gratificação Natalina': get_pos('Gratificação Natalina', sheet, begin_row +1),
            'Hora Extra': get_pos('Hora Extra', sheet, begin_row +1),
            'Abono de Permanência': get_pos('Abono de Permanência', sheet, begin_row +1),
            'Adicional Noturno': get_pos('Adicional Noturno', sheet, begin_row +1),
            'Adicional Atividade Penosa': get_pos('Adicional Atividade Penosa', sheet, begin_row +1),
            'Adicional Insalubridade': get_pos('Adicional Insalubridade', sheet, begin_row +1),
            'Outras Verbas Remuneratórias': get_pos('Outras Verbas Remuneratórias', sheet, begin_row+1),
            'Outras Verbas Remuneratórias Retroativas/Temporárias': get_pos('Outras Verbas Remuneratórias Retroativas/Temporárias', sheet, begin_row+1),
            'Férias': get_pos('Férias', sheet, begin_row+1),
            'Total de Verbas Temporárias': get_pos('Total de Verbas Temporárias', sheet, begin_row +1),
    }

    return indemnity_position_dict

#Retorna a posição final de indexação de uma planilha do tipo Verba Indenizatória
def get_inde_end_row(data, begin_row, pos):
    i = begin_row
    try:
        while(i < len(data)):
            if(data[i][pos] == ''):
                return i 
            else:
                i += 1
    except:
        return i-1

#Parser, convertendo os objetos para o formato exigido para empregados com dados indenizatórios
def employees_indemnity(file_name, indemnity_name, outputPath, year, month, file_type):

    #Definindo aspectos do main Data
    extension = file_name.split('.')
    path = './/' + outputPath + "//" + file_name

    data = read_data(path, extension)

    #Definindo aspectos dos dados indenizatórios
    indemnity_extension = indemnity_name.split('.')
    indemnity_path = './/' + outputPath  + '//' + indemnity_name

    indemnity_data = read_data(indemnity_path, indemnity_extension)

    #Definindo Folhas interáveis das planilhas
    keys = []
    for key in data.keys():
        keys.append(key)
    sheet = data[keys[0]]

    indemnity_keys = []
    for key in indemnity_data.keys():
        indemnity_keys.append(key)
    indemnity_sheet = indemnity_data[indemnity_keys[0]]

    #Definindo linhas Iteráveis da planilha Principal
    begin_string  = "Matrícula" 
    begin_row = get_begin_row(sheet, begin_string)

    end_string = "TOTAL GERAL"
    end_row = get_end_row(sheet, end_string)

    #Definindo linhas Iteráveis da planilha Indenizatória
    indemnity_begin_string = "Matrícula"
    indemnity_begin_row = get_begin_row(indemnity_sheet, indemnity_begin_string)
    
    #Recuperando Informações acerca da posição dos elementos nas planilhas
    data_pos_dict = get_data_pos_dict(sheet, begin_row)
    indemnity_pos_dict = get_indemnity_pos_dict(indemnity_sheet, indemnity_begin_row)
    
    indemnity_end_row = get_inde_end_row(indemnity_sheet,indemnity_begin_row + 1,indemnity_pos_dict['Férias Indenizatórias'])

    return all_employees_indemnity(sheet, begin_row, end_row, data_pos_dict, indemnity_sheet, indemnity_begin_row, indemnity_end_row , indemnity_pos_dict, file_type)

# Formata as Strings para o json,  retirando os (R$)
def format_string(string):
    if(isinstance(string,  float)):
        return string
    elif(isinstance(string, int)):
        return float(string)
    aux  = str(string)

    if(' BRL' in aux):
        final = ''
        for i in aux:
            if((i != ' ') and ( i !='B') and(i != 'R') and (i != 'L') and( i != '.')):
                final+= i
            
        return float(final.replace(',','.'))

    if(aux.find('(') != -1):
        aux = string[2:-1]
        aux = aux.replace(',', '.')
    else:
        aux = string[2:]
        aux = aux.replace(',', '.')
    return float(aux)

#Realiza uma linear pelo id em questão
def match_row(indemnity_data, indemnity_begin_row, indemnity_pos_dict, indemnity_end_row, id):
    for i in range(indemnity_begin_row, indemnity_end_row):
        if(indemnity_data[i][indemnity_pos_dict['Matrícula']] == id):
            return i
    return None 

#Função responsável por definir array com dados dos empregados + indenizações
def all_employees_indemnity(data, begin_row, end_row, data_pos_dict, indemnity_data, indemnity_begin_row, indemnity_end_row, indemnity_pos_dict, file_type):
    employees = []
    #Inicializando valores de idexação
    i = begin_row + 3
    j = indemnity_begin_row + 2
    while(i < end_row):
        if(data[i][data_pos_dict['Matrícula']] == indemnity_data[j][indemnity_pos_dict['Matrícula']]):
            employee = {
                    'reg' : data[i][data_pos_dict['Matrícula']], 
                    'name': data[i][data_pos_dict['Nome']], 
                    'role': data[i][data_pos_dict['Cargo']], 
                    'type': file_type,  
                    'workplace': data[i][data_pos_dict['Lotação']], 
                    'active': True if ('Ativos' in file_type) else False, 
                    "income": 
                    #Income Details
                    {'total' : format_string(data[i][data_pos_dict['Rendimento Líquido Total * (14)']]),  # ? Total Liquido ??
                        'wage'  : format_string(data[i][data_pos_dict['Remuneração do Cargo Efetivo (1)']]), 
                        'perks' : 
                    #Perks Object 
                    { 'total' : format_string(indemnity_data[j][indemnity_pos_dict['Total de Indenizações']]), 
                        'food' : format_string(indemnity_data[j][indemnity_pos_dict['Auxílio-alimentação']]), 
                        'transportation': format_string(indemnity_data[j][indemnity_pos_dict['Auxílio-transporte']]), 
                        'pre_school': format_string(indemnity_data[j][indemnity_pos_dict['Auxílio-transporte']]), 
                        'birth_aid': format_string(indemnity_data[j][indemnity_pos_dict['Auxílio-natalidade']]), 
                        'housing_aid': format_string(indemnity_data[j][indemnity_pos_dict['Auxílio-moradia']]), 
                        'subistence': format_string(indemnity_data[j][indemnity_pos_dict['Ajuda de Custo']]), 
                        'compensatory_leave':format_string(indemnity_data[j][indemnity_pos_dict['Abono de Permanência']]),  
                        'pecuniary':format_string(indemnity_data[j][indemnity_pos_dict['Abono Pecuniário']]), 
                        'vacation_pecuniary':format_string(indemnity_data[j][indemnity_pos_dict['Férias Indenizatórias']]), #Férias
                        'furniture_transport':format_string(indemnity_data[j][indemnity_pos_dict['Transporte Mobiliário']]), 
                        "premium_license_pecuniary": format_string(indemnity_data[j][indemnity_pos_dict['Licença Prêmio em Pecúnia']]), 
                    }, 
                    'other': 
                    { #Funds Object 
                        'total': format_string(indemnity_data[j][indemnity_pos_dict['Total de Verbas Temporárias']]), 
                        'eventual_benefits': format_string(indemnity_data[j][indemnity_pos_dict['Férias']]),  #Férias
                        'trust_position' : format_string(data[i][data_pos_dict['Função de Confiança ou Cargo em Comissão (3)']]),  #Pericia e projeto
                        'gratification': format_string(indemnity_data[j][indemnity_pos_dict['Gratificação de Perícia e Projeto']]) +
                        format_string(indemnity_data[j][indemnity_pos_dict['Gratificação Exercício Cumulativo de Ofício']]) + 
                        format_string(indemnity_data[j][indemnity_pos_dict['Gratificação Encargo de Curso e Concurso']]) +
                        format_string(indemnity_data[j][indemnity_pos_dict['Gratificação Local de Trabalho']]) + 
                        format_string(indemnity_data[j][indemnity_pos_dict['Gratificação Natalina']]), 
                        'others_total': format_string(indemnity_data[j][indemnity_pos_dict['Hora Extra']]) + 
                        format_string(indemnity_data[j][indemnity_pos_dict['Adicional Noturno']]) + 
                        format_string(indemnity_data[j][indemnity_pos_dict['Adicional Atividade Penosa']]) + 
                        format_string(indemnity_data[j][indemnity_pos_dict['Adicional Insalubridade']]) +
                        format_string(indemnity_data[j][indemnity_pos_dict['Outras Verbas Remuneratórias']]) + 
                        format_string(indemnity_data[j][indemnity_pos_dict['Outras Verbas Remuneratórias Retroativas/Temporárias']]), 
                        'others': format_string(data[i][data_pos_dict['Outras Verbas Remuneratórias Legais ou Judiciais (2)']]), 
                    } , 
                    } , 
                    'discounts':
                    { #Discounts Object
                        'total' : format_string(data[i][data_pos_dict['Total de Descontos (13)']]) * -1 if (format_string(data[i][data_pos_dict['Total de Descontos (13)']])) < 0 else format_string(data[i][data_pos_dict['Total de Descontos (13)']]), 
                        'prev_contribution': format_string(data[i][data_pos_dict['Contribuição Previdenciária (10)']]) * -1 if(format_string(data[i][data_pos_dict['Contribuição Previdenciária (10)']]) < 0) else format_string(data[i][data_pos_dict['Contribuição Previdenciária (10)']]), 
                        'ceil_retention': format_string(data[i][data_pos_dict['Retenção por Teto Constitucional (12)']]) * -1 if(format_string(data[i][data_pos_dict['Retenção por Teto Constitucional (12)']]) < 0) else format_string(data[i][data_pos_dict['Retenção por Teto Constitucional (12)']]), 
                        'income_tax': format_string(data[i][data_pos_dict['Imposto de Renda (11)']]) * -1 if(format_string(data[i][data_pos_dict['Imposto de Renda (11)']]) < 0) else format_string(data[i][data_pos_dict['Imposto de Renda (11)']]), 
                    }
                }
            i += 1
            j += 1
        else:
            match_id = data[i][data_pos_dict['Matrícula']]
            match = match_row(indemnity_data, indemnity_begin_row, indemnity_pos_dict, indemnity_end_row, match_id)
            if(match == None ):
                #Significa que não temos dados acerca de verbas indenizatórias sobre o empregado
                # --------- Nesse preenchemos como um empregado sem vi , j se mantém, e i segue em frente ----- #
                employee = all_employees(data, i, i+1, data_pos_dict, file_type)
                i+= 1
            else:
                employee = {}
                i+= 1    
        if(len(employee) > 0):
            employees.append(employee)

    return employees

#Função Auxiliar responsável pela tradução de um mês em um numero.
def get_month_number(month):
    months = { 'Janeiro' : 1 , 
              'Fevereiro':2 , 
              'Março': 3, 
              'Abril': 4, 
              'Maio':5, 
              'Junho':6, 
              'Julho':7, 
              'Agosto':8, 
              'Setembro':9, 
              'Outubro':10, 
              'Novembro':11, 
              'Dezembro':12
            }
    return months[month]

#Função destinada a verificar se exisem os dados acerca de verbas indenizatórias 
#------ Apenas para querys pós julho de 2019 ------# 
def check_indemnity(year, month):
    valid_months2019 = ['Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    if(int(year) < 2019):
        return False 
    elif((int(year) == 2019) and (month not in valid_months2019)):
        return False
    else:
        return True

#Retorna o tipo de planilha baseado no nome do arquivo
def get_file_kind(name):
    if("membros-ativos" in name):
        return 'Membros Ativos'
    elif('membros-inativos' in name):
        return 'Membros Inativos'
    elif('servidores-ativos' in name):
        return 'Servidores Ativos'
    elif('servidores-inativos' in name):
        return 'Servidores Inativos'
    elif('pensionistas' in name):
        return "Pensionistas"
    elif('colaboradores' in name):
        return 'Colaboradores Ativos'
    else:
        sys.stderr.write('Tipo de arquivo não identificado: ' + name)
        os._exit(1)

#Processo de geração do objeto resultado do Crawler e Parser. 
def crawler_result(year,  month,  outputPath,  version,  file_names):
    #Realizando o processo de parser em todas as planilhas
    employee = []
    final_employees = [] 
    if(check_indemnity(year, month)):
        indemnity_names = file_names.pop(-1)
        for i in range(len(file_names)):
            final_employees.append(employees_indemnity(file_names[i],  indemnity_names[i],  outputPath,  year,  month,  get_file_kind(file_names[i])))
    else:
        for i in range(len(file_names)):
            final_employees.append(employees(file_names[i], outputPath, year, month, get_file_kind(file_names[i])))

    #Armazenando Todos os Empregados em lista unica
    for lista in final_employees:
        for employe in lista:
            employee.append(employe) 

    month_number = get_month_number(month)
    now  = datetime.now()

    return {
        'agencyID' : 'mpf' , 
        'month' : month_number, 
        'year' : int(year), 
        'crawler': 
        { #CrawlerObject
             'crawlerID': 'mpf', 
             'crawlerVersion': version,   
        }, 
        'files' : file_names, 
        'employees': employee, 
        'timestamp': now.strftime("%H:%M:%S"), 
    }