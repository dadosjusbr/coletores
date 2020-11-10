from pyexcel_ods import get_data 
from pyexcel_xls import get_data 

#Definindo primeira Linha iterável da planilha 
def get_begin_line(planilha):
    line = 0
    for i in range(len(planilha)):
        if(len(planilha[i]) > 0):
            if(planilha[i][0] == "   Remuneração do     Cargo Efetivo (1)                                         "):
                return  line+1
            else:
                line += 1 
        else:
            line += 1

#Definindo ultima Linha Iterável da Planilha
def get_end_line(planilha):
    line = len(planilha)
    for i in range(len(planilha) -1 ,0,-1):
        if(len(planilha[i]) > 0):
            if(planilha[i][0] == "TOTAL GERAL"):
                return line - 1
            else:
                line -= 1
        else:
            line -= 1

#Parser, convertendo os objetos para o formato exigido
def employees(file_name):
    data =  get_data(file_name)
    keys = []
    for key in data.keys(): 
        keys.append(key)

    #Definindo planilha e linhas Iteráveis    
    planilha = data[keys[0]]
    begin_line = get_begin_line(planilha)
    end_line = get_end_line(planilha)
    employees = []
    for i in range(begin_line,end_line):
        employee = {
            'reg' : planilha[i][0],
            'name': planilha[i][1],
            'role': planilha[i][2],
            'type': '' ,  
            'workplace': planilha[i][3],
            'active': True,
            "income": 
            #Income Details
            {'total' : planilha[i][12],
             'wage'  : planilha[i][4],
             'perks' :
            #Perks Object 
            { 'total' : 0,
               'food' : 0 ,
               'transportation': 0,
               'preSchool': 0,
               'health': 0,
               'birthAid': 0,
               'housingAid': 0,
               'subistence': 0,
               'otherPerksTotal': 0,
               'others': ""
            },
            'other': 
            { #Funds Object 
              'total': planilha[i][10],
              'personalBenefits': planilha[i][5],
              'eventualBenefits': planilha[i][10],
              'positionOfTrust' : planilha[i][6],
              'daily': 0 ,
              'gratification': planilha[i][7],
              'originPosition': 0,
              'otherFundsTotal': planilha[i][11],
              'others': 0,
            } ,
            } ,
            'discounts':
            { #Discounts Object
              'total' : planilha[i][16] * -1,
              'prevContribution': planilha[i][13] * -1,
              'cell Retention': planilha[i][15] * -1 ,
              'incomeTax': planilha[i][14] - 1,
              'otherDiscountsTotal': 0 ,
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

#Processo de geração do objeto resultado do Crawler e Parser. 
#----------OBS : EM FUNCIONAMENTO PARCIAL PRECISA ABSTRAIR ----------#
def crawler_result(year,month,file_names):
    employee = employees(file_names[0])
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
        'timestamp': '21:15',
        'procInfo' : ''
    }