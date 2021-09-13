import unittest
from parser import parse

class TestParser(unittest.TestCase):
    def test_membros_ativos_2020_01(self):
        self.maxDiff = None

        expected = {
            "reg": "10037",
            "name": "RICARDO JOSE FERREIRA",
            "role": "PROMOT DE JUST. ENTR. FINAL",
            "type": "membro",
            "workplace": "PJ DE MACAPA  -  FAMILIA 3S, ORFAOS, SUCE",
            "active": True,
            "income": {
                "total": 48591.51,
                "wage": 33689.11,
                "perks": {
                    "total": 5592.39,
                    "Food": 3368.91,
                    "Health": 2223.48,
                    "Vacation": 0.0,
                    "HousingAid": 0.0,
                    "PremiumLicensePecuniary": 0.0
                },
                "other": {
                    "total": 9310.01,
                    "trust_position": 5604.21,
                    "others_total": 3705.8,
                    "others": {
                        "Férias 1/3 constitucionais": 0.0,
                        "Gratificação Natalina": 0.0,
                        "Abono de Permanência": 3705.8,
                        "Abono Pecuniário": 0.0,
                        "Auxílio Doença": 0.0,
                        "Recesso Administrativo": 0.0,
                        "Diferença Indenizada": 0.0,
                        "Plantão indenizado": 0.0,
                        "Substituição": 0.0,
                        "Hora-Extra": 0.0,
                        "Plantão": 0.0,
                        "Diferença de Recebimentos": 0.0,
                        "Cumulação": 0.0,
                        "Devoluções de Descontos": 0.0
                    },
                    "gratification": 0.0
                }
            },
            "discounts": {
                "total": 13485.69,
                "prev_contribution": 3705.8,
                "ceil_retention": 0.0,
                "income_tax": 9779.89
            }
        }

        files = ['./output_test/2020-05-remuneracao-membros-ativos.csv',
         './output_test/2020-05-verbas-indenizatorias-membros-ativos.csv']
        employees = parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == '__main__':
    unittest.main()