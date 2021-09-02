import unittest
from parser import parse

class TestParser(unittest.TestCase):
    def test_membros_ativos_2020_01(self):
        self.maxDiff = None

        expected = {
            "reg": "20826",
            "name": "ANA BRIGIDA XANDER WESSEL",
            "role": "PROMOTOR(A) DE JUSTIÇA DE 3a",
            "type": "membro",
            "workplace": "3ª PMJ",
            "active": True,
            "income": {
                "total": 100690.29,
                "wage": 33689.11,
                "perks": {
                    "total": 1850.0,
                    "Food": 1000.0,
                    "Health": 600.0,
                    "Transportation": 0.0,
                    "Subsistence": 0.0,
                    "PreSchool": 0.0,
                    "HousingAid": 0.0
                },
                "other": {
                    "total": 65401.18,
                    "trust_position": 3376.0,
                    "others_total": 62025.18,
                    "others": {
                        "Férias 1/3 constitucionais": 37065.11,
                        "Gratificação Natalina": 0.0,
                        "Abono de Permanência": 0.0,
                        "Auxílio-Escola": 0.0,
                        "Auxílio-Odontológico": 250.0,
                        "Outros Auxílios": 0.0,
                        "Abonos": 24710.07,
                        "Adicionais": 0.0,
                        "Comissões": 0.0,
                        "Diferenças": 0.0,
                        "Indenizações": 0.0,
                        "Outras Remunerações": 0.0
                    },
                    "gratification": 0.0
                }
            },
            "discounts": {
                "total": 21944.4,
                "prev_contribution": 4548.02,
                "ceil_retention": 0.0,
                "income_tax": 17396.38
            }
        }

        files = ['./output_test/01-2020-remuneracao-membros-ativos.csv',
         './output_test/01-2020-verbas-indenizatorias-membros-ativos.csv']
        employees = parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == '__main__':
    unittest.main()