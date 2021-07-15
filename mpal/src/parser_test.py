import parser
import unittest

class TestParser(unittest.TestCase):

    def membros_ativos_6_2021(self):
        self.maxDiff = None

        expected = {
            'reg': 'ADEZIA LIMA DE CARVALHO',
            'name': 'ADEZIA LIMA DE CARVALHO',
            'role': 'PROMOTOR DE 3ª',
            'type': 'membro',
            'workplace': 'PROMOTORES DE JUSTICA',
            'active': True,
            'income': {
                'total': 33689.16,
                'wage': 0.0,
                'perks': {
                    'total': 0.0
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 33689.16,
                    'others': {
                        'Gratigicação natalina': 33689.16,
                        'Vacation': 0.0,
                        'Abono de permanência': 0.0,
                        'Outras Remunerações Temporárias': 0.0
                    }
                }
            },
            'discounts': {
                'total': 11814.61,
                'prev_contribution': 4716.48,
                'ceil_retention': 0.0,
                'income_tax': 7098.13
            }
        }

        file = './output_test/membros_ativos-6-2021.json'
        employees = parser.parse(file)
        print(employees)
        #Verificações
        self.assertEqual(1, len(employees))

        self.assertDictEqual(employees[0], expected)

if __name__ == '__main__':
    unittest.main()
