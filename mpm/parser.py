import pandas as pd
from datetime import datetime
import os
import math

cwd = os.getcwd()

# Read data downloaded from the crawler
def read_data(path):
    try:
        data = pd.read_excel(cwd + path)
        return data
    except:
        print('Cannot Read File.')

# Define first iterable line 
def get_begin_row(data,rows,begin_string):
    new_begin = ''
    for row in rows:
        if(data.iloc[row][0] == begin_string):
            new_begin = int(row) + 1

    while(isNaN(data.iloc[new_begin][0])):  
        new_begin += 1
    return new_begin

def isNaN(string):
    return string != string

# Define last iterable line 
def get_end_row(data, rows, end_string):
    for row in rows:
        if(data.iloc[row][0] == end_string):
            return int(row) -2

def employees(file_name):
    data = read_data(file_name)
    rows  = list(data.index.values)
    begin_string  = "Matrícula" # word before starting data
    begin_row = get_begin_row(data,rows,begin_string)
    end_string_remuneration = "1  Remuneração do cargo efetivo - Subsídio, Vencimento, GAMPU, V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza." # phrase after finishing the data
    end_row = get_end_row(data,rows,end_string_remuneration)
    return all_employees(data,begin_row,end_row)

def employees_indemnity(file_name, indemnity_file_name):
    data = read_data(file_name)
    indemnity_data = read_data(indemnity_file_name)
    ativo = False
    if(file_name.__contains__("ativos")):
        ativo = True

    #define limits
    rows  = list(data.index.values)
    begin_string  = "Matrícula" # word before starting data
    begin_row = get_begin_row(data,rows,begin_string)
    end_string_remuneration = "1  Remuneração do cargo efetivo - Subsídio, Vencimento, GAMPU, V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza." # phrase after finishing the data
    end_row = get_end_row(data,rows,end_string_remuneration)
    
    return all_employees_indemnity(data, begin_row, end_row, indemnity_data, ativo)

def match_line(id,indemnity_data):
    rows = list(indemnity_data.index.values)
    for row in rows:
        if(indemnity_data.iloc[row][0] == id):
            return row

# Used when the employee is not on the indemnity list
def all_employees(data,begin_row,end_row):
    employees = []
    for i in range(begin_row,end_row):
        id = data.iloc[i][0]
        employee = {
            'reg' : data.iloc[i][0],
            'name': data.iloc[i][1],
            'role': data.iloc[i][2],
            'type': '' ,  
            'workplace': data.iloc[i][3],
            'active': True,
            "income": 
            #Income Details
            {'total' : data.iloc[i][17], # ? Total Liquido ??
             'wage'  : data.iloc[i][4],
             'perks' : 
            #Perks Object 
              { 'total' : data.iloc[i][11],
               'food' : '',
               'transportation': '',
               'preSchool': '', 
               'health': '', 
               'birthAid': '', 
               'housingAid': '',
               'subistence': '', 
               'otherPerksTotal': '',
               'others': "" 
            },
            'other': 
            { #Funds Object 
              'total': data.iloc[i][10],
              'personalBenefits': '',  
              'eventualBenefits': data.iloc[i][8], #Férias
              'positionOfTrust' : data.iloc[i][6], 
              'daily': '' , 
              'gratification': data.iloc[i][4], #gratificação natalina
              'originPosition': '', 
              'otherFundsTotal':'', 
              'others': data.iloc[i][5], #Outras verbas remuneratórias, legais ou judiciais
            } ,
            } ,
     'discounts':
            { #Discounts Object
              'total' : data.iloc[i][16],
              'prevContribution': data.iloc[i][13],
              'cell Retention': data.iloc[i][15], #Retenção por teto constitucional
              'incomeTax': data.iloc[i][14],
              'otherDiscountsTotal': '',
              'others': '',
            }
        }
        if(begin_row == end_row):
            return employee 
        else:
            employees.append(employee)
       
    return employees

def all_employees_indemnity(data,begin_row,end_row,indemnity_data, ativo):
    employees = []
    id = data.iloc[begin_row][0]
    match_row = match_line(id,indemnity_data)
    i = begin_row

    while(i <= end_row):
        if(indemnity_data.iloc[match_row][0] == data.iloc[i][0]):
            employee = {
                'reg' : data.iloc[i][0],
                'name': data.iloc[i][1],
                'role': data.iloc[i][2],
                'type': '' ,  
                'workplace': data.iloc[i][3],
                'active': ativo,
                "income": 
                #Income Details
                {'total' : data.iloc[i][17], # ? Total Liquido ??
                    'wage'  : data.iloc[i][4],
                    'perks' : 
                #Perks Object 
                {'total' : indemnity_data.iloc[match_row][13],
                    'food' : indemnity_data.iloc[match_row][5],
                    'transportation': indemnity_data.iloc[match_row][7],
                    'preSchool': '', 
                    'health': '', 
                    'birthAid': indemnity_data.iloc[match_row][6], 
                    'housingAid': indemnity_data.iloc[match_row][4],
                    'subistence': '', 
                    'otherPerksTotal': '',
                },
                'other': 
                 #Funds Object 
                {'total': data.iloc[i][10],
                    'personalBenefits': '',  
                    'eventualBenefits': data.iloc[i][8], #Férias
                    'positionOfTrust' : data.iloc[i][6], 
                    'daily': '' , 
                    'gratification': (data.iloc[i][4]) + (indemnity_data.iloc[match_row][11]), #gratificação natalina + grat. encargo cursou ou concurso
                    'originPosition': '', 
                    'otherFundsTotal': (indemnity_data.iloc[match_row][8]) + (indemnity_data.iloc[match_row][9]) + (indemnity_data.iloc[match_row][10]) + (indemnity_data.iloc[match_row][12]), 
                    'others': data.iloc[i][5], #Outras verbas remuneratórias, legais ou judiciais
                } ,
                } ,
                'discounts':
                { #Discounts Object
                    'total' : data.iloc[i][16],
                    'prevContribution': data.iloc[i][13],
                    'cell Retention': data.iloc[i][15], #Retenção por teto constitucional
                    'incomeTax': data.iloc[i][14],
                    'otherDiscountsTotal': '',
                    'others': '',
                }
                }            
        else:
            id = data.iloc[i][0]
            before_match = match_row
            match_row = match_line(id,indemnity_data)
            if(match_row == None): 
                employee = all_employees(data,i,i)
                
            # else:
            #     employee = all_employees(data,i,i)
                
        if(match_row == None):
            match_row = before_match
            i += 1
        else:
            match_row += 1
            i += 1 

        employees.append(employee)
    
    return (employees)


def crawler_result(year,month,file_names):
    final_employees = [] 
    indemnity_files_names = []
    files_names = []
    j= 0

    for i in range(len(file_names)):
        if(file_names[i].__contains__('Verbas Indenizatorias')):
            indemnity_files_names.append(file_names[i])
        else:
            files_names.append(file_names[i])
    
    for i in range(len(files_names)):
        final_employees.append(employees_indemnity(files_names[i], indemnity_files_names[j]))
        j += 1
   
    now  = datetime.now()

    return {
        'agencyID' : 'MPM' ,
        'month' : month,
        'year' : year,
        'crawler': 
        { #CrawlerObject
             'crawlerID': 'mpm',
             'crawlerVersion': 'Inicial' ,  
        },
        #'files' : file_names,
        'employees': final_employees,
        'timestamp': now.strftime("%H:%M:%S"),
        'procInfo' : ''
    }


