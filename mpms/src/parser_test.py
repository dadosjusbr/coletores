from parser import parse
import unittest

class TestParser(unittest.TestCase):
    def test_membros_ativos_2019_06(self):
        self.maxDiff = None

        expected = {
            "reg": "8000247",
            "name": "ANTONIO SIUFI NETO",
            "role": "PROCURADOR DE JUSTIÇA",
            "type": "membro",
            "workplace": "COLÉGIO DE PROCURADORES",
            "active": True,
            "income": {
                "total": 123300.91,
                "wage": 35462.22,
                "perks": {
                    "total": 52678.97
                },
                "other": {
                    "total": 35159.72,
                    "trust_position": 6792.79,
                    "others_total": 28366.93,
                    "others": {
                        "Férias 1/3 constitucionais": 28366.93,
                        "Gratificação Natalina": 0.0,
                        "Abono de Permanência": 0.0
                    },
                    "eventual_benefits": 0.0
                }
            },
            "discounts": {
                "total": 20998.82,
                "prev_contribution": 4789.51,
                "ceil_retention": 2961.69,
                "income_tax": 13247.62
            }
        }

        files = ['./output_test/remuneracao-2019-06.xlsx']
        employees = parse(files, '2019', '06')

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


    def test_membros_ativos_2019_07(self):
        self.maxDiff = None

        expected = {
            "reg": "8008493",
            "name": "ALEXANDRE MAGNO BENITES DE LACERDA",
            "role": "PROMOTOR DE JUSTIÇA",
            "type": "membro",
            "workplace": "PROMOTORES - CAMPO GRANDE",
            "active": True,
            "income": {
                "total": 94837.37,
                "wage": 33689.11,
                "perks": {
                    "total": 48501.13,
                    "Food": 2358.23,
                    "Health": 2358.23,
                    "Vacation": 11229.7,
                    "Transportation": 2358.24,
                    "Subsistence": 0.0,
                    "PremiumLicensePecuniary": 11481.31,
                    "VacationPecuniary": 18715.42,
                    "PreSchool": 0.0,
                    "HousingAid": 0.0
                },
                "other": {
                    "total": 12647.13,
                    "trust_position": 5161.41,
                    "others_total": 7485.72,
                    "others": {
                        "Férias 1/3 constitucionais": 7485.72,
                        "Gratificação Natalina": 0.0,
                        "Abono de Permanência": 0.0,
                        "Indenização de Substituição": 0.0,
                        "Compensação de Plantão": 0.0,
                        "Cumulações": 0.0
                    }
                }
            },
            "discounts": {
            "total": 11007.24,
            "prev_contribution": 4541.28,
            "ceil_retention": 0.0,
            "income_tax": 6465.96
            }
        }

        files = ['./output_test/remuneracao-2019-07.xlsx',
                 './output_test/indenizacao-2019-07.xlsx']

        employees = parse(files, '2021', '07')

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)



if __name__ == '__main__':
    unittest.main()