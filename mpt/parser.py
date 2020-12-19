import pandas as pd
from datetime import datetime
from pandas_ods_reader import read_ods
import math
import sys
import os
nan = float('nan')

#Read excel file and turn data as a dataframe object
def read_data(file):
    try:
        data = pd.read_excel(file)
    except Exception as excep:
        sys.stderr.write('Cannot read data from file. The following exception was raised: ' + str(excep))
        os._exit(1)
    else: 
        return data

#Return frist row (int) of interesting data
def get_begin_row(data,rows,begin_string):
    for row in rows:
        if(data.iloc[row][0] == begin_string):
            new_begin = int(row)
    
    #Frist not none id afther begin_string
    begin = new_begin + 1
    for i in range(begin,len(data.index)):
        try:
            if(not math.isnan(data.iloc[i][0])):
                return i 
        except:
            return i

#Return last row (int) of interesting data
def get_end_row(data,rows,end_string):
    rows.reverse()
    for row in rows:
        if(data.iloc[row][0] == end_string):
            return int(row)

#Return File type based on fileName
def get_file_type(file):
    if('MembrosAtivos' in file):
        return "Membros Ativos"
    elif('MembrosInativos' in file):
        return "Membros Inativos"
    elif('ServidoresAtivos' in file):
        return "Servidores Ativos"
    elif("ServidoresInativos" in file):
        return 'Servidores Inativos'
    elif('Pensionistas' in file):
        return 'Pensionistas'
    elif('Colaboradores' in file):
        return 'Colaboradores Ativos'
    else:
        return 'Irregular/Unknown type'

#Return all employees in file on struct format 
def all_employees(file):

    data = read_data(file)
    rows = list(data.index.values)

    begin_string = "Matrícula ou Nome"
    begin = get_begin_row(data,rows,begin_string)

    end_string =  "Fonte da Informação: Sistema MentorRH"
    end = get_end_row(data,rows,end_string)

    file_type = get_file_type(file)

    return employees_struct(begin,end,data,file_type)

#Format Values to valid string remove (R$)
def cleanup_currency(string):
    if(isinstance(string, float)):
        return string
    elif(isinstance(string,int)):
        return float(string)

    aux  = str(string).split(',')
    int_part = aux[0]
    cents = aux[1]

    final_int = ''
    for caracther in int_part:
        if(caracther  == 'R' or caracther  == '$' or caracther == '.'):
            final_int = final_int + ''
        else:
            final_int  =  final_int + caracther

    return float(final_int + '.' + cents)

# Return all employees of a sheet in a struct
def employees_struct(begin,end,data,file_type):
    employees = []
    for i in range(begin,end):
        employee = {
            'reg' : int(data.iloc[i][0].split('-')[0]),
            'name': data.iloc[i][0].split('-')[1],
            'role': data.iloc[i][1],
            'type': file_type,  
            'workplace': data.iloc[i][2],
            'active': True if ('Ativos' in file_type) else False,
            "income": 
            #Income Details
            {'total' : cleanup_currency(data.iloc[i][18]), #Total Liquido
             'wage'  : cleanup_currency(data.iloc[i][4]),
             'perks' : 
            #Perks Object 
            { 'total' : cleanup_currency(data.iloc[i][10]),
               'compensatory_leave': cleanup_currency(data.iloc[i][9]),
               'vacation_pecuniary':cleanup_currency(data.iloc[i][8]),#Férias
            },
            'other': 
            { #Funds Object 
              'total': cleanup_currency(data.iloc[i][11]),
              'trust_position' : cleanup_currency(data.iloc[i][6]), 
              'gratification': cleanup_currency(data.iloc[i][7]),
              'others':cleanup_currency(data.iloc[i][5])

            } ,
            } ,
            'discounts':
            { #Discounts Object
              'total' : cleanup_currency(data.iloc[i][17]) * -1  if ( cleanup_currency(data.iloc[i][17]) < 0) else (cleanup_currency(data.iloc[i][17])),
              'prev_contribution': cleanup_currency(data.iloc[i][13]) * -1  if ( cleanup_currency(data.iloc[i][13]) < 0) else (cleanup_currency(data.iloc[i][13])),
              'ceil_retention': cleanup_currency(data.iloc[i][15]) * -1  if ( cleanup_currency(data.iloc[i][15]) < 0) else (cleanup_currency(data.iloc[i][15])),
              'income_tax': cleanup_currency(data.iloc[i][14]) * -1  if ( cleanup_currency(data.iloc[i][14]) < 0) else (cleanup_currency(data.iloc[i][14])),
            }
        }
        employees.append(employee)

    return (employees)

#Return Result object 
def parse(files,month,year,version):
    employees = []
    for file in files:
        file_employees = all_employees(file)
        for employee in file_employees:
            employees.append(employee)

    return {
        'agencyID' : 'mpt' ,
        'month' : month,
        'year' : year,
        'crawler': 
        { #CrawlerObject
             'crawlerID': 'mpt',
             'crawlerVersion': version, 
        },
        'files' : files,
        'employees': employees,
        'timestamp': datetime.now().strftime("%H:%M:%S"),
}