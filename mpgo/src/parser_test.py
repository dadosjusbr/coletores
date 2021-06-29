import os
import parser
import unittest


class TestParser(unittest.TestCase):
    def test_membros_jan_2018(self):
        self.maxDiff = None

        expected = {
            "reg": "4405.0",
            "name": "ABRAO AMISY NETO",
            "role": "PROCURADOR DE JUSTICA/COORDENADOR DE PROCURADORIA DE JUSTIÇA",
            "type": "membro",
            "workplace": "18ª PROCURADORIA DE JUSTIÇA",
            "active": True,
            "income": {
                "total": 48374.75,
                "wage": 35462.22,
                "perks": {"total": 1210.0},
                "other": {
                    "total": 11702.53,
                    "trust_position": 6383.2,
                    "others_total": 5319.33,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de permanência": 0.0,
                        "Outras RemuneraçõesTemporárias": 5319.33,
                    },
                },
            },
            "discounts": {
                "total": 21419.28,
                "prev_contribution": 5053.36,
                "ceil_retention": 7871.43,
                "income_tax": 8494.49,
            },
        }

        files = ("./output_test/2018_01_remu.csv", "./output_test/2018_01_vi.csv")
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_fev_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "4529.0",
            "name": "WAGNER DE PINA CABRAL",
            "role": "PROMOTOR DE JUSTICA DE 3A. ENTRÂNCIA",
            "type": "membro",
            "workplace": "3ª PROMOTORIA DE JUSTIÇA DA COMARCA DE RIO VERDE",
            "active": True,
            "income": {
                "total": 59675.95,
                "wage": 33689.11,
                "other": {
                    "total": 24826.84,
                    "trust_position": 0.0,
                    "others_total": 24826.84,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de permanência": 4800.69,
                        "Verbas Rescisórias": 0.0,
                        "Abono Pecuniário": 14972.79,
                        "Outras Verbas Indenizatórias": 0.0,
                        "Adicional de Insalubridade/Periculosidade": 0.0,
                        "Gratificação Exercício Cumulativo": 5053.36,
                        "Gratificação Exercício Natureza Especial": 0.0,
                        "Substituição": 0.0,
                        "Outras Remunerações Temporárias": 0.0,
                    },
                },
                "perks": {
                    "total": 1160.0,
                    "food": 1160.0,
                    "pre_school": 0.0,
                    "premium_license_pecuniary": 0.0,
                },
            },
            "discounts": {
                "total": 14533.37,
                "prev_contribution": 4800.69,
                "ceil_retention": 0.0,
                "income_tax": 9732.68,
            },
        }

        files = ("./output_test/2020_02_remu.csv", "./output_test/2020_02_vi.csv")
        employees = parser.parse(files)
        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == "__main__":
    unittest.main()
