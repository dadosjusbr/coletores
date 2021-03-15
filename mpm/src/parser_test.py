import os
import parser
import unittest


class TestParser(unittest.TestCase):

    def test_membros_ativos(self):
        self.maxDiff = None

        expected = {
            'reg': '1191-6',
            'name': 'ADILSON JOSE GUTIERREZ',
            'role': 'PROMOTOR DE JUSTICA MILITAR',
            'type': 'membro',
            'workplace': '1ª PROCURADORIA DE JUSTIÇA MILITAR EM SÃO PAULO/SP',
            'active': True,
            'income': {
                'total': 66379.24,
                'wage': 33689.11,
                'perks': {
                    'total': 910.08,
                    'food': 910.08,
                    'transportation': 0,
                    'birth_aid': 0,
                    'housing_aid': 0
                },
                'other': {
                    'total': 31780.05,
                    'trust_position': 0,
                    'others_total': 31780.05,
                    'others': {
                        'Gratificação Natalina': 16844.55,
                        'Férias (1/3 constitucional)': 11229.70,
                        'Abono de Permanência': 3705.80,
                        'GRAT ENCARGO CURSO OU CONCURSO': 0,
                        'INSALUBRIDADE 10%': 0,
                        'ATIVIDADE PENOSA': 0,
                        'SUBSTITUIÇÃO FC/CC': 0,
                        'GECO': 0,
                    }}
            },
            'discounts': {
                'total': 14319.74,
                'prev_contribution': 3705.8,
                'ceil_retention': 0,
                'income_tax': 10613.94
            }
        }

        files = ('./output_test/Membros ativos-1-2020.xlsx',
                 './output_test/Membros ativos-Verbas Indenizatorias-1-2020.xlsx')
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_inativos(self):
        self.maxDiff = None

        expected = {
            'reg': '0004-3',
            'name': 'ANETE VASCONCELOS DE BORBOREMA',
            'role': 'SUBPROCURADOR-GERAL DA JUSTIÇA MILITAR',
            'type': 'membro',
            'workplace': 'APOSENTADOS/INATIVOS',
            'active': False,
            'income': {
                'total': 55992.97,
                'wage': 37328.65,
                'perks': {
                    'total': 0,
                    'food': 0,
                    'transportation': 0,
                    'birth_aid': 0,
                    'housing_aid': 0,
                },
                'other': {
                    'total': 18664.32,
                    'trust_position': 0,
                    'others_total': 18664.32,
                    'others': {
                        'Gratificação Natalina': 18664.32,
                        'Férias (1/3 constitucional)': 0,
                        'Abono de Permanência': 0,
                        'GRAT ENCARGO CURSO OU CONCURSO': 0,
                        'INSALUBRIDADE 10%': 0,
                        'ATIVIDADE PENOSA': 0,
                        'SUBSTITUIÇÃO FC/CC': 0,
                        'GECO': 0,
                    }}
            },
            'discounts': {
                'total': 11362.42,
                'prev_contribution': 3434.48,
                'ceil_retention': 0,
                'income_tax': 7927.94,
            }
        }

        files = ('./output_test/Membros inativos-1-2020.xlsx',
                 './output_test/Membros inativos-Verbas Indenizatorias-1-2020.xlsx')
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_servidores_ativos(self):
        self.maxDiff = None

        expected = {
            'reg': '0376-0',
            'name': 'ABEL DA COSTA VALE NETO',
            'role': 'TECNICO DO MPU/ADMINISTRAÇÃO',
            'type': 'servidor',
            'workplace': 'COORDENADORIA ADMINISTRATIVA DO PLAN-ASSISTE',
            'active': True,
            'income': {
                'total': 31685.71,
                'wage': 12229.5,
                'perks': {
                    'total': 1395.01,
                    'food': 910.08,
                    'transportation': 484.93,
                    'birth_aid': 0,
                    'housing_aid': 0,
                },
                'other': {
                    'total': 18061.2,
                    'trust_position': 3563.93,
                    'others_total': 14497.27,
                    'others': {
                        'Gratificação Natalina': 7777.98,
                        'Férias (1/3 constitucional)': 5185.32,
                        'Abono de Permanência': 0,
                        'GRAT ENCARGO CURSO OU CONCURSO': 0,
                        'INSALUBRIDADE 10%': 0,
                        'ATIVIDADE PENOSA': 0,
                        'SUBSTITUIÇÃO FC/CC': 1533.97,
                        'GECO': 0,
                    }}
            },
            'discounts': {
                'total': 4452.77,
                'prev_contribution': 1319.12,
                'ceil_retention': 0,
                'income_tax': 3133.65
            }
        }

        files = ('./output_test/Servidores ativos-1-2020.xlsx',
                 './output_test/Servidores ativos-Verbas Indenizatorias-1-2020.xlsx')
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_servidores_inativos(self):
        self.maxDiff = None

        expected = {
            'reg': '1103-7',
            'name': 'ALBA REGINA BITENCOURT PEREIRA',
            'role': 'TECNICO DO MPU/ADMINISTRAÇÃO',
            'type': 'servidor',
            'workplace': 'APOSENTADOS/INATIVOS',
            'active': False,
            'income': {
                'total': 18463.75,
                'wage': 12309.17,
                'perks': {
                    'total': 0,
                    'food': 0,
                    'transportation': 0,
                    'birth_aid': 0,
                    'housing_aid': 0
                },
                'other': {
                    'total': 6154.58,
                    'trust_position': 0,
                    'others_total': 6154.58,
                    'others': {
                        'Gratificação Natalina': 6154.58,
                        'Férias (1/3 constitucional)': 0,
                        'Abono de Permanência': 0,
                        'GRAT ENCARGO CURSO OU CONCURSO': 0,
                        'INSALUBRIDADE 10%': 0,
                        'ATIVIDADE PENOSA': 0,
                        'SUBSTITUIÇÃO FC/CC': 0,
                        'GECO': 0,
                    }}
            },
            'discounts': {
                'total': 3010.35,
                'prev_contribution': 682.33,
                'ceil_retention': 0,
                'income_tax': 2328.02
            }
        }

        files = ('./output_test/Servidores inativos-1-2020.xlsx',
                 './output_test/Servidores inativos-Verbas Indenizatorias-1-2020.xlsx')
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_pensionistas(self):
        self.maxDiff = None

        expected = {
            'reg': '1522-9',
            'name': 'ABRAAO ANTONIO XAVIER DINIZ',
            'role': 'PENSÃO CIVIL',
            'type': 'pensionista',
            'workplace': 'PENSÃO ESPECIAL',
            'active': False,
            'income':                     {
                'total': 4237.79,
                'wage': 2860.13,
                'perks': {
                    'total': 0,
                    'food': 0,
                    'transportation': 0,
                    'birth_aid': 0,
                    'housing_aid': 0
                },
                'other': {
                    'total': 1377.66,
                    'trust_position': 0,
                    'others_total': 1377.66,
                    'others': {
                        'Gratificação Natalina': 1377.66,
                        'Férias (1/3 constitucional)': 0,
                        'Abono de Permanência': 0,
                        'GRAT ENCARGO CURSO OU CONCURSO': 0,
                        'INSALUBRIDADE 10%': 0,
                        'ATIVIDADE PENOSA': 0,
                        'SUBSTITUIÇÃO FC/CC': 0,
                        'GECO': 0,
                    }}
            },
            'discounts': {
                'total': 207.4,
                'prev_contribution': 146.7,
                'ceil_retention': 0,
                'income_tax': 60.7
            }
        }

        files = ('./output_test/Pensionistas-1-2020.xlsx',
                 './output_test/Pensionistas-Verbas Indenizatorias-1-2020.xlsx')
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_colaboradores(self):
        self.maxDiff = None

        expected = {
            'reg': '7822-1',
            'name': 'ANA VICTÓRIA DE PAULA SANTOS GUIMARÃES',
            'role': 'ESTAGIÁRIO',
            'type': 'colaborador',
            'workplace': '5ª PROCURADORIA DE JUSTIÇA MILITAR NO RIO DE JANEIRO/RJ',
            'active': True,
            'income': {
                'total': 983,
                'wage': 850,
                'perks': {
                    'total': 133,
                    'food': 0,
                    'transportation': 133,
                    'birth_aid': 0,
                    'housing_aid': 0
                },
                'other': {
                    'total': 0,
                    'trust_position': 0,
                    'others_total': 0,
                    'others': {
                        'Gratificação Natalina': 0,
                        'Férias (1/3 constitucional)': 0,
                        'Abono de Permanência': 0,
                        'GRAT ENCARGO CURSO OU CONCURSO': 0,
                        'INSALUBRIDADE 10%': 0,
                        'ATIVIDADE PENOSA': 0,
                        'SUBSTITUIÇÃO FC/CC': 0,
                        'GECO': 0,
                    }}
            },
            'discounts': {
                'total': 0,
                'prev_contribution': 0,
                'ceil_retention': 0,
                'income_tax': 0
            }
        }

        files = ('./output_test/Colaboradores-1-2020.xlsx',
                 './output_test/Colaboradores-Verbas Indenizatorias-1-2020.xlsx')
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == '__main__':
    unittest.main()
