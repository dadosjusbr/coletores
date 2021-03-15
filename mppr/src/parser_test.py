import os
import parser
import unittest

class TestParser(unittest.TestCase):

    def test_membros_jan_2020(self):
        self.maxDiff = None

        expected = {
            'reg': 'ADAUTO SALVADOR REIS FACCO',
            'name': 'ADAUTO SALVADOR REIS FACCO',
            'role': 'PROMOTOR DE JUSTICA',
            'type': 'membro',
            'workplace': 'CURITIBA - 1a. VARA CIVEL',
            'active': True,
            'income': {
                'total': 44077.89,
                'wage': 33689.11,
                'perks': {
                    'total': 6352.49,
                    'food': 995.08 ,
                    'health': 979.68,
                    'pre_school': 0.00,
                    'housing_aid': 4377.73,
                },
                'other': {
                    'total': 7720.42,
                    'trust_position': 0.00,
                    'others_total': 4014.62,
                    'eventual_benefits': 3705.8,
                    'others': {
                        '13o. Salário': 308.82,
                        'Adicional de Férias': 0.00,
                        'Abono de permanência': 3705.8,
                        'Adicional Noturno': 0.00,
                        'Cursos': 0.00,
                        'Serviço Extraor': 0.00,
                        'Substituição de Função': 0.00,
                        'Cumulações': 0.00
                    },
            },
        },
            'discounts': {
                'total': 13152.81,
                'prev_contribution': 3705.8,
                'ceil_retention': 0.00,
                'income_tax': 9447.01,
            }
    }
        files = ('./output_test/2020_01_remu.ods',
                 './output_test/2020_01_vi.ods')
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)
    
    def test_membros_jan_2019(self):
        self.maxDiff = None

        expected = {
            'reg': 'ADAUTO SALVADOR REIS FACCO',
            'name': 'ADAUTO SALVADOR REIS FACCO',
            'role': 'PROMOTOR DE JUSTICA',
            'type': 'membro',
            'workplace': 'CURITIBA - 1a. VARA CIVEL',
            'active': True,
            'income': {
                'total': 37394.91,
                'wage': 33689.11,
                'perks': {
                    'total': 2044.99,
                    'food': 967.34 ,
                    'health': 1077.65,
                    'pre_school': 0.00,
                    'housing_aid': 0.00,
                },
                'other': {
                    'total': 3705.8,
                    'trust_position': 0.00,
                    'others_total': 3705.8,
                    'eventual_benefits': 0.00,
                    'others': {
                        '13o. Salário': 0.00,
                        'Adicional de Férias': 0.00,
                        'Abono de permanência': 3705.8,
                        'Adicional Noturno': 0.00,
                        'Cursos': 0.00,
                        'Serviço Extraor': 0.00,
                        'Substituição de Função': 0.00,
                        'Cumulações': 0.00
                    },
            },
        },
            'discounts': {
                'total': 12048.8,
                'prev_contribution': 3705.8,
                'ceil_retention': 0.00,
                'income_tax': 8343.00,
            }
    }
        files = ('./output_test/2019_01_remu.ods',
                 './output_test/2019_01_vi.ods')
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)
    


if __name__ == '__main__':
    unittest.main()