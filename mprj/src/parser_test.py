import os
import parser
import unittest
import pathlib
import numpy as np

class TestParser(unittest.TestCase):

    def test_membros_ativos(self):
        self.maxDiff = None

        expected = {
            'reg': '02003042' ,
            'name': 'ADELIA BARBOZA DE CARVALHO',
            'role': 'PROCURADOR DE JUSTICA',
            'type': 'membro',
            'workplace':'1ª PROCURADORIA DE JUSTIÇA JUNTO À 22ª CÂMARA CÍVEL DO TRIBUNAL DE JUSTIÇA DO ESTADO DO RIO DE JANEIRO',
            'active': True,
            'income':
                {
                    'total': 84630.50,
                    'wage': 37300.81,
                    'perks':{
                        'total': 5650.38,
                        'food': 1230.00,
                        'transportation': 0.00,
                        'health': 4420.38,
                    },
                    'other':
                    {
                        'total': 41679.31,
                        'trust_position': 0.00,
                        'gratification': 0.00,
                        'others_total': 41679.31,
                        'others':{
                            'Gratificação natalina': 0.00,
                            'Férias (1/3 constitucional)': 0.00,
                            'Abono de permanência': 5222.11,
                            'AUXÍLIO-EDUCAÇÃO': 0.00,
                            'CONVERSÃO DE LICENÇA ESPECIAL': 18650.40,
                            'DEVOLUÇÃO IR RRA':5986.06,
                            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS': 0.00,
                            'INDENIZAÇÃO POR LICENÇA NÃO GOZADA': 11820.74,
                            'DEVOLUÇÃO FUNDO DE RESERVA': 0.00,
                            'DIFERENÇAS DE AUXÍLIOS': 0.00,
                            'PARCELAS PAGAS EM ATRASO':0.00,
                        },
                    },
                },
                'discounts':
                {
                    'total': 13174.39,
                    'prev_contribution': 5222.11,
                    'ceil_retention':0.00,
                    'income_tax': 7952.28,
                }
        }
        files = [('./output_test/2020_11_MATIV.ods') , ('./output_test/2020_11_Verbas Indenizatórias-MATIV.ods')]
        employees = parser.parse(files)

        #Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_inativos(self):
        self.maxDiff = None

        expected = {
            'reg': '00179515',
            'name': 'ADA BUKSMAN',
            'role': 'PROMOTOR DE JUSTICA',
            'type': 'membro',
            'active': False,
            'income':
                {
                    'total': 45760.30,
                    'wage': 35462.22,
                    'perks':{
                        'total':2909.79,
                        'health': 2909.79,
                    },
                    'other':
                    {
                        'total': 7388.29,
                        'trust_position': 0.00,
                        'others_total': 7388.29,
                        'others':{
                            'Gratificação natalina': 0.00,
                            'Férias (1/3 constitucional)': 0.00,
                            'Abono de permanência': 0.00,
                            'AUXÍLIO-EDUCAÇÃO': 0.00,
                            'DEVOLUÇÃO IR RRA': 7388.29,
                            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS':0.00,
                            'INDENIZAÇÃO DE LICENÇA ESPECIAL/PRÊMIO NÃO USUFRUÍDA': 0.0,
                            'DEVOLUÇÃO FUNDO DE RESERVA':0.00,
                        },
                    },
                },
                'discounts':
                {
                    'total': 4438.49,
                    'prev_contribution': 4438.49,
                    'ceil_retention':0.00,
                    'income_tax': 0.00,
                }
        }
        files = [('./output_test/2020_11_MINAT.ods'), ('./output_test/2020_11_Verbas Indenizatórias-MINAT.ods')]
        employees = parser.parse(files)

        #Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_servidores_ativos(self):
        self.maxDiff = None

        expected = {
            'reg': '00003189',
            'name': 'ACELINO AMURIM DA SILVA',
            'role': 'TÉCNICO DO MP - ÁREA: PROCESSUAL',
            'type': 'servidor',
            'workplace': 'SECRETARIA DA 2ª PROMOTORIA DE JUSTIÇA CÍVEL DE DUQUE DE CAXIAS',
            'active': True,
            'income':
                {
                    'total': 17119.27,
                    'wage': 11644.51,
                    'perks':{
                        'total': 2522.71,
                        'food':1285.91,
                        'transportation':136.80,
                        'health':1100.00
                    },
                    'other':
                    {
                        'total': 2952.05,
                        'trust_position': 0.00,
                        'gratification':1285.04,
                        'others_total': 1667.01,
                        'others':{
                            'Gratificação natalina': 0.00,
                            'Férias (1/3 constitucional)': 0.00,
                            'Abono de permanência': 0.00,
                            'AUXÍLIO-ADOÇÃO': 0.00,
                            'AUXÍLIO-EDUCAÇÃO': 1667.01,
                            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS': 0.00,
                            'INDENIZAÇÃO DE LICENÇA ESPECIAL/PRÊMIO NÃO USUFRUÍDA': 0.00,
                            'DIFERENÇAS DE AUXÍLIOS': 0.00,
                            'PARCELAS PAGAS EM ATRASO': 0.00,
                            'SUBSTITUIÇÃO DE CARGO EM COMISSÃO / FUNÇÃO GRATIFICADA': 0.00

                        },
                    },
                },
                'discounts':
                {
                    'total': 3763.91,
                    'prev_contribution': 1630.23,
                    'ceil_retention':0.00,
                    'income_tax': 2133.68,
                }
        }
        files = [('./output_test/2020_11_SATIV.ods'), ('./output_test/2020_11_Verbas Indenizatórias-SATIV.ods')]
        employees = parser.parse(files)

        #Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def teste_servidores_inativos(self):
        self.maxDiff = None

        expected = {
            'reg': '00001322',
            'name': 'ADELAIDE BURATTO',
            'role': 'AUXILIAR DO MP - ÁREA: ADMINISTRATIVA',
            'type': 'servidor',
            'active': False,
            'income':
                {
                    'total': 9548.15,
                    'wage': 8827.26,
                    'perks':{
                        'total': 720.89,
                        'food':0.00,
                        'transportation':0.00,
                        'health': 720.89,
                    },
                    'other':
                    {
                        'total': 0.00,
                        'trust_position': 0.00,
                        'others_total': 0.00,
                        'others':{
                            'Gratificação natalina': 0.00,
                            'Férias (1/3 constitucional)': 0.00,
                            'Abono de permanência': 0.00,
                            'AUXÍLIO-ADOÇÃO': 0.00,
                            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS': 0.00,
                            'INDENIZAÇÃO DE LICENÇA ESPECIAL/PRÊMIO NÃO USUFRUÍDA': 0.00,
                            'DIFERENÇAS DE AUXÍLIOS': 0.00,
                            'PARCELAS PAGAS EM ATRASO': 0.00,
                        },
                    },
                },
                'discounts':
                {
                    'total': 1311.25,
                    'prev_contribution': 381.67,
                    'ceil_retention': 0.00,
                    'income_tax': 929.58,
                }
        }
        files = [('./output_test/2020_11_SINAT.ods'), ('./output_test/2020_11_Verbas Indenizatórias-SINAT.ods')]
        employees = parser.parse(files)

        #Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def teste_pensionistas(self):
        self.maxDiff = None

        expected = {
            'reg': '02002761-1',
            'name':'ACASSIA MARIA CARVALHO PEREIRA',
            'type': 'pensionista',
            'active': False,
            'income':
                {
                    'total': 26473.52,
                    'wage': 26473.52,
                    'perks':{},
                    'other':
                    {
                        'total': 0.00,
                        'trust_position': 0.00,
                        'others_total': 0.00,
                        'others':{
                            'Gratificação natalina': 0.00,
                            'Férias (1/3 constitucional)': 0.00,
                            'Abono de permanência': 0.00,
                        },
                    },
                },
                'discounts':
                {
                    'total': 7955.07,
                    'prev_contribution': 2852.15,
                    'ceil_retention': 0.00,
                    'income_tax': 5102.92,
                }
        }

        files = [('./output_test/2020_11_PENSI.ods')]
        employees = parser.parse(files)

        #Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def teste_colaboradores(self):
        self.maxDiff = None

        expected = {
            'name': 'AGHATTA CRYST DE BRITO GONÇALVES',
            'role': 'Bolsa auxílio ao estagiário forense. 20.22.0001.0028176.2020-34',
            'type': 'colaborador',
            'workplace': 'PROMOTORIA DE JUSTIÇA CÍVEL E DE FAMÍLIA DE RIO DAS OSTRAS',
            'active': True,
            'income':
            {
                'total': 870.00,
                'wage': 870.00,
            },
            'discounts':
            {
                'total': 0.00,
                'income_tax': 0.00,
            }
        }

        files = [('./output_test/2020_11_COLAB.ods')]
        employees = parser.parse(files)

        #Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def teste_servidores_ativos_outubro_2020(self):
        self.maxDiff = None

        expected = {
            'reg':'00004938',
            'name': 'ZILMA OLIVEIRA MARQUES',
            'role': 'TÉCNICO DO MP - ÁREA: ADMINISTRATIVA',
            'type': 'servidor',
            'workplace': 'SECRETARIA DA 2ª PROMOTORIA DE JUSTIÇA DE FAMÍLIA DA CAPITAL',
            'active': True,
            'income':
                {
                    'total': 11316.45,
                    'wage': 9217.66,
                    'perks':{
                        'total': 2098.79,
                        'food':1230.00,
                        'transportation':0.00,
                        'health':868.79
                    },
                    'other':
                    {
                        'total': 0.00,
                        'trust_position': 0.00,
                        'gratification': 0.00,
                        'others_total': 0.00,
                        'others':{
                            'Gratificação natalina': 0.00,
                            'Férias (1/3 constitucional)': 0.00,
                            'Abono de permanência': 0.00,
                            'AUXÍLIO-ADOÇÃO': 0.00,
                            'AUXÍLIO-EDUCAÇÃO': 0.00,
                            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS': 0.00,
                            'INDENIZAÇÃO DE LICENÇA ESPECIAL/PRÊMIO NÃO USUFRUÍDA': 0.00,
                            'DIFERENÇAS DE AUXÍLIOS': 0.00,
                            'PARCELAS PAGAS EM ATRASO': 0.00,
                            'SUBSTITUIÇÃO DE CARGO EM COMISSÃO / FUNÇÃO GRATIFICADA': 0.00
                        },
                    },
                },
                'discounts':
                {
                    'total': 2601.08,
                    'prev_contribution': 1290.47,
                    'ceil_retention':0.00,
                    'income_tax': 1310.61,
                }
        }
        files = [('./output_test/2020_10_SATIV.ods'),('./output_test/2020_10_Verbas Indenizatórias-SATIV.ods')]
        employees = parser.parse(files)

        #Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def teste_servidores_inativos_outubro_2020(self):
        self.maxDiff = None

        expected = {
            'reg': '00198219',
            'name': 'ANA CHRISTINA ARAGÃO COSTA',
            'role': 'ANALISTA DO MP - ÁREA: ADMINISTRATIVA',
            'type': 'servidor',
            'active': False,
            'income':
                {
                    'total': 39321.04,
                    'wage': 28245.21,
                    'perks':{
                        'total': 1100.00,
                        'transportation':0.00,
                        'health':1100.00
                    },
                    'other':
                    {
                        'total': 9975.83,
                        'trust_position': 0.00,
                        'others_total': 9975.83,
                        'others':{
                            'Gratificação natalina': 0.00,
                            'Férias (1/3 constitucional)': 0.00,
                            'Abono de permanência': 0.00,
                            'AUXÍLIO-ADOÇÃO': 0.00,
                            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS': 0.00,
                            'INDENIZAÇÃO DE LICENÇA ESPECIAL/PRÊMIO NÃO USUFRUÍDA': 9975.83,
                            'DIFERENÇAS DE AUXÍLIOS': 0.00,
                        },
                    },
                },
                'discounts':
                {
                    'total': 8989.29,
                    'prev_contribution': 3100.18,
                    'ceil_retention':0.00,
                    'income_tax': 5889.11,
                }
        }
        files = [('./output_test/2020_10_SINAT.ods'),('./output_test/2020_10_Verbas Indenizatórias-SINAT.ods')]
        employees = parser.parse(files)

        #Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def teste_membros_ativos_jan_2020(self):
        self.maxDiff = None

        expected = {
            'reg': '00002186',
            'name': 'ADIEL DA SILVA FRANÇA',
            'role': 'PROMOTOR DE JUSTICA',
            'workplace':'2ª PROMOTORIA DE JUSTIÇA DE EXECUÇÃO DE MEDIDAS SÓCIO-EDUCATIVAS DA CAPITAL',
            'type': 'membro',
            'active': True,
            'income':
                {
                    'total': 50557.48,
                    'wage': 33689.10,
                    'perks':{
                        'total': 3852.62,
                        'food': 1230.00,
                        'transportation': 1010.00,
                        'health': 1612.62,
                    },
                    'other':
                    {
                        'total': 13015.76,
                        'trust_position': 0.00,
                        'gratification': 3368.91,
                        'others_total': 9646.85,
                        'others':{
                            'Gratificação natalina': 0.00,
                            'Férias (1/3 constitucional)': 0.00,
                            'Abono de permanência': 0.00,
                            'AUXÍLIO-EDUCAÇÃO': 699.00,
                            'CONVERSÃO DE LICENÇA ESPECIAL': 0.00,
                            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS': 0.00,
                            'INDENIZAÇÃO POR LICENÇA NÃO GOZADA': 5614.85,
                            'DEVOLUÇÃO FUNDO DE RESERVA': 0.00,
                            'DIFERENÇAS DE AUXÍLIOS': 0.00,
                            'PARCELAS PAGAS EM ATRASO': 3333.00 ,
                        },
                    },
                },
                'discounts':
                {
                    'total': 12741.03,
                    'prev_contribution': 4716.47,
                    'ceil_retention':0.00,
                    'income_tax': 8024.56,
                }
        }
        files = [('./output_test/2020_01_MATIV.ods'),('./output_test/2020_01_Verbas Indenizatórias-MATIV.ods')]
        employees = parser.parse(files)

        #Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def teste_membros_ativos_fev_2020(self):
        self.maxDiff = None

        expected = {
            'reg': '01002838',
            'name': 'ADOLFO BORGES FILHO',
            'role': 'PROCURADOR DE JUSTICA',
            'workplace':'1ª PROCURADORIA DE JUSTIÇA JUNTO À 17ª CÂMARA CÍVEL DO TRIBUNAL DE JUSTIÇA DO ESTADO DO RIO DE JANEIRO',
            'type': 'membro',
            'active': True,
            'income':
                {
                    'total': 57465.53,
                    'wage': 39293.32,
                    'perks':{
                        'total': 6436.31,
                        'food': 1230.00,
                        'transportation': 336.67,
                        'health': 4869.64 ,
                        'housing_aid': 00.0,
                    },
                    'other':
                    {
                        'total': 11735.9,
                        'trust_position': 0.00,
                        'gratification': 0.00,
                        'others_total': 11735.9,
                        'others':{
                            'Gratificação natalina': 0.00,
                            'Férias (1/3 constitucional)': 0.00,
                            'Abono de permanência': 5501.06,
                            'AUXÍLIO-EDUCAÇÃO': 0.00,
                            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS': 0.00,
                            'INDENIZAÇÃO POR LICENÇA NÃO GOZADA': 0.00,
                            'DEVOLUÇÃO FUNDO DE RESERVA': 6234.84,
                            'DIFERENÇAS DE AUXÍLIOS': 0.00,
                            'PARCELAS PAGAS EM ATRASO': 0.00 ,
                        },
                    },
                },
                'discounts':
                {
                    'total': 13872.44,
                    'prev_contribution': 5501.06,
                    'ceil_retention':0.00,
                    'income_tax': 8371.38,
                }
        }
        files = [('./output_test/2020_02_MATIV.ods'),('./output_test/2020_02_Verbas Indenizatórias-MATIV.ods')]
        employees = parser.parse(files)

        #Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def teste_servidores_ativos_marco_2020(self):
        self.maxDiff = None

        expected = {
            'reg':'00005625',
            'name': 'ACYR QUARESMA JUNIOR',
            'role': 'TÉCNICO DO MP - ÁREA: ADMINISTRATIVA',
            'type': 'servidor',
            'workplace': 'SECRETARIA DO NÚCLEO DE INVESTIGAÇÃO DAS PROMOTORIAS DE JUSTIÇA DE INVESTIGAÇÃO PENAL DE NOVA IGUAÇU',
            'active': True,
            'income':
                {
                    'total': 11052.30,
                    'wage': 8382.82,
                    'perks':{
                        'total': 2669.48,
                        'food':1230.00,
                        'transportation': 376.20,
                        'health': 1063.28,
                    },
                    'other':
                    {
                        'total': 0.00,
                        'trust_position': 0.00,
                        'gratification': 0.00,
                        'others_total': 0.00,
                        'others':{
                            'Gratificação natalina': 0.00,
                            'Férias (1/3 constitucional)': 0.00,
                            'Abono de permanência': 0.00,
                            'AUXÍLIO-ADOÇÃO': 0.00,
                            'AUXÍLIO-EDUCAÇÃO': 0.00,
                            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS': 0.00,
                            'DIFERENÇAS DE AUXÍLIOS': 0.00,
                            'PARCELAS PAGAS EM ATRASO': 0.00,
                        },
                    },
                },
                'discounts':
                {
                    'total': 2286.76,
                    'prev_contribution': 1173.59,
                    'ceil_retention': 0.00,
                    'income_tax': 1113.17,
                }
        }
        files = [('./output_test/2020_03_SATIV.ods'),('./output_test/2020_03_Verbas Indenizatórias-SATIV.ods')]
        employees = parser.parse(files)

        #Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def teste_membros_ativos_abr_2020(self):
        self.maxDiff = None
        expected = {
            'reg': '00001954',
            'name': 'ADRIANA ARAUJO PORTO',
            'role': 'PROMOTOR DE JUSTICA',
            'workplace':'PROMOTORIA DE JUSTIÇA CÍVEL DE VALENÇA',
            'type': 'membro',
            'active': True,
            'income':
                {
                    'total': 49452.96,
                    'wage': 33689.10,
                    'perks':{
                        'total': 1285.91,
                        'food': 1285.91,
                        'health': 0.00 ,
                        'housing_aid': 0.00,
                    },
                    'other':
                    {
                        'total': 14477.95,
                        'trust_position': 0.00,
                        'gratification': 0.00,
                        'others_total': 14477.95,
                        'others':{
                            'Gratificação natalina': 0.00,
                            'Férias (1/3 constitucional)': 0.00,
                            'Abono de permanência': 0.00,
                            'AUXÍLIO-EDUCAÇÃO': 3248.25,
                            'INDENIZAÇÃO POR LICENÇA NÃO GOZADA': 11229.70,
                            'DEVOLUÇÃO FUNDO DE RESERVA': 0.00,
                            'DIFERENÇAS DE AUXÍLIOS': 0.00,
                            'PARCELAS PAGAS EM ATRASO': 0.00 ,
                        },
                    },
                },
                'discounts':
                {
                    'total': 11814.58,
                    'prev_contribution': 4716.47,
                    'ceil_retention':0.00,
                    'income_tax': 7098.11,
                }
        }
        files = [('./output_test/2020_04_MATIV.ods'),('./output_test/2020_04_Verbas Indenizatórias-MATIV.ods')]
        employees = parser.parse(files)

        #Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def teste_servidores_ativos_abr_2020(self):
        self.maxDiff = None

        expected = {
            'reg': '00002438',
            'name': 'ADAILDO MOREIRA DA SILVA',
            'role': 'TÉCNICO DO MP - ÁREA: INFORMÁTICA',
            'type': 'servidor',
            'workplace': 'COORDENADORIA DE ANÁLISES, DIAGNÓSTICOS E GEOPROCESSAMENTO',
            'active': True,
            'income':
                {
                    'total': 12631.81,
                    'wage': 10561.91,
                    'perks':{
                        'total': 2069.9,
                        'food':1230.00,
                        'health': 839.90,
                    },
                    'other':
                    {
                        'total': 0.00,
                        'trust_position': 0.00,
                        'gratification': 0.00,
                        'others_total': 0.00,
                        'others':{
                            'Gratificação natalina': 0.00,
                            'Férias (1/3 constitucional)': 0.00,
                            'Abono de permanência': 0.00,
                            'AUXÍLIO-ADOÇÃO': 0.00,
                            'AUXÍLIO-EDUCAÇÃO': 0.00,
                            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS': 0.00,
                            'DIFERENÇAS DE AUXÍLIOS': 0.00,
                            'PARCELAS PAGAS EM ATRASO': 0.00,
                        },
                    },
                },
                'discounts':
                {
                    'total': 3107.19,
                    'prev_contribution': 1478.66,
                    'ceil_retention': 0.00,
                    'income_tax': 1628.53,
                }
        }
        files = [('./output_test/2020_04_SATIV.ods'),('./output_test/2020_04_Verbas Indenizatórias-SATIV.ods')]
        employees = parser.parse(files)

        #Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)
    def teste_membros_ativos_maio_jul_2020(self):
        self.maxDiff = None
        expected = {
            'reg': '00002846',
            'name': 'ADRIANA SILVEIRA MANDARINO',
            'role': 'PROMOTOR DE JUSTICA',
            'workplace':'PROMOTORIA DE JUSTIÇA JUNTO À 3ª VARA CRIMINAL DE DUQUE DE CAXIAS',
            'type': 'membro',
            'active': True,
            'income':
                {
                    'total': 54473.59,
                    'wage': 33689.10,
                    'perks':{
                        'total': 5302.88,
                        'food': 1285.91,
                        'health': 4016.97 ,
                    },
                    'other':
                    {
                        'total': 15481.61,
                        'trust_position': 0.00,
                        'gratification': 1684.45 ,
                        'others_total': 13797.16,
                        'others':{
                            'Gratificação natalina': 0.00,
                            'Férias (1/3 constitucional)': 0.00,
                            'Abono de permanência': 0.00,
                            'AUXÍLIO-EDUCAÇÃO': 2567.46,
                            'INDENIZAÇÃO POR LICENÇA NÃO GOZADA': 11229.70,
                            'DEVOLUÇÃO FUNDO DE RESERVA': 0.00,
                            'DIFERENÇAS DE AUXÍLIOS': 0.00,
                            'PARCELAS PAGAS EM ATRASO': 0.00 ,
                        },
                    },
                },
                'discounts':
                {
                    'total': 12121.39,
                    'prev_contribution': 4716.47,
                    'ceil_retention':0.00,
                    'income_tax': 7404.92,
                }
        }
        files = [('./output_test/2020_05_MATIV.ods'),('./output_test/2020_05_Verbas Indenizatórias-MATIV.ods')]
        employees = parser.parse(files)

        #Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == '__main__':
    unittest.main()