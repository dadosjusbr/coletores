import os
import parser
import parser_2018
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
            "active": True,
            "income": {
                "total": 37089.11,
                "wage": 33689.11,
                "perks": {
                    "total": 3400.0,
                    "food": 3400.0,
                    "housing_aid": 0.0,
                    "vacation": 0.0,
                },
                "other": {
                    "total": 0.0,
                    "trust_position": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Licença Prêmio Indenizada": 0.0,
                        "Programa de Aposentadoria Incentivada": 0.0,
                        "Verbas Rescisórias": 0.0,
                        "Cumulação": 0.0,
                        "Complemento por Entrância": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 11081.85,
                "prev_contribution": 3705.8,
                "ceil_retention": 0.0,
                "income_tax": 7376.05,
            },
        }

        files = (
            "./output_test/Membros ativos-01-2020.ods",
            "./output_test/Membros ativos-Verbas Indenizatorias-01-2020.ods",
        )
        employees = parser.parse(files, "2019", "1")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_ativos_jun_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "51604",
            "name": "DIEGO NARDO",
            "role": "06° PROMOTOR DE JUSTIÇA DE PORTO NACIONAL",
            "type": "membro",
            "workplace": "06ª PROMOTORIA DE JUSTIÇA DE PORTO NACIONAL",
            "active": True,
            "income": {
                "total": 60244.6,
                "wage": 33689.11,
                "perks": {
                    "total": 1200.0,
                    "food": 1200.0,
                    "housing_aid": 0.0,
                    "vacation": 0.0,
                },
                "other": {
                    "total": 25355.49,
                    "trust_position": 0.0,
                    "others_total": 25355.49,
                    "others": {
                        "Gratificação Natalina": 16844.56,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Licença Prêmio Indenizada": 0.0,
                        "Programa de Aposentadoria Incentivada": 0.0,
                        "Cumulação": 6737.82,
                        "Complemento por Entrância": 1773.11,
                    },
                },
            },
            "discounts": {
                "total": 15618.99,
                "prev_contribution": 3900.84,
                "ceil_retention": 2906.72,
                "income_tax": 8811.43,
            },
        }

        files = (
            "./output_test/Membros ativos-06-2019.ods",
            "./output_test/Membros ativos-Verbas Indenizatorias-06-2019.ods",
        )
        employees = parser.parse(files, "2019", "06")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_ativos_apr_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "16097",
            "name": "FRANCISCO RODRIGUES DE SOUZA FILHO",
            "role": "17° PROMOTOR DE JUSTIÇA DA CAPITAL",
            "type": "membro",
            "workplace": "17ª PROMOTORIA DE JUSTIÇA DA CAPITAL",
            "active": True,
            "income": {
                "total": 43400.04,
                "wage": 33689.11,
                "other": {
                    "total": 8510.93,
                    "trust_position": 0.0,
                    "others_total": 8510.93,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Licença Prêmio Indenizada": 0.0,
                        "Cumulação": 6737.82,
                        "Complemento por Entrância": 1773.11,
                    },
                },
                "perks": {
                    "total": 1200.0,
                    "food": 1200.0,
                    "housing_aid": 0.0,
                    "vacation": 0.0,
                },
            },
            "discounts": {
                "total": 14754.34,
                "prev_contribution": 3900.84,
                "ceil_retention": 2906.72,
                "income_tax": 7946.78,
            },
        }

        files = (
            "./output_test/Membros ativos-04-2019.ods",
            "./output_test/Membros ativos-Verbas Indenizatorias-04-2019.ods",
        )
        employees = parser.parse(files, "2019", "04")
        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_ativos_2018(self):
        self.maxDiff = None

        expected = {
            "reg": "6991",
            "name": "BEATRIZ REGINA LIMA DE MELLO",
            "role": "16° PROMOTOR DE JUSTIÇA DA CAPITAL",
            "type": "membro",
            "workplace": "09ª PROCURADORIA DE JUSTIÇA, 16ª PROMOTORIA DE JUSTIÇA DA CAPITAL",
            "active": True,
            "income": {
                "total": 31385.24,
                "wage": 28947.55,
                "other": {
                    "total": 9750.76,
                    "trust_position": 0.0,
                    "others_total": 9750.76,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 2437.69,
                        "Abono de Permanência": 0.0,
                        "Licença Prêmio Indenizada": 0.0,
                        "Cumulação": 5789.51,
                        "Complemento por Entrância": 1523.56,
                    },
                },
                "perks": {
                    "total": 35725.28,
                    "food": 2400.0,
                    "housing_aid": 4377.73,
                    "vacation": 28947.55,
                },
            },
            "discounts": {
                "total": 12964.45,
                "prev_contribution": 3351.82,
                "ceil_retention": 2497.62,
                "income_tax": 7115.01,
            },
        }

        files = (
            "./output_test/Membros ativos-08-2018.ods",
            "./output_test/Membros ativos-Verbas Indenizatorias-08-2018.ods",
        )
        employees = parser_2018.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == "__main__":
    unittest.main()
