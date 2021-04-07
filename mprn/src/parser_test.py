import os
import parser
import unittest


class TestParser(unittest.TestCase):
    def test_membros_ativos_jan_2018(self):
        self.maxDiff = None

        expected = {
            "reg": "1993178",
            "name": "ADRIANA LIRA DA LUZ MELLO",
            "role": "PROMOTOR DE 3a ENTRANCIA",
            "type": "membro",
            "workplace": "Não informado",
            "active": True,
            "income": {
                "total": 35956.78,
                "wage": 29679.05,
                "perks": {"total": 6277.73},
                "other": {
                    "total": 0.0,
                    "trust_position": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Outras Remunerações Temporárias": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 10374.24,
                "prev_contribution": 3184.23,
                "ceil_retention": 0.0,
                "income_tax": 6312.44,
                "discounts_others_total": 877.57,
                "others_total": 877.57,
                "others": {"Descontos Diversos": 877.57},
            },
        }

        files = ("./output_test/Membros ativos-1-2018.ods",)
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_ativos_fev_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "1571940",
            "name": "ADRIANA MELO DINIZ",
            "role": "PROMOTOR DE 3a ENTRANCIA",
            "type": "membro",
            "workplace": "53ª  PROMOTORIA DE JUSTIÇA - NATAL",
            "active": True,
            "income": {
                "total": 43319.29,
                "wage": 38586.27,
                "perks": {
                    "total": 2200.0,
                    "health": 800.0,
                    "food": 1400.0,
                    "housing_aid": 0.0,
                },
                "other": {
                    "total": 2533.02,
                    "trust_position": 0.0,
                    "others_total": 2533.02,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Outras Remunerações Temporárias": 0.0,
                        "Substituição Cargo C. Função GAE": 0.0,
                        "Adicional Periculosidade": 0.0,
                        "Licença Compensatória": 2533.02,
                    },
                },
            },
            "discounts": {
                "total": 12768.04,
                "prev_contribution": 3705.8,
                "ceil_retention": 0.0,
                "income_tax": 7271.78,
                "discounts_others_total": 1790.46,
                "others_total": 1790.46,
                "others": {"Descontos Diversos": 1790.46},
            },
        }

        files = (
            "./output_test/Membros ativos-2-2020.ods",
            "./output_test/Membros ativos-Verbas Indenizatorias-2-2020.ods",
        )
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == "__main__":
    unittest.main()
