import os
import parser
import unittest


class TestParser(unittest.TestCase):
    def test_membros_ativos(self):
        self.maxDiff = None

        expected = {
            "reg": 293600,
            "name": "ABELARDO GUIMARAES CASTRO",
            "role": "PROMOT.ENTRANC.ESPECIAL",
            "type": "membro",
            "workplace": "BELO HORIZONTE - COMARCA; BH-01PJ FAZENDA PUBLICA EXEC FISCAIS",
            "active": True,
            "income": {
                "total": 37876.34,
                "wage": 33689.11,
                "other": {
                    "total": 514.69,
                    "trust_position": 0.0,
                    "others_total": 514.69,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Outras Remunerações Temporárias": 514.69,
                    },
                },
                "perks": {
                    "total": 3672.54,
                    "food": 1100.0,
                    "pre_school": 0.0,
                    "transportation": 0.0,
                    "housing_aid": 0.0,
                    "health": 2572.54,
                },
            },
            "discounts": {
                "total": 10977.58,
                "prev_contribution": 3705.8,
                "ceil_retention": 0.0,
                "income_tax": 7271.78,
            },
        }
        files = (
            "./output_test/Membros ativos-01-2020.xlsx",
            "./output_test/Membros ativos-Verbas Indenizatorias-01-2020.xlsx",
        )
        employees = parser.parse("01", "2020", files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_ativos(self):
        self.maxDiff = None

        expected = {
        }
        files = (
            "./output_test/Membros ativos-05-2020.xlsx",
            "./output_test/Membros ativos-Verbas Indenizatorias-05-2020.xlsx",
        )
        employees = parser.parse("05", "2020", files)
        print(employees)
        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == "__main__":
    unittest.main()
