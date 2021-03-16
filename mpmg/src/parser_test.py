import os
import parser
import unittest


class TestParser(unittest.TestCase):
    def test_membros_ativos_backward_april20(self):
        self.maxDiff = None

        expected = {
            "reg": "293600",
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
            "./output_test/Membros ativos-01-2020.html",
            "./output_test/Membros ativos-Verbas Indenizatorias-01-2020.html",
        )
        employees = parser.parse("01", "2020", files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_ativos_forward_may20(self):
        self.maxDiff = None

        expected = {
            "reg": "152600",
            "name": "JULIANA MARIA RIBEIRO DA FONSECA SALOMAO",
            "role": "PROMOT.ENTRANC.ESPECIAL",
            "type": "membro",
            "workplace": "PARÁ DE MINAS - COMARCA; PARA DE MINAS-PJ-01PJ",
            "active": True,
            "income": {
                "total": 41899.37,
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
                        "Insalubridade 10%": 0.0,
                        "Gratificações": 0.0,
                    },
                },
                "perks": {
                    "total": 7695.57,
                    "food": 1100.0,
                    "pre_school": 0.0,
                    "transportation": 0.0,
                    "health": 980.72,
                    "indemnities": 5614.85,
                    "indemnities_diligences": 0.0,
                },
            },
            "discounts": {
                "total": 11081.85,
                "prev_contribution": 3705.8,
                "ceil_retention": 0.0,
                "income_tax": 7376.05,
                "discounts_others_total": 0.0,
            },
        }
        files = (
            "./output_test/Membros ativos-05-2020.html",
            "./output_test/Membros ativos-Verbas Indenizatorias-05-2020.html",
        )
        employees = parser.parse("05", "2020", files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_ativos_fev18(self):
        self.maxDiff = None

        expected = {
            "reg": "293600",
            "name": "ABELARDO GUIMARAES CASTRO",
            "role": "PROMOT.ENTRANC.ESPECIAL",
            "type": "membro",
            "workplace": "RIBEIRÃO DAS NEVES - COMARCA; RIBEIRAO DAS NEVES-PJ-07PJ",
            "active": True,
            "income": {
                "total": 34916.89,
                "wage": 28947.56,
                "other": {
                    "total": 707.6,
                    "trust_position": 0.0,
                    "others_total": 707.6,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Outras Remunerações Temporárias": 707.6,
                    },
                },
                "perks": {
                    "total": 5261.73,
                    "food": 884.0,
                    "pre_school": 0.0,
                    "transportation": 0.0,
                    "housing_aid": 4377.73,
                    "health": 0.0,
                },
            },
            "discounts": {
                "total": 9295.51,
                "prev_contribution": 3184.23,
                "ceil_retention": 0.0,
                "income_tax": 6111.28,
            },
        }
        files = (
            "./output_test/Membros ativos-02-2018.html",
            "./output_test/Membros ativos-Verbas Indenizatorias-02-2018.html",
        )
        employees = parser.parse("02", "2018", files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_ativos_backward_jan19(self):
        self.maxDiff = None

        expected = {
            "reg": "100600",
            "name": "DEL VECCHIO LIMA DOS SANTOS",
            "role": "PROMOTOR 2A ENTRANCIA",
            "type": "membro",
            "workplace": "DISPONIBILIDADE COMPULSORIA-COMARCA; DISPONIBILIDADE COMPULSORIA - UNIDADE",
            "active": True,
            "income": {
                "total": 36116.98,
                "wage": 21725.58,
                "other": {
                    "total": 14391.4,
                    "trust_position": 0.0,
                    "others_total": 14391.4,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Outras Remunerações Temporárias": 14391.4,
                    },
                },
                "perks": {
                    "total": 0.0,
                    "food": 0.0,
                    "pre_school": 0.0,
                    "transportation": 0.0,
                    "housing_aid": 0.0,
                    "health": 0.0,
                },
            },
            "discounts": {
                "total": 2785.81,
                "prev_contribution": 2389.81,
                "ceil_retention": 0.0,
                "income_tax": 396.0,
            },
        }
        files = (
            "./output_test/Membros ativos-01-2019.html",
            "./output_test/Membros ativos-Verbas Indenizatorias-01-2019.html",
        )
        employees = parser.parse("01", "2019", files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == "__main__":
    unittest.main()
