import pandas as pd
from datetime import datetime
import os

cwd = os.getcwd()

remuneracoes = {
    "matricula": 0,
    "nome": 1,
    "cargo": 2,
    "lotacao": 3,
    "cargo_efetivo": 4,
    "outras_verbas": 5,
    "cargo_em_comissão": 6,
    "gratificacao_natalina": 7,
    "ferias": 8,
    "abono_de_permanencia": 9,
    "temporarias": 10,
    "verbas_indenizatorias": 11,
}

descontos = {
    "matricula": 0,
    "nome": 1,
    "cargo": 2,
    "lotacao": 3,
    "contribuicao_previdenciaria": 5,
    "imposto_de_renda": 6,
    "retencao_por_teto__constitucional": 7
}

# Read data downloaded from the crawler
def read_data(path):
    try:
        data = pd.read_excel(cwd + path)
        return data
    except:
        print('Cannot Read File.')

# Define first iterable line 
def get_begin_row(data,rows,begin_string):
    for row in rows:
        if(data.iloc[row][0] == begin_string):
            return int(row) + 3 

# Define last iterable line 
def get_end_row(data,rows,end_string):
    print(data.iloc[84][1])
    for row in rows:
        if(data.iloc[row][0] == end_string):
            print(int(row) -2)
            return int(row) -2

def employees(file_name, path): 
    data = read_data(path)
    rows  = list(data.index.values)
    begin_string  = "Matrícula" # word before starting data
    begin_row = get_begin_row(data,rows,begin_string)
    end_string = "1  Remuneração do cargo efetivo - Subsídio, Vencimento, GAMPU, V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza." # phrase after finishing the data
    end_row = get_end_row(data,rows,end_string)
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
               'food' : 0,
               'transportation': 0,
               'preSchool': 0, 
               'health': 0, # Não encontrado
               'birthAid': 0, # Não encontrado
               'housingAid': 0,# Não encontrado
               'subistence': 0, #Não encontrado
               'otherPerksTotal': 0,# Não encontrado
               'others': "" #Não encontrado
            },
            'other': 
            { #Funds Object 
              'total': data.iloc[i][10],
              'personalBenefits': 0, #Não encontrado 
              'eventualBenefits': data.iloc[i][8], #Férias
              'positionOfTrust' : data.iloc[i][6], 
              'daily': 0 , #Não encontrado
              'gratification': data.iloc[i][4], #gratificação natalina
              'originPosition': 0, #Não encontrado
              'otherFundsTotal':0, #Não encontrado
              'others': data.iloc[i][5], #Outras verbas remuneratórias, legais ou judiciais
            } ,
            } ,
     'discounts':
            { #Discounts Object
              'total' : data.iloc[i][16],
              'prevContribution': data.iloc[i][13],
              'cell Retention': data.iloc[i][15], #Retenção por teto constitucional
              'incomeTax': data.iloc[i][14],
              'otherDiscountsTotal': 0,
              'others': '',
            }
        }
        if(begin_row == end_row):
            return employee 
        else:
            employees.append(employee)
       
    return employees

