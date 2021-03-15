import os
import parser
import unittest

class TestParser(unittest.TestCase):

    def test_membros_jan_2020(self):
        self.maxDiff = None
        
        expected = {
            'reg': "2135",
            'name': "ABADIA NUNES PINTO",
            'role': "AUXILIAR DE SERVIÇOS JUDICIÁRIOS I",
            'type': 'membro',
            'workplace': "INATIVOS - NÃO APLICÁVEL",
            'active': True,
            "income":
            {
                'total': 7089.57,
                'wage': 7089.57,
                'perks':{
                    'total': 0.0,
                    'food': 0.0,
                    'pre_school': 0.0,
                },
                'other':
                { 
                    'total': 0.00,
                    'trust_position': 0.00,
                    'eventual_benefits': 0.00,
                    'others_total': 0.00,
                    'others': {
                        'Gratificação Natalina': 0.00,
                        'Férias (1/3 constitucional)': 0.00,
                        'Abono de permanência': 0.00,
                        'Verbas Rescisórias': 0.00,
                        'Licença-Prêmio': 0.00,
                        'Abono Pecuniário': 0.00,
                        'Outras Verbas Indenizatórias': 0.00,
                        'Adicional de Insalubridade/Periculosidade': 0.00,
                        'Gratificação Exercício Cumulativo': 0.00,
                        'Gratificação Exercício Natureza Especial': 0.00,
                        "Substituição": 0.00,
                        'Outras Remunerações Temporárias': 0.00,
                    }
                },

            },
            'discounts':
            {
                'total': 1288.21,
                'prev_contribution': 977.53,
                'ceil_retention': 0.00,
                'income_tax': 310.68,
            }
        }

        files = ('./output_test/2020_01_remu.csv',
                './output_test/2020_01_vi.csv')
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == '__main__':
    unittest.main()
