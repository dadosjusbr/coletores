import os
import parser
import unittest
import pathlib
import numpy as np

class TestParser(unittest.TestCase):

    def test_membros_ativos(self):
        self.maxDiff = None

        expected = {
            'reg': 02003042.0 ,
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
            'reg': 00179515.0,
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
            'reg': 00003189.0,
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
            'reg': 00001322.0,
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
            'reg': 00004938.0,
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

    def teste_servidores_ativos_outubro_2020(self):
        self.maxDiff = None

        expected = {
            'reg': 00198219.0,
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

if __name__ == '__main__':
    unittest.main()
