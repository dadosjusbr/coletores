import pandas as pd
from datetime import datetime
import math
nan = float('nan')

#Definindo primeira Linha iterável da planilha 
def get_begin_row(data,rows,begin_string):
    for row in rows:
        if(data.iloc[row][0] == begin_string):
            new_begin = int(row)

    #Primeiro indice não None pós matricula
    begin = new_begin +1
    for i in range(begin,len(data.index)):
        try:
            if(not math.isnan(data.iloc[i][0])):
                return i 
        except:
            return i
#Definindo ultima Linha Iterável da Planilha
def get_end_row(data,rows,end_string):
    rows.reverse()
    #Caso contenha total geral
    for row in rows:
        if(data.iloc[row][0] == end_string):
            return int(row)  
    
    #Se não temos total geral
    for row in rows:
        #Lugar com o primeiro nome de pessoas
        try:
            if(not math.isnan(data.iloc[row][2])):
                return  int(row)
        except:
            return int(row)
    return None

#Define estratégia de leitura baseada na extensão do arquivo.
def read_data(path,extension):
    if('ods' in extension):
        df_engine = 'odf'
    else:
        df_engine = 'xlrd'
    
    #Leitura de arquivo em disco.
    try:
        data = pd.read_excel(path,engine = df_engine)
    except Exception as excep:
        print(excep)
    return data

#Definindo primeira Linha iterável da planilha para planilhas sem Indenizações
def get_begin_row_notIn(data,rows,begin_string):
    for row in rows:
        if(data.iloc[row][0] == begin_string):
            new_begin = int(row)
    
#Parser, convertendo os objetos para o formato exigido para empregados sem dados indenizatórios
def employees(file_name,outputPath,year,month,file_type):

    #Definindo main Data
    extension = file_name.split('.')
    path = './/' + outputPath +'//' + file_name

    data = read_data(path,extension)
    rows = list(data.index.values)

    #Definindo linhas Iteráveis da planilha Principal
    begin_string  = "Nome ou Matrícula" 
    begin_row = get_begin_row(data,rows,begin_string)

    end_string = "TOTAL GERAL"
    end_row = get_end_row(data,rows,end_string)

    return all_employees_novi(data,begin_row,end_row,file_type)

#Para empregados sem dados de verbas indenizatórias 
def all_employees_novi(data,begin_row,end_row,file_type):
    employees = []
    for i in range(begin_row,end_row):
        employee = {
            'reg' : data.iloc[i][0],
            'name': data.iloc[i][0],
            'role': data.iloc[i][3],
            'type': file_type,  
            'workplace': data.iloc[i][13],
            'active': True if ('Ativos' in file_type) else False,
            "income": 
            #Income Details
            {'total' : format_string(data.iloc[i][25]), # ? Total Liquido ??
             'wage'  : format_string(data.iloc[i][14]),
             'perks' : 
            #Perks Object 
            { 'total' : format_string(data.iloc[i][27]),
               'vacation_pecuniary':format_string(data.iloc[i][18]),#Férias
            },
            'other': 
            { #Funds Object 
              'total': format_string(data.iloc[i][26]),
              'trust_position' : format_string(data.iloc[i][16]), #Pericia e projeto
              'gratification': format_string(data.iloc[i][17]), #Só existem dados da gratificação natalina
              'others': format_string(data.iloc[i][15]) + format_string(data.iloc[i][19]), #Não encontrado
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
def all_employees(data,begin_row,end_row,file_type):
    employees = []
    for i in range(begin_row,end_row):
        employee = {
            'reg' : data.iloc[i][0],
            'name': data.iloc[i][2],
            'role': data.iloc[i][7],
            'type': file_type,
            'workplace': data.iloc[i][11],
            'active': True if ('Ativos' in file_type) else False,
            "income": 
            #Income Details
            {'total' : format_string(data.iloc[i][26]), # ? Total Liquido ??
             'wage'  : format_string(data.iloc[i][12]),
             'perks' : 
            #Perks Object 
            { 'total' : format_string(data.iloc[i][20]),
               'compensatory_leave':format_string(data.iloc[i][19]), 
               'vacation_pecuniary':format_string(data.iloc[i][18]),#Férias
            },
            'other': 
            { #Funds Object 
              'total': format_string(data.iloc[i][27]),
              'trust_position' : format_string(data.iloc[i][14]), #Pericia e projeto
              'gratification': format_string(data.iloc[i][17]), #Só existem dados da gratificação natalina
              'others': format_string(data.iloc[i][13]), #Não encontrado
            } ,
            } ,
            'discounts':
            { #Discounts Object
              'total' : format_string(data.iloc[i][25]) * -1 if (format_string(data.iloc[i][25]) < 0) else format_string(data.iloc[i][25]),
              'prev_contribution': format_string(data.iloc[i][22]) * -1 if(format_string(data.iloc[i][22]) < 0) else format_string(data.iloc[i][22]),
              'ceil_retention': format_string(data.iloc[i][24]) * -1 if(format_string(data.iloc[i][24]) < 0) else format_string(data.iloc[i][24]),
              'income_tax': format_string(data.iloc[i][23]) * - 1 if (format_string(data.iloc[i][23]) < 0) else format_string(data.iloc[i][23]),
            }
        }
        if(begin_row == end_row):
            return employee 
        else:
            employees.append(employee)
       
    return (employees)

#Parser, convertendo os objetos para o formato exigido para empregados com dados indenizatórios
def employees_indemnity(file_name,indemnity_name,outputPath,year,month,file_type):

    #Definindo aspectos do main Data
    extension = file_name.split('.')
    path = './/' + outputPath + "//" + file_name

    data = read_data(path,extension)
    rows  = list(data.index.values)

    #Definindo linhas Iteráveis da planilha Principal
    begin_string  = "Matrícula" 
    begin_row = get_begin_row(data,rows,begin_string)

    end_string = "TOTAL GERAL"
    end_row = get_end_row(data,rows,end_string)

    #Definindo aspectos dos dados indenizatórios
    indemnity_extension = indemnity_name.split('.')
    indemnity_path = './/' + outputPath  + '//' + indemnity_name

    indemnity_data =  read_data(indemnity_path,indemnity_extension)

    return all_employees_indemnity(data,begin_row,end_row,indemnity_data,file_type)

# Encontra a linha que representa um funcionário na planilha de indenizações por meio do ID
def match_line(id,indemnity_data):
    rows = list(indemnity_data.index.values)
    for row in rows:
        if(indemnity_data.iloc[row][0] == id):
            return  row

# Formata as Strings para o json, retirando os (R$)
def format_string(string):
    if(isinstance(string, float)):
        return string
    elif(isinstance(string,int)):
        return float(string)
    aux  = str(string)
    if(aux.find('(') != -1):
        aux = string[2:-1]
        aux = aux.replace(',','.')
    else:
        aux = string[2:]
        aux = aux.replace(',','.')
    
    return float(aux)

#Função responsável por definir array com dados dos empregados + indenizações
def all_employees_indemnity(data,begin_row,end_row,indemnity_data,file_type):
    employees = []
    id = data.iloc[begin_row][0]
    match_row = match_line(id,indemnity_data)
    i = begin_row
    while(i <= end_row):
        #Por motivos desconhecidos alguns funcionários não estão na planilha indenizatória
                        # --- mesmo estando na planilha comum ---#
        if(indemnity_data.iloc[match_row][0] == data.iloc[i][0]):
            employee = {
                'reg' : data.iloc[i][0],
                'name': data.iloc[i][2],
                'role': data.iloc[i][7],
                'type': file_type, 
                'workplace': data.iloc[i][11],
                'active': True if ('Ativos' in file_type) else False,
                "income": 
                #Income Details
                {'total' : data.iloc[i][26], # ? Total Liquido ??
                    'wage'  : data.iloc[i][12],
                    'perks' : 
                #Perks Object 
                { 'total' : format_string(indemnity_data.iloc[match_row][26]),
                    'food' : format_string(indemnity_data.iloc[match_row][16]),
                    'transportation': format_string(indemnity_data.iloc[match_row][19]),
                    'pre_school': format_string(indemnity_data.iloc[match_row][17]),
                    'birth_aid': format_string(indemnity_data.iloc[match_row][21]),
                    'housing_aid': format_string(indemnity_data.iloc[match_row][23]),
                    'subistence': format_string(indemnity_data.iloc[match_row][22]),
                    'compensatory_leave':format_string(indemnity_data.iloc[match_row][33]), 
                    'pecuniary':format_string(indemnity_data.iloc[match_row][24]),
                    'vacation_pecuniary':format_string(indemnity_data.iloc[match_row][15]),#Férias
                    'furniture_transport':format_string(indemnity_data.iloc[match_row][20]),
                    "premium_license_pecuniary": format_string(indemnity_data.iloc[match_row][25]),
                },
                'other': 
                { #Funds Object 
                    'total': format_string(indemnity_data.iloc[match_row][40]),
                    'eventual_benefits': format_string(indemnity_data.iloc[match_row][39]), #Férias
                    'trust_position' : format_string(data.iloc[i][14]), #Pericia e projeto
                    'gratification': format_string(indemnity_data.iloc[match_row][27]) +
                    format_string(indemnity_data.iloc[match_row][28]) + 
                    format_string(indemnity_data.iloc[match_row][29]) +
                    format_string(indemnity_data.iloc[match_row][30]) + 
                    format_string(indemnity_data.iloc[match_row][31]),
                    'others_total': format_string(indemnity_data.iloc[match_row][32]) + 
                    format_string(indemnity_data.iloc[match_row][34]) + 
                    format_string(indemnity_data.iloc[match_row][35]) + 
                    format_string(indemnity_data.iloc[match_row][36]) +
                    format_string(indemnity_data.iloc[match_row][37]) + 
                    format_string(indemnity_data.iloc[match_row][38]),
                    'others': format_string(data.iloc[i][13]),
                } ,
                } ,
                'discounts':
                { #Discounts Object
                    'total' : (data.iloc[i][25]) * -1 if(format_string(data.iloc[i][25]) < 0) else format_string(data.iloc[i][25]),
                    'prev_contribution': data.iloc[i][22] * -1 if(format_string(data.iloc[i][22]) < 0) else format_string(data.iloc[i][22]),
                    'ceil_retention': data.iloc[i][24] * -1 if(format_string(data.iloc[i][24]) < 0) else format_string(data.iloc[i][24]),
                    'income_tax': (data.iloc[i][23] * - 1) if(format_string(data.iloc[i][23]) < 0) else format_string(data.iloc[i][23]),
                }
            }            
        else:
            id = data.iloc[i][0]
            before_match = match_row
            match_row = match_line(id,indemnity_data)
            if(match_row == None): 
                employee = all_employees(data,i,i,file_type)
            else:
                employee = all_employees(data,i,i,file_type)
                
        if(match_row == None):
            match_row = before_match
            i += 1
        else:
            match_row += 1
            i += 1 

        employees.append(employee)
    
    return (employees)

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
def check_indemnity(year,month):
    valid_months2019 = ['Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']

    if(int(year) < 2019):
        return False 
    elif((int(year) == 2019) and (month not in valid_months2019)):
        return False
    else:
        return True

#Processo de geração do objeto resultado do Crawler e Parser. 
def crawler_result(year,month,outputPath,file_names):
    #Ordem do tipo de arquivos
    file_order = ['Membros Ativos','Membros Inativos','Servidores Ativos','Servidores Inativos','Pensionistas','Colaboradores Ativos']

    #Realizando o processo de parser em todas as planilhas
    employee = []
    final_employees = [] 
    if(check_indemnity(year,month)):
        indemnity_names = file_names.pop(-1)
        for i in range(len(file_names)):
            final_employees.append(employees_indemnity(file_names[i],indemnity_names[i],outputPath,year,month,file_order[i]))
    else:
        for i in range(len(file_names)):
            final_employees.append(employees(file_names[i],outputPath,year,month,file_order[i]))

    #Armazenando Todos os Empregados em lista unica
    for lista in final_employees:
        for employe in lista:
            employee.append(employe) 

    month_number = get_month_number(month)
    now  = datetime.now()

    return {
        'agencyID' : 'MPF' ,
        'month' : month_number,
        'year' : int(year),
        'crawler': 
        { #CrawlerObject
             'crawlerID': 'mpf',
             'crawlerVersion': 'Inicial' ,  
        },
        'files' : file_names,
        'employees': employee,
        'timestamp': now.strftime("%H:%M:%S"),
        'procInfo' : ''
    }