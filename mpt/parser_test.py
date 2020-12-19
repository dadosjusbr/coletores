import parser
import unittest
import os

# Unit test for each mpt spreadsheet, in order to increase confidence in the parsing process.
# Objects created by analyzing the single line in question from the test spreadsheets for January 2020- #

# Spreadsheets list
remuneration = ['.//test_files//remuneracaoMembrosAtivos-1-2020.xls', './/test_files//proventosMembrosInativos-1-2020.xls',
'.//test_files//remuneracaoServidoresAtivos-1-2020.xls', './/test_files//proventosServidoresInativos-1-2020.xls',
'.//test_files//proventosPensionistas-1-2020.xls', './/test_files//proventosColaboradores-1-2020.xls']

#Variables for test
year = 2020
month = 1

class ParserTest(unittest.TestCase):

    def test_active_member(self):
        #Expected Object from active members file.
        expected_active_member = {
            'reg' : 808,
            'name': 'ÉLISSON MIESSA DOS SANTOS',
            'role': 'PROCURADOR DO TRABALHO',
            'type': 'Membros Ativos',  
            'workplace': '4º OFÍCIO GERAL DA PTM DE RIBEIRÃO PRETO',
            'active': True,
            "income": 
            #Income Details
            {'total' : 39503.95, #Total Liquido
             'wage'  : 33689.11,
             'perks' : 
            #Perks Object 
            { 'total' : 0.00,
               'compensatory_leave': 0.00,
               'vacation_pecuniary': 0.00, #Férias
            },
            'other': 
            { #Funds Object 
              'total': 910.08,
              'trust_position': 0.00, 
              'gratification': 16844.55,
              'others':0.00,
            } ,
            } ,
            'discounts':
            { #Discounts Object
              'total' : 11029.71,
              'prev_contribution': 3705.80 ,
              'ceil_retention': 0.00,
              'income_tax': 7323.91,
            }
        }
        test_file = [remuneration[0]]
        result_employees = parser.parse(test_file,1,2020,'unspecified')['employees']

        self.assertEqual(1,len(result_employees))
        self.assertDictEqual(result_employees[0], expected_active_member)
    
    def test_inactive_member(self):
        #Expected Object from Inactive Member file.
        expected_inactive_member = {
            'reg' : 2407098,
            'name': "MARIA MANZANO MALDONADO",
            'role': 'INATIVO INTEGRAL P/ TEMPO SERVICO',
            'type': 'Membros Inativos',  
            'workplace': 'PROC. REGIONAL TRABALHO 02ª REGIAO - SP',
            'active': False,
            "income": 
            #Income Details
            {'total' : 44682.28, #Total Liquido
             'wage'  : 37328.65,
             'perks' : 
            #Perks Object 
            { 'total' : 0.00,
               'compensatory_leave': 0.00,
               'vacation_pecuniary': 0.00, #Férias
            },
            'other': 
            { #Funds Object 
              'total': 0.00,
              'trust_position' : 0.00, 
              'gratification': 18664.32,
              'others':0.00,
            } ,
            } ,
            'discounts':
            { #Discounts Object
              'total' : 11310.69,
              'prev_contribution': 3435.04,
              'ceil_retention': 0.00,
              'income_tax': 7875.65,
            }
        }
        test_file = [remuneration[1]]
        result_employees = parser.parse(test_file,1,2020,'unspecified')['employees']

        self.assertEqual(1,len(result_employees))
        self.assertDictEqual(result_employees[0], expected_inactive_member)
    
    def test_active_server(self):
        #Expected Object from Active server file.
        expected_active_server = {
            'reg' : 6006347,
            'name': 'FERNANDA DE DONÁ SHIMOFUSA',
            'role': 'TÉCNICO DO MPU/ADMINISTRAÇÃO / FC 02',
            'type': 'Servidores Ativos',  
            'workplace': 'SECRETARIA DA CHEFIA DE GABINETE DO PROCURADOR-CHEFE',
            'active': True,
            "income": 
            #Income Details
            {'total' : 13336.72, #Total Liquido
             'wage'  : 9689.68,
             'perks' : 
            #Perks Object 
            { 'total' : 0.00,
               'compensatory_leave': 0.00,
               'vacation_pecuniary': 0.00, #Férias
            },
            'other': 
            { #Funds Object 
              'total': 910.08,
              'trust_position' : 1185.05, 
              'gratification': 5340.47,
              'others':0.00,
            } ,
            } ,
            'discounts':
            { #Discounts Object
              'total' : 2878.48,
              'prev_contribution': 1044.54,
              'ceil_retention': 0.00,
              'income_tax': 1833.94,
            }
        }
        test_file = [remuneration[2]]
        result_employees = parser.parse(test_file,1,2020,'unspecified')['employees']

        self.assertEqual(1,len(result_employees))
        self.assertDictEqual(result_employees[0], expected_active_server)
    
    def test_inactive_server(self):
        #Expected Object from inactive server file.
        expected_inactive_server = {
            'reg' : 6000346,
            'name': 'ALOISIO FERREIRA DE VASCONCELOS',
            'role': 'INATIVO INTEGRAL P/ TEMPO SERVICO',
            'type': 'Servidores Inativos',  
            'workplace': 'DIRETORIA DE ORÇAMENTO E FINANÇAS',
            'active': False,
            "income": 
            #Income Details
            {'total' : 45793.62, #Total Liquido
             'wage'  : 18701.52,
             'perks' : 
            #Perks Object 
            { 'total' : 0.00,
               'compensatory_leave': 0.00,
               'vacation_pecuniary':0.00, #Férias
            },
            'other': 
            { #Funds Object 
              'total': 0.00,
              'trust_position' : 0.00, 
              'gratification': 15989.71,
              'others': 13277.90,
            } ,
            } ,
            'discounts':
            { #Discounts Object
              'total' : 2175.51,
              'prev_contribution': 2175.51,
              'ceil_retention':0.00 ,
              'income_tax': 0.00,
            }
        }
        test_file = [remuneration[3]]
        result_employees = parser.parse(test_file,1,2020,'unspecified')['employees']

        self.assertEqual(1,len(result_employees))
        self.assertDictEqual(result_employees[0], expected_inactive_server)

    def test_pensioner(self):
        #Expected Object from pensioner file.
        expected_pensioner  = {
            'reg' : 4200065,
            'name': 'ADRIANA DO REGO BARROS RAMAGEM SOARES',
            'role': 'PENSÃO ESPECIAL',
            'type': "Pensionistas",  
            'workplace': 'PROC. REGIONAL TRABALHO 01ª  REGIAO - RJ',
            'active': False,
            "income": 
            #Income Details
            {'total' : 21419.19, #Total Liquido
             'wage'  : 17731.11,
             'perks' : 
            #Perks Object 
            { 'total' : 0.00,
               'compensatory_leave': 0.00,
               'vacation_pecuniary':0.00, #Férias
            },
            'other': 
            { #Funds Object 
              'total': 0.00,
              'trust_position' : 0.00, 
              'gratification': 8865.55,
              'others': 0.00,
            } ,
            } ,
            'discounts':
            { #Discounts Object
              'total' : 5177.47,
              'prev_contribution': 1614.87,
              'ceil_retention': 0.00,
              'income_tax': 3562.60,
            }
        }
        test_file = [remuneration[4]]
        result_employees = parser.parse(test_file,1,2020,'unspecified')['employees']

        self.assertEqual(1,len(result_employees))
        self.assertDictEqual(result_employees[0], expected_pensioner)
    
    def test_colaborator(self):
        #Expected Object from Colaborator file.
        expected_colaborator = {
            'reg' : 6005546,
            'name': 'ADELSO DA SILVEIRA DUTRA',
            'role': 'CHEFE DA SECRETARIA DA PTM DE CHAPECÓ / FC 01',
            'type': "Colaboradores Ativos",  
            'workplace': 'SECRETARIA DA PTM DE CHAPECÓ',
            'active': True,
            "income": 
            #Income Details
            {'total' : 1863.60, #Total Liquido
             'wage'  : 0.00,
             'perks' : 
            #Perks Object 
            { 'total' : 949.87,
               'compensatory_leave': 0.00,
               'vacation_pecuniary':339.72, #Férias
            },
            'other': 
            { #Funds Object 
              'total': 910.08,
              'trust_position' : 1019.17, 
              'gratification': 509.58,
              'others': 0.00,
            } ,
            } ,
            'discounts':
            { #Discounts Object
              'total' : 4.87,
              'prev_contribution': 0.00,
              'ceil_retention': 0.00,
              'income_tax': 4.87,
            }
        }
        test_file = [remuneration[5]]
        result_employees = parser.parse(test_file,1,2020,'unspecified')['employees']

        self.assertEqual(1,len(result_employees))
        self.assertDictEqual(result_employees[0], expected_colaborator)

if __name__ == '__main__':
    unittest.main()