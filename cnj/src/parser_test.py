import parser
import unittest
import json

class TestParser(unittest.TestCase):

    def test_jan_2018(self):
        self.maxDiff = None

        expected = {
            'reg': '',
            'name': 'ADRIANO CELSO GUIMARAES',
            'role': '',
            'type': 'membro',
            'workplace': '',
            'active': True,
            'income': {
                'total': 51906.08,
                'wage': 30471.11,
                'perks': {
                    'total': 6202.0,
                    'food': 1825.0,
                    'pre_school': 0.0,
                    'health': 0,
                    'birth_aid': 0,
                    'housing_aid': 4377.0,
                    'subsistence': 0.0
                },
                'other': {
                    'total': 15232.97,
                    'daily': 0.0,
                    'others_total': 15232.97,
                    'others': {
                        'Abono de permanência': 4342.92,
                        'ARTIGO 95, III da CF': 549.76,
                        'Abono constitucional de 1/3 de férias': 0.0,
                        'Indenização de férias': 0.0,
                        'Antecipação de férias': 0,
                        'Gratificação natalina': 0.0,
                        'Antecipação de gratificação natalina': 0.0,
                        'Substituição': 0.0,
                        'Gratificação por exercício cumulativo': 10340.29,
                        'Gratificação por encargo Curso/Concurso': 0,
                        'Pagamentos retroativos': 0.0,
                        'JETON': 0
                    }
                }
            },
            'discounts': {
                'total': 14687.56,
                'prev_contribution': 4342.92,
                'ceil_retention': 0.0,
                'income_tax': 7609.24,
                'others_total': 2735.4,
                'others': {
                    'Descontos Diversos': 2735.4
                }
            }
        }

        files = ('./src/output_test/TJRJ-contracheque.xlsx',
                './src/output_test/TJRJ-direitos-eventuais.xlsx',
                './src/output_test/TJRJ-direitos-pessoais.xlsx',
                './src/output_test/TJRJ-indenizações.xlsx')

        parser.parse('TJRJ', "2018", files, '/src/output_test', 'teste')
        with open('./src/output_test/TJRJ-1-2018.json') as json_file:
            data = json.load(json_file)
        employees = data['cr']['employees']

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_jan_2019(self):
        self.maxDiff = None

        expected = {
            'reg': '',
            'name': 'ADRIANO CELSO GUIMARAES',
            'role': '',
            'type': 'membro',
            'workplace': '',
            'active': True,
            'income': {
                'total': 55241.15,
                'wage': 35462.22,
                'perks': {
                    'total': 1825.0,
                    'food': 1825.0,
                    'pre_school': 0.0,
                    'health': 0,
                    'birth_aid': 0,
                    'housing_aid': 0.0,
                    'subsistence': 0.0
                },
                'other': {
                    'total': 17953.93,
                    'daily': 0.0,
                    'others_total': 17953.93,
                    'others': {
                        'Abono de permanência': 5054.28,
                        'ARTIGO 95, III da CF': 639.81,
                        'Abono constitucional de 1/3 de férias': 0.0,
                        'Indenização de férias': 0.0,
                        'Antecipação de férias': 0,
                        'Gratificação natalina': 0.0,
                        'Antecipação de gratificação natalina': 0.0,
                        'Substituição': 0.0,
                        'Gratificação por exercício cumulativo': 12259.84,
                        'Gratificação por encargo Curso/Concurso': 0,
                        'Pagamentos retroativos': 0.0,
                        'JETON': 0
                    }
                }
            },
            'discounts': {
                'total': 17620.29,
                'prev_contribution': 5054.28,
                'ceil_retention': 0.0,
                'income_tax': 9006.56,
                'others_total': 3559.45,
                'others': {
                    'Descontos Diversos': 3559.45
                }
            }
        }

        files = ('./src/output_test/TJRJ-contracheque.xlsx',
                './src/output_test/TJRJ-direitos-eventuais.xlsx',
                './src/output_test/TJRJ-direitos-pessoais.xlsx',
                './src/output_test/TJRJ-indenizações.xlsx')

        parser.parse('TJRJ', "2019", files, '/src/output_test', 'teste')
        with open('./src/output_test/TJRJ-1-2019.json') as json_file:
            data = json.load(json_file)
        employees = data['cr']['employees']

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

if __name__ == '__main__':
    unittest.main()