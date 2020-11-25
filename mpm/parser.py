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
def get_end_row(data, rows, end_string_remuneration, end_string_other_funds):
    for row in rows:
        if((data.iloc[row][0] == end_string_remuneration) or (data.iloc[row][0] == end_string_other_funds)):
            return int(row) -2

def employees(file_name):
    data = read_data(file_name)
    rows  = list(data.index.values)
    begin_string  = "Matrícula" # word before starting data
    begin_row = get_begin_row(data,rows,begin_string)
    end_string_remuneration = "1  Remuneração do cargo efetivo - Subsídio, Vencimento, GAMPU, V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza." # phrase after finishing the data
    end_string_other_funds = "1 Auxílio-alimentação, Auxílio-transporte, Auxílio-Moradia, Ajuda de Custo e outras dessa natureza, exceto diárias, que serão divulgadas no Portal da Transparência, discriminada de forma individualizada."
    end_row = get_end_row(data,rows,end_string_remuneration, end_string_other_funds)
    return all_employees(data,begin_row,end_row)

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

def crawler_result(year,month,file_names):
    for i in range(len(file_names)):
        employee = employees(file_names[i])

    now  = datetime.now()

    return {
        'agencyID' : 'MPM' ,
        'month' : month,
        'year' : int(year),
        'crawler': 
        { #CrawlerObject
             'crawlerID': 'mpm',
             'crawlerVersion': 'Inicial' ,  
        },
        'files' : file_names,
        'employees': employee,
        'timestamp': now.strftime("%H:%M:%S"),
        'procInfo' : ''
    }


