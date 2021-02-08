import parser
import unittest

class TestParser(unittest.TestCase):
    # Membros ativos sem folha complementar e de 13º
    def test_membros_ativos(self):
        self.maxDiff = None

        expected = {
            'reg': '3418723',
            'name': 'ADONIRAN LEMOS ALMEIDA FILHO',
            'role': 'PROMOTOR DE JUSTICA DE ENTRÂNCIA INICIAL',
            'type': 'membro',
            'workplace': 'PROMOTORIA DE JUSTIÇA DE PINHEIRO MACHADO',
            'active': True,
            'income': {
                'total': 25851.96,
                'wage': 25851.96,
                'perks': {
                    'total': 0.0
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 9094.28,
                'prev_contribution': 4008.95,
                'ceil_retention': 0.0,
                'income_tax': 5085.33
            }
        }

        files = ("./output_test/M-NORMAL-12-2020.json",)
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # Membros ativos com folha complementar
    def test_membros_ativos_complementar(self):
        self.maxDiff = None

        expected = {
            'reg': '3418723',
            'name': 'ADONIRAN LEMOS ALMEIDA FILHO',
            'role': 'PROMOTOR DE JUSTICA DE ENTRÂNCIA INICIAL',
            'type': 'membro',
            'workplace': 'PROMOTORIA DE JUSTIÇA DE PINHEIRO MACHADO',
            'active': True,
            'income': {
                'total': 51703.92,
                'wage': 25851.96,
                'perks': {
                    'total': 25851.96
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 9094.28,
                'prev_contribution': 4008.95,
                'ceil_retention': 0.0,
                'income_tax': 5085.33
            }
        }

        files = ("./output_test/M-NORMAL-12-2020.json", 
                 "./output_test/M-COMPLEMENTAR-12-2020.json")
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # Membros ativos com folha complementar e 13º
    def test_membros_ativos_complementar(self):
        self.maxDiff = None

        expected = {
            'reg': '3418723',
            'name': 'ADONIRAN LEMOS ALMEIDA FILHO',
            'role': 'PROMOTOR DE JUSTICA DE ENTRÂNCIA INICIAL',
            'type': 'membro',
            'workplace': 'PROMOTORIA DE JUSTIÇA DE PINHEIRO MACHADO',
            'active': True,
            'income': {
                'total': 77555.88,
                'wage': 51703.92,
                'perks': {
                    'total': 25851.96
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 18188.56,
                'prev_contribution': 8017.9,
                'ceil_retention': 0.0,
                'income_tax': 10170.66
            }
        }

        files = ("./output_test/M-NORMAL-12-2020.json", 
                 "./output_test/M-COMPLEMENTAR-12-2020.json",
                 "./output_test/M-13-12-2020.json")
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

if __name__ == '__main__':
    unittest.main()
