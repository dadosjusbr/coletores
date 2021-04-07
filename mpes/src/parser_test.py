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
    


if __name__ == '__main__':
    unittest.main()
