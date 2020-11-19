import pandas as pd

#Definindo primeira Linha iterável da planilha 
def get_begin_row(data,rows,begin_string):
    for row in rows:
        if(data.iloc[row][0] == begin_string):
                return int(row) + 3 
    
#Definindo ultima Linha Iterável da Planilha
def get_end_row(data,rows,end_string):
    for row in rows:
        if(data.iloc[row][0] == end_string):
            return int(row) -1 

#Define estratégia de leitura baseada na extensão do arquivo.
def read_data(path,extension):
    if('ods' in extension):
        df_engine = 'odf'
    else:
        df_engine = 'xlrd'
    
    #Leitura de arquivo em disco.
    try:
        data = pd.read_excel(path,engine = df_engine)
    except:
        print('Cannot Read File.')
    return data

#Parser, convertendo os objetos para o formato exigido
def employees(file_name,indemnity_name,outputPath,year,month):

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

    return all_employees(data,begin_row,end_row,indemnity_data)

# Encontra a linha que representa um funcionário na planilha de indenizações por meio do ID
def match_line(id,indemnity_data):
    rows = list(indemnity_data.index.values)
    for row in rows:
        if(indemnity_data.iloc[row][0] == id):
            return row

# Formata as Strings para o json, retirando os (R$)
def format_string(string):
    aux = ''
    for letter in str(string):
        if(letter != 'R' and letter != "$"):
            if(letter == ','):
                aux += '.'
            else:
                aux += letter
    return float(aux)

#Função responsável por definir array com dados dos empregados
def all_employees(data,begin_row,end_row,indemnity_data):
    employees = []
    for i in range(begin_row,end_row):
        id = data.iloc[i][0]
        match_row = match_line(id,indemnity_data)
        employee = {
            'reg' : data.iloc[i][0],
            'name': data.iloc[i][2],
            'role': data.iloc[i][7],
            'type': '' ,  
            'workplace': data.iloc[i][11],
            'active': True,
            "income": 
            #Income Details
            {'total' : format_string(data.iloc[i][26]), # ? Total Liquido ??
             'wage'  : format_string(data.iloc[i][12]),
             'perks' : 
            #Perks Object 
            { 'total' : format_string(indemnity_data.iloc[match_row][26]),
               'food' : format_string(indemnity_data.iloc[match_row][16]),
               'transportation': format_string(indemnity_data.iloc[match_row][19]),
               'preSchool': format_string(indemnity_data.iloc[match_row][17]),
               'health': 0, # Não encontrado
               'birthAid': format_string(indemnity_data.iloc[match_row][21]),
               'housingAid': format_string(indemnity_data.iloc[match_row][23]),
               'subistence': 0, #Não encontrado
               'otherPerksTotal': format_string(indemnity_data.iloc[match_row][15]) + 
                format_string(indemnity_data.iloc[match_row][20]) + 
                format_string(indemnity_data.iloc[match_row][22])+ 
                format_string(indemnity_data.iloc[match_row][24]) + 
                format_string(indemnity_data.iloc[match_row][25]),
               'others': ""
            },
            'other': 
            { #Funds Object 
              'total': format_string(indemnity_data.iloc[match_row][40]),
              'personalBenefits': 0, #Não encontrado 
              'eventualBenefits': format_string(indemnity_data.iloc[match_row][39]), #Férias
              'positionOfTrust' : format_string(indemnity_data.iloc[match_row][27]), #Pericia e projeto
              'daily': 0 , #Não encontrado
              'gratification': format_string(indemnity_data.iloc[match_row][28]) + 
              format_string(indemnity_data.iloc[match_row][29]) +
              format_string(indemnity_data.iloc[match_row][30]) + 
              format_string(indemnity_data.iloc[match_row][31]),
              'originPosition': 0,
              'otherFundsTotal': format_string(indemnity_data.iloc[match_row][32]) + 
              format_string(indemnity_data.iloc[match_row][33]) +
              format_string(indemnity_data.iloc[match_row][34]) + 
              format_string(indemnity_data.iloc[match_row][35]) + 
              format_string(indemnity_data.iloc[match_row][36]) +
              format_string(indemnity_data.iloc[match_row][37]) + 
              format_string(indemnity_data.iloc[match_row][38]),
              'others': "",
            } ,
            } ,
            'discounts':
            { #Discounts Object
              'total' : format_string(data.iloc[i][25]) * -1,
              'prevContribution': format_string(data.iloc[i][22]) * -1,
              'cell Retention': format_string(data.iloc[i][24]) * -1 ,
              'incomeTax': format_string(data.iloc[i][23]) * - 1,
              'otherDiscountsTotal': 0,
              'others': '',
            }
        }
        employees.append(employee)
    
    return (employees)

#Função Auxiliar responsável pela tradução de um mês em um numero.
def get_month_number(month):
    meses = { 'Janeiro' : 1 ,
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
    return meses[month]

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
    if(check_indemnity(year,month)):
        indemnity_names = file_names.pop(-1)
        employee = employees(file_names[0],indemnity_names[0],outputPath,year,month) 

    month_number = get_month_number(month)

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
        'timestamp': '15.56',
        'procInfo' : ''
    }