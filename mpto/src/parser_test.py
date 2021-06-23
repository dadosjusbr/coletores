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

    def test_membros_ativos_jun_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "32201", 
            "name": "ABEL ANDRADE LEAL JUNIOR", 
            "role": "01° PROMOTOR DE JUSTIÇA DE PORTO NACIONAL", 
            "type": "membro", 
            "workplace": "01ª PROMOTORIA DE JUSTIÇA DE PORTO NACIONAL", 
            "active": true, 
            "income": {
                "total": 68831.8, 
                "wage": 33689.11, 
                "perks": {
                    "food": 1200.0, 
                    "housing_aid": 0.0, 
                    "vacation": 0.0
                }, 
                "other": {
                    "total": 33942.69, 
                    "trust_position": 0.0, 
                    "others_total": 28074.26, 
                    "others": {
                        "Gratificação Natalina": 16844.56, 
                        "Férias (1/3 constitucional)": 11229.7, 
                        "Abono de Permanência": 0.0, 
                        "Outras Remunerações Temporárias": 5868.43, 
                        "Licença Prêmio Indenizada": 0.0, 
                        "Programa de Aposentadoria Incentivada": 0.0, 
                        "Cumulação": 5868.43, 
                        "Complemento por Entrância": 0.0
                    }
                }
            }, 
            "discounts": {
                "total": 15975.4, 
                "prev_contribution": 3705.8, 
                "ceil_retention": 264.22, 
                "income_tax": 12005.38
            }
        }

        files = ("./output_test/Membros ativos-6-2019.ods",)
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_ativos_apr_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "32201", 
            "name": "ABEL ANDRADE LEAL JUNIOR", 
            "role": "01° PROMOTOR DE JUSTIÇA DE PORTO NACIONAL", 
            "type": "membro", 
            "workplace": "01ª PROMOTORIA DE JUSTIÇA DE PORTO NACIONAL", 
            "active": true, 
            "income": {
                "total": 33689.11, 
                "wage": 33689.11, 
                "other": {
                    "total": 0.0, 
                    "trust_position": 0.0, 
                    "others_total": 0.0, 
                    "others": {
                        "Gratificação Natalina": 0.0, 
                        "Férias (1/3 constitucional)": 0.0, 
                        "Abono de Permanência": 0.0, 
                        "Licença Prêmio Indenizada": 0.0, 
                        "Cumulação": 6520.47, 
                        "Complemento por Entrância": 0.0
                    }
                }, 
                "perks": {
                    "food": 1200.0, 
                    "housing_aid": 0.0, 
                    "vacation": 0.0
                }
            }, 
            "discounts": {
                "total": 13539.27, 
                "prev_contribution": 3705.8, 
                "ceil_retention": 916.26, 
                "income_tax": 8917.21
            }
        }

        files = ("./output_test/Membros ativos-4-2019.ods",)
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_ativos_2018(self):
        self.maxDiff = None

        expected = {
            "reg": "32201",
            "name": "ABEL ANDRADE LEAL JUNIOR", 
            "role": "01° PROMOTOR DE JUSTIÇA DE PORTO NACIONAL", 
            "type": "membro", 
            "workplace": "01ª PROMOTORIA DE JUSTIÇA DE PORTO NACIONAL, 03ª PROMOTORIA DE JUSTIÇA DE PORTO NACIONAL", 
            "active": true, 
            "income": {
                "total": 30566.13, 
                "wage": 28947.55, 
                "other": {
                    "total": 1618.58, 
                    "trust_position": 0.0, 
                    "others_total": 1618.58, 
                    "others": {
                        "Gratificação Natalina": 0.0, 
                        "Férias (1/3 constitucional)": 1618.58, 
                        "Abono de Permanência": 0.0, 
                        "Licença Prêmio Indenizada": 0.0, 
                        "Cumulação": 4855.72, 
                        "Complemento por Entrância": 0.0
                    }
                }, 
                "perks": {
                    "food": 2400.0, 
                    "housing_aid": 4377.73, 
                    "vacation": 28947.55
                }
            }, 
            "discounts": {
               "total": 11209.41, 
               "prev_contribution": 3184.23, 
               "ceil_retention": 40.27, 
               "income_tax": 7984.91
            }
        }


        files = ("./output_test/Membros ativos-8-2018.ods",)
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)