import os
import parser
import unittest

class TestParser(unittest.TestCase):

    def test_membros_jan_2020(self):
        self.maxDiff = None

        expected = {
            'reg': '1001',
            'name': 'ADELCION CALIMAN',
            'role': 'PROMOTOR DE JUSTIÇA',
            'type': 'membro',
            'workplace': 'PJ CRIMINAL DE VITÓRIA',
            'active': True,
            'income': {
                'total': 54239.47,
                'wage': 33689.11,
                'perks': {
                    'total': 3033.76,
                    'food': 2240.33,
                    'health': 793.43,
                },
                'other': {
                    'total': 20550.36,
                    'trust_position': 0.00,
                    'others_total': 20550.36,
                    'eventual_benefits': 0.00,
                    'others': {
                        'Gratificação Natalina': 0.00,
                        'Férias (1/3 constitucional)': 16844.56,
                        'Abono de permanência': 3705.8,
                        'ABONO  FÉR. IND. EX. ANT': 0.00,
                        'Plantão': 0.00,
                    },
            },
        },
            'discounts': {
                'total': 13305.27,
                'prev_contribution': 3705.8,
                'ceil_retention': 0.00,
                'income_tax': 9599.47,
            }
    }
        files = ('./output_test/2020_01_remu.xlsx',
                 './output_test/2020_01_vi.xlsx')
        employees = parser.parse(files,'2020','01')

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    #O propósito deste teste é verificar a execução para meses anteriores á ago/2019
    def test_membros_jan_2019(self):
        self.maxDiff = None

        expected = {
            'reg': 'ZENALDO BAPTISTA DE SOUSA',
            'name': 'ZENALDO BAPTISTA DE SOUSA',
            'role': 'PROMOTOR DE JUSTIÇA',
            'type': 'membro',
            'workplace': 'PJ DE CASTELO',
            'active': True,
            'income': {
                'total': 57054.85,
                'wage': 35710.46,
                'perks': {
                    'total': 0.00,
                },
                'other': {
                    'total': 21344.39,
                    'trust_position': 0.00,
                    'others_total': 21344.39,
                    'others': {
                        '13º VENCIMENTO': 0.00,
                        'Férias (1/3 constitucional)': 0.00,
                        'Abono de permanência': 0.00,
                        'VERBAS INDENIZATÓRIAS 1': 21344.39,
                        'VERBAS INDENIZATÓRIAS 2': 0.00,
                        'REMUNERAÇÃO TEMPORÁRIA 1': 0.00,
                        'REMUNERAÇÃO TEMPORÁRIA 2': 0.00,

                    },
            },
        },
            'discounts': {
                'total': 11637.72,
                'prev_contribution': 3705.8,
                'ceil_retention': 0.00,
                'income_tax': 7931.92,
            }
    }
        files = ('./output_test/2019_01_remu.xlsx',
                 './output_test/2019_01_vi.xlsx')
        employees = parser.parse(files,'2019','01')

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


    


if __name__ == '__main__':
    unittest.main()
