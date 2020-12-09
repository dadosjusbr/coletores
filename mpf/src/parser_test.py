import parser
import os

# Teste de unidade para cada planilha do mpf, de modo a aumentar a confiança no processo de parsing.
# Objetos criados pela análise da unica linha em questão das planilhas referentes a Janeiro de 2020--- #

#Objeto esperado para o arquivo de teste de membros ativos
active_member = {
    'reg': 844,
    'name': 'LAURO PINTO CARDOSO NETO',
    'role': 'PROCURADOR REGIONAL DA REPÚBLICA',
    'type': "Membros Ativos",
    'workplace': 'PRR1ª REGIÃO',
    'active': True,
    'income':
        #Income details
        { 'total': 62012.26,
            'wage':35462.22,
            #Perks object
            'perks':{
                'total':35416.56,
                'food': 910.08,
                'transportation': 0.00,
                'pre_school': 0.00,
                'housing_aid': 0.00,
                'subistence': 0.00,
                'compensatory_leave': 0.00,
                'pecuniary':34506.48,
                'vacation_pecuniary':0.00,
                'furniture_transport':0.00,
                'premium_license_pecuniary':0.00,        
            },
            'other':
            { #Funds Object
                'total':48647.33,
                'eventual_benefits':25879.86,
                'trust_position':0.00,
                'gratification': 0.00 +
                0.00 +
                0.00 +
                0.00 +
                19409.9,
                'others_total': 0.00 +
                0.00 +
                0.00 +
                0.00 + 
                3357.57 +
                0.00,
                'others': 3357.57,
            },     
        },
        'discounts':
        {#Discounts Object
            'total': 18739.72,
            'prev_contribution': 4270.17,
            'ceil_retention': 0.00,
            'income_tax': 14464.55,
        }
}

#Objeto esperado para o arquivo de teste de membros inativos
inactive_member = {
    'reg': 8,
    'name': 'GILDA PEREIRA DE CARVALHO',
    'role': 'SUBPROCURADOR-GERAL DA REPÚBLICA',
    'type': "Membros Inativos",
    'workplace': 'PGR',
    'active': False,
    'income':
        #Income details
        { 'total': 25960.83,
            'wage':37328.65,
            #Perks object
            'perks':{
                'total':0.00,
                'food': 0.00,
                'transportation': 0.00,
                'pre_school': 0.00,
                'housing_aid': 0.00,
                'subistence': 0.00,
                'compensatory_leave': 0.00,
                'pecuniary':0.00,
                'vacation_pecuniary':0.00,
                'furniture_transport':0.00,
                'premium_license_pecuniary':0.00,        
            },
            'other':
            { #Funds Object
                'total':18664.33,
                'eventual_benefits':0.00,
                'trust_position':0.00,
                'gratification': 0.00 +
                0.00 +
                0.00 +
                0.00 +
                18664.33,
                'others_total': 0.00 +
                0.00 +
                0.00 +
                0.00 + 
                0.00 +
                0.00 ,
                'others': 0.00,
            },     
        },
        'discounts':
        {#Discounts Object
            'total': 11367.82,
            'prev_contribution': 3435.03,
            'ceil_retention': 0.00,
            'income_tax': 7927.79,
        }      
}

#Objeto esperado para o arquivo de teste de servidores ativos
active_server = {
    'reg': 2422,
    'name': 'ADRIANA MARIA LIMA DE PAULA',
    'role': 'TÉCNICO DO MPU/ADMINISTRAÇÃO',
    'type': "Servidores Ativos",
    'workplace': 'PR-PI',
    'active': True,
    'income':
        #Income details
        { 'total': 16750.17,
            'wage':11754.59,
            #Perks object
            'perks':{
                'total':910.08,
                'food': 910.08,
                'transportation': 0.00,
                'pre_school': 0.00,
                'housing_aid': 0.00,
                'subistence': 0.00,
                'compensatory_leave': 1466.5,
                'pecuniary':0.00,
                'vacation_pecuniary':0.00,
                'furniture_transport':0.00,
                'premium_license_pecuniary':0.00,        
            },
            'other':
            { #Funds Object
                'total':14272.33,
                'eventual_benefits':4443.94,
                'trust_position':0.00,
                'gratification': 0.00 +
                0.00 +
                0.00 +
                0.00 +
                6665.92,
                'others_total': 0.00 +
                0.00 +
                0.00 +
                0.00 + 
                1695.97 +
                0.00,
                'others': 1695.97,
            },     
        },
        'discounts':
        {#Discounts Object
            'total': 7580.78,
            'prev_contribution': 1466.5,
            'ceil_retention': 0.00,
            'income_tax': 2790,
        }      
}

#Objeto esperado para o arquivo de teste de servidores inativos
inactive_server = {
    'reg': 4942,
    'name': 'DERMEVAL FERREIRA PORTO',
    'role': 'TÉCNICO DO MPU/ADMINISTRAÇÃO',
    'type': "Servidores Inativos",
    'workplace': 'PR-SP',
    'active': False,

    'income':
        #Income details
        { 'total': 7239.12,
            'wage':11398.39,
            #Perks object
            'perks':{
                'total':910.08,
                'food': 910.08,
                'transportation': 0.00,
                'pre_school': 0.00,
                'housing_aid': 0.00,
                'subistence': 0.00,
                'compensatory_leave': 1358.3,
                'pecuniary':0.00,
                'vacation_pecuniary':0.00,
                'furniture_transport':0.00,
                'premium_license_pecuniary':0.00,        
            },
            'other':
            { #Funds Object
                'total':8482.3,
                'eventual_benefits':0.00,
                'trust_position':0.00,
                'gratification': 0.00 +
                0.00 +
                0.00 +
                0.00 +
                6174.13,
                'others_total': 0.00 +
                0.00 +
                0.00 +
                0.00 + 
                949.87+
                0.00 ,
                'others': 949.87,
            },     
        },
        'discounts':
        {#Discounts Object
            'total': 5517.57,
            'prev_contribution': 1358.3,
            'ceil_retention': 0.00,
            'income_tax': 2526.41,
        }      
}

#Objeto esperado para o arquivo de teste de Pensionistas
pensioner = {
    'reg': 90916902,
    'name': 'ACELINO MARTINIANO DA SILVA NETO',
    'role': 'PENSIONISTA',
    'type': "Pensionistas",
    'workplace': 'PR-SE',
    'active': False,

    'income':
        #Income details
        { 'total': 13966.59,
            'wage': 14962.32,
            #Perks object
            'perks':{
                'total': 0.00,
                'food': 0.00,
                'transportation': 0.00,
                'pre_school': 0.00,
                'housing_aid': 0.00,
                'subistence': 0.00,
                'compensatory_leave': 0.00,
                'pecuniary':0.00,
                'vacation_pecuniary':0.00,
                'furniture_transport':0.00,
                'premium_license_pecuniary':0.00,        
            },
            'other':
            { #Funds Object
                'total':16850.9,
                'eventual_benefits':0.00,
                'trust_position':0.00,
                'gratification': 0.00 +
                0.00 +
                0.00 +
                0.00 +
                10604.41,
                'others_total': 0.00 +
                0.00 +
                0.00 +
                0.00 + 
                6246.49+
                0.00 ,
                'others': 6246.49,
            },     
        },
        'discounts':
        {#Discounts Object
            'total': 995.73,
            'prev_contribution': 990.73,
            'ceil_retention': 0.00,
            'income_tax': 0.00,
        }        
}

#Objeto esperado para o arquivo de teste de Colaboradores
colaborator = {
    'reg': 30418,
    'name': 'AGATA BOBBIO FERRAZ',
    'role': 'COLABORADOR',
    'type': "Colaboradores Ativos",
    'workplace': 'PRR1ª REGIÃO',
    'active': True,

    'income':
        #Income details
        { 'total': 7059.94,
            'wage': 0.00,
            #Perks object
            'perks':{
                'total': 910.08,
                'food': 910.08,
                'transportation': 0.00,
                'pre_school': 0.00,
                'housing_aid': 0.00,
                'subistence': 0.00,
                'compensatory_leave': 0.00,
                'pecuniary':0.00,
                'vacation_pecuniary':0.00,
                'furniture_transport':0.00,
                'premium_license_pecuniary':0.00,        
            },
            'other':
            { #Funds Object
                'total':4608.37,
                'eventual_benefits':0.00,
                'trust_position': 9216.74,
                'gratification': 0.00 +
                0.00 +
                0.00 +
                0.00 +
                4608.37,
                'others_total': 0.00 +
                0.00 +
                0.00 +
                0.00 + 
                0.00 +
                0.00 ,
                'others': 0.00,
            },     
        },
        'discounts':
        {#Discounts Object
            'total': 2156.8,
            'prev_contribution': 671.12,
            'ceil_retention': 0.00,
            'income_tax': 1480.68,
        }  
}

#Lista de planilhas remunerátorias e indenizatórias que o parser consome.

simple_remuneration = ["remuneracao-membros-ativos_2020_Janeiro.ods",'provento-membros-inativos_2020_Janeiro.ods',
"remuneracao-servidores-ativos_2020_Janeiro.ods","provento-servidores-inativos_2020_Janeiro.ods",
"valores-percebidos-pensionistas_2020_Janeiro.ods","valores-percebidos-colaboradores_2020_Janeiro.ods"]

vi = ["verbas-indenizatorias-e-outras-remuneracoes-temporarias_2020_Janeiro_membros-ativos.ods",
"verbas-indenizatorias-e-outras-remuneracoes-temporarias_2020_Janeiro_membros-inativos.ods",
"verbas-indenizatorias-e-outras-remuneracoes-temporarias_2020_Janeiro_servidores-ativos.ods",
"verbas-indenizatorias-e-outras-remuneracoes-temporarias_2020_Janeiro_servidores-inativos.ods",
"verbas-indenizatorias-e-outras-remuneracoes-temporarias_2020_Janeiro_pensionistas.ods",
'verbas-indenizatorias-e-outras-remuneracoes-temporarias_2020_Janeiro_colaboradores.ods']

def get_parser_result_vi():
    file_path = 'test_files'
    year = 2020
    month = 'Janeiro'

    all_files = [] 

    for file in simple_remuneration:
        all_files.append(file)
    all_files.append(vi)

    return parser.crawler_result(year,month,file_path,all_files)

def get_scenario_list():
    scenarios = []
    scenarios.append(active_member)
    scenarios.append(inactive_member)
    scenarios.append(active_server)
    scenarios.append(inactive_server)
    scenarios.append(pensioner)
    scenarios.append(colaborator)

    return scenarios

result = get_parser_result_vi()
result_employees = result['employees']
expected_employees = get_scenario_list()

# Expected e result keys são iguais para qualquer objeto

# keys de cada dicionário que compoe o objeto employee
general_keys = ['reg', 'name', 'role', 'type', 'workplace', 'active']
income_keys = ['total','wage'] #[income]
perks_keys = ['total', 'food', 'transportation', 'pre_school', 'housing_aid', 'subistence',
'compensatory_leave', 'pecuniary','vacation_pecuniary', 'furniture_transport', 'premium_license_pecuniary'] #[income][perks]
funds_keys = ['total', 'eventual_benefits', 'trust_position', 'gratification', 'others_total', 'others'] #['income']['other']
discounts_keys = ['total', 'prev_contribution', 'ceil_retention', 'income_tax'] #[discounts]

#--- Assertations para testes de unidade ---#

#- Verifica se todos os funcionários são retornados --#
assert len(result_employees) == len(expected_employees)

#-- Verificando asserts de atributos gerais --#
for i in range(len(expected_employees)):
    for key in general_keys:
        assert expected_employees[i][key] == result_employees[i][key], ("Was expected" + str(expected_employees[i][key]) + 'but was send: ' +
        str(result_employees[i][key]) + ' .Object Number: ' + str(i) + ' .Field: '+
        str(key) + " ." )

#-- Verificando asserts de atributos do  objeto income -- #
for i in range(len(expected_employees)):
    for key in income_keys:
        assert expected_employees[i]['income'][key] == result_employees[i]['income'][key], ("Was expected" + str(expected_employees[i]['income'][key]) + 'but was send: ' +
        str(result_employees[i]['income'][key]) + ' .Object Number: ' + str(i) + ' .Field: '+
        str(key) + " ." )

#-- Verificando asserts de atributos do objeto perks --#
for i in range(len(expected_employees)):
    for key in perks_keys:
        assert expected_employees[i]['income']['perks'][key] == result_employees[i]['income']['perks'][key], ("Was expected" + str(expected_employees[i]['income']['perks'][key]) + 'but was send: ' +
        str(result_employees[i]['income']['perks'][key]) + ' .Object Number: ' + str(i) + ' .Field: '+
        str(key) + " ." )

#-- Verificando asserts de atributos do objeto Funds --#
for i in range(len(expected_employees)):
    for key in funds_keys:
        assert expected_employees[i]['income']['other'][key] == result_employees[i]['income']['other'][key], ("Was expected" + str(expected_employees[i]['income']['other'][key]) + 'but was send: ' +
        str(result_employees[i]['income']['perks'][key]) + ' .Object Number: ' + str(i) + ' .Field: '+
        str(key) + " ." )

#-- Verificando asserts de atributos do objeto Discounts --#
for i in range(len(expected_employees)):
    for key in discounts_keys:
        assert expected_employees[i]['discounts'][key] == result_employees[i]['discounts'][key], ("Was expected" + str(expected_employees[i]['discounts'][key]) + 'but was send: ' +
        str(result_employees[i]['discounts'][key]) + ' .Object Number: ' + str(i) + ' .Field: '+
        str(key) + " ." )
