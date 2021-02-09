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
                'total': 24172.19,
                'wage': 25851.96,
                'perks': {
                    'total': 620.51
                },
                'other': {
                    'total': -2300.28,
                    'trust_position': 0.0,
                    'others_total': -2300.28,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0,
                        'Outras remunerações temporárias': -2300.28
                    }
                }
            },
            'discounts': {
                'total': 8253.96,
                'prev_contribution': 4008.95,
                'ceil_retention': 0.0,
                'income_tax': 4245.01
            }
        }

        second_expected = {
            'reg': '3427811',
            'name': 'BRUNO HERINGER JUNIOR', 
            'role': 'PROMOTOR DE JUSTICA DE ENTRÂNCIA FINAL', 
            'type': 'membro', 
            'workplace': 'SUBPROCURADORIA-GERAL DE JUSTIÇA PARA ASSUNTOS JURÍDICOS', 
            'active': True, 
            'income': {
                'total': 39563.9, 
                'wage': 31916.0, 
                'perks': {
                    'total': 910.08
                }, 
                'other': {
                    'total': 6737.82, 
                    'trust_position': 3191.6, 
                    'others_total': 3546.22, 
                    'others': {
                        'Gratificação Natalina': 0.0, 
                        'Férias (1/3 constitucional)': 3546.22, 
                        'Abono de Permanência': 0.0,
                        'Outras remunerações temporárias': 0.0
                    }
                }
            }, 
            'discounts': {
                'total': 12632.88, 
                'prev_contribution': 5161.11, 
                'ceil_retention': 0.0, 
                'income_tax': 7471.77
            }
        }

        files = ("./output_test/M-NORMAL-12-2020.json",)
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(2, len(employees))
        self.assertDictEqual(employees[0], expected)
        self.assertDictEqual(employees[1], second_expected)

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
                'total': 50024.149999999994,
                'wage': 25851.96,
                'perks': {
                    'total': 26472.469999999998
                },
                'other': {
                    'total': -2300.28,
                    'trust_position': 0.0,
                    'others_total': -2300.28,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0,
                        'Outras remunerações temporárias': -2300.28
                    }
                }
            },
            'discounts': {
                'total': 8253.96,
                'prev_contribution': 4008.95,
                'ceil_retention': 0.0,
                'income_tax': 4245.01
            }
        }

        second_expected = {
            'reg': '3427811',
            'name': 'BRUNO HERINGER JUNIOR', 
            'role': 'PROMOTOR DE JUSTICA DE ENTRÂNCIA FINAL', 
            'type': 'membro', 
            'workplace': 'SUBPROCURADORIA-GERAL DE JUSTIÇA PARA ASSUNTOS JURÍDICOS', 
            'active': True, 
            'income': {
                'total': 75167.97, 
                'wage': 31916.0, 
                'perks': {
                    'total': 36514.15
                }, 
                'other': {
                    'total': 6737.82, 
                    'trust_position': 3191.6, 
                    'others_total': 3546.22, 
                    'others': {
                        'Gratificação Natalina': 0.0, 
                        'Férias (1/3 constitucional)': 3546.22, 
                        'Abono de Permanência': 0.0,
                        'Outras remunerações temporárias': 0.0
                    }
                }
            }, 
            'discounts': {
                'total': 12632.88, 
                'prev_contribution': 5161.11, 
                'ceil_retention': 0.0, 
                'income_tax': 7471.77
            }
        }

        files = ("./output_test/M-NORMAL-12-2020.json", 
                 "./output_test/M-COMPLEMENTAR-12-2020.json")
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(2, len(employees))
        self.assertDictEqual(employees[0], expected)
        self.assertDictEqual(employees[1], second_expected)

    # Membros ativos com folha complementar e 13º
    def test_membros_ativos_decimo(self):
        self.maxDiff = None

        expected = {
            'reg': '3418723',
            'name': 'ADONIRAN LEMOS ALMEIDA FILHO',
            'role': 'PROMOTOR DE JUSTICA DE ENTRÂNCIA INICIAL',
            'type': 'membro',
            'workplace': 'PROMOTORIA DE JUSTIÇA DE PINHEIRO MACHADO',
            'active': True,
            'income': {
                'total': 75876.10999999999,
                'wage': 51703.92,
                'perks': {
                    'total': 26472.469999999998
                },
                'other': {
                    'total': -2300.28,
                    'trust_position': 0.0,
                    'others_total': -2300.28,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0,
                        'Outras remunerações temporárias': -2300.28
                    }
                }
            },
            'discounts': {
                'total': 17348.239999999998,
                'prev_contribution': 8017.9,
                'ceil_retention': 0.0,
                'income_tax': 9330.34
            }
        }

        second_expected = {
            'reg': '3427811',
            'name': 'BRUNO HERINGER JUNIOR', 
            'role': 'PROMOTOR DE JUSTICA DE ENTRÂNCIA FINAL', 
            'type': 'membro', 
            'workplace': 'SUBPROCURADORIA-GERAL DE JUSTIÇA PARA ASSUNTOS JURÍDICOS', 
            'active': True, 
            'income': {
                'total': 110275.57, 
                'wage': 63832.0, 
                'perks': {
                    'total': 36514.15
                }, 
                'other': {
                    'total': 9929.42, 
                    'trust_position': 6383.2, 
                    'others_total': 3546.22, 
                    'others': {
                        'Gratificação Natalina': 0.0, 
                        'Férias (1/3 constitucional)': 3546.22, 
                        'Abono de Permanência': 0.0,
                        'Outras remunerações temporárias': 0.0
                    }
                }
            }, 
            'discounts': {
                'total': 25159.92, 
                'prev_contribution': 10322.23, 
                'ceil_retention': 0.0, 
                'income_tax': 14837.69
            }
        }

        files = ("./output_test/M-NORMAL-12-2020.json", 
                 "./output_test/M-COMPLEMENTAR-12-2020.json",
                 "./output_test/M-13-12-2020.json")
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(2, len(employees))
        self.assertDictEqual(employees[0], expected)
        self.assertDictEqual(employees[1], second_expected)

if __name__ == '__main__':
    unittest.main()
