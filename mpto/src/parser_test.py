import os
import parser
import unittest


class TestParser(unittest.TestCase):
    def test_membros_ativos_jan_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "32201",
            "name": "ABEL ANDRADE LEAL JUNIOR",
            "role": "01° PROMOTOR DE JUSTIÇA DE PORTO NACIONAL",
            "type": "membro",
            "workplace": "01ª PROMOTORIA DE JUSTIÇA DE PORTO NACIONAL",
            "active": true,
            "income": {
                "total": 37089.11,
                "wage": 33689.11,
                "perks": {
                    "food": 3400.0,
                    "housing_aid": 0.0,
                    "vacation": 0.0
                },
                "other": {
                    "total": 0.0,
                    "trust_position": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Outras Remunerações Temporárias": 0.0,
                        "Licença Prêmio Indenizada": 0.0,
                        "Programa de Aposentadoria Incentivada": 0.0,
                        "Verbas Rescisórias": 0.0,
                        "Cumulação": 0.0,
                        "Complemento por Entrância": 0.0
                    }
                }
            },
            "discounts": {
                "total": 11081.85,
                "prev_contribution": 3705.8,
                "ceil_retention": 0.0,
                "income_tax": 7376.05
            }
        }

        files = ("./output_test/Membros ativos-1-2020.ods",)
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)