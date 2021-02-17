import os
import parser
import unittest


class TestParser(unittest.TestCase):

    # Tests for parsers for the months from July 2019 to November 2020
    def test_membros_ativos_jan_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "3725",
            "name": "ABNER CASTORINO",
            "role": "PROMOTOR DE JUSTICA (ENTRANCIA FINAL)",
            "type": "membro",
            "workplace": "PROMOTORIA DE JUSTICA DE SAO BERNARDO DO CAMPO",
            "active": True,
            "income": {
                "total": 40253.32,
                "wage": 33689.1,
                "perks": {
                    "total": 960.0,
                    "food": 960.0,
                    "vacation_pecuniary": 0.0,
                    "premium_license_pecuniary": 0.0,
                },
                "other": {
                    "total": 5604.22,
                    "trust_position": 0.0,
                    "others_total": 5604.22,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "GRAT. CUMULATIVA": 5604.22,
                        "GRAT. NATUREZA ESPECIAL": 0.0,
                        "GRAT. DE GRUPO DE ATUAÇÃO ESPECIAL": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 12623.0,
                "prev_contribution": 3705.8,
                "ceil_retention": 0.0,
                "income_tax": 8917.2,
            },
        }

        files = (
            "./output_test/Membros_ativos-01-2020.ods",
            "./output_test/Membros_ativos-Verbas Indenizatorias-01-2020.ods",
        )
        employees = parser.parse(files, "01", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_ativos_dez_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "2970",
            "name": "ADINAN APARECIDO DE OLIVEIRA",
            "role": "PROMOTOR DE JUSTICA (ENTRANCIA FINAL)",
            "type": "membro",
            "workplace": "PROMOTORIA DE JUSTICA DE JABOTICABAL",
            "active": True,
            "income": {
                "total": 89843.27,
                "wage": 33689.1,
                "perks": {"total": 33900.45},
                "other": {
                    "total": 22253.72,
                    "trust_position": 0.0,
                    "others_total": 22253.72,
                    "others": {
                        "Gratificação Natalina": 22253.72,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 23764.14,
                "prev_contribution": 9859.5,
                "ceil_retention": 0.0,
                "income_tax": 13904.64,
            },
        }

        files = ("./output_test/Membros_ativos-12-2019.ods",)
        employees = parser.parse(files, "12", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_inativos_jan_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "137707",
            "name": "ABEL PEDRO RIBEIRO",
            "role": "PROMOTOR DE JUSTICA (ENTRANCIA FINAL)",
            "type": "membro",
            "workplace": "PROMOTORIAS DE JUSTICA",
            "active": False,
            "income": {
                "total": 52739.74,
                "wage": 35159.83,
                "perks": {"total": 0.0},
                "other": {
                    "total": 17579.91,
                    "trust_position": 0.0,
                    "others_total": 17579.91,
                    "others": {
                        "Gratificação Natalina": 17579.91,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 11884.88,
                "prev_contribution": 4487.91,
                "ceil_retention": 0.0,
                "income_tax": 7396.97,
            },
        }

        files = ("./output_test/Membros_inativos-01-2020.ods",)
        employees = parser.parse(files, "01", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_inativos_dez_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "948780",
            "name": "AGENOR NAKAZONE",
            "role": "PROCURADOR DE JUSTICA",
            "type": "membro",
            "workplace": "PROCURADORIA DE JUSTICA CRIMINAL",
            "active": False,
            "income": {
                "total": 57373.46,
                "wage": 36742.01,
                "perks": {"total": 0.0},
                "other": {
                    "total": 20631.45,
                    "trust_position": 1506.96,
                    "others_total": 19124.49,
                    "others": {
                        "Gratificação Natalina": 19124.49,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 24777.39,
                "prev_contribution": 8591.43,
                "ceil_retention": 0.0,
                "income_tax": 16185.96,
            },
        }

        files = ("./output_test/Membros_inativos-12-2019.ods",)
        employees = parser.parse(files, "12", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_servidores_inativos_jan_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "1174",
            "name": "ABIGAIR MONTEIRO",
            "role": "OFICIAL DE PROMOTORIA I",
            "type": "servidor",
            "workplace": "AREA REGIONAL DE SAO JOSE DO RIO PRETO",
            "active": False,
            "income": {
                "total": 8458.57,
                "wage": 8458.57,
                "perks": {"total": 0.0},
                "other": {
                    "total": 0.0,
                    "trust_position": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 1372.38,
                "prev_contribution": 604.18,
                "ceil_retention": 0.0,
                "income_tax": 768.2,
            },
        }

        files = ("./output_test/Servidores_inativos-01-2020.ods",)
        employees = parser.parse(files, "01", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_servidores_inativos_dez_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "953273",
            "name": "ALCIDES CAETANO",
            "role": "AUXILIAR DE PROMOTORIA I",
            "type": "servidor",
            "workplace": "AREA DE TRANSPORTES",
            "active": False,
            "income": {
                "total": 10768.1,
                "wage": 6674.54,
                "perks": {"total": 356.24},
                "other": {
                    "total": 3737.32,
                    "trust_position": 0.0,
                    "others_total": 3737.32,
                    "others": {
                        "Gratificação Natalina": 3737.32,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 1546.78,
                "prev_contribution": 447.16,
                "ceil_retention": 0.0,
                "income_tax": 1099.62,
            },
        }

        files = ("./output_test/Servidores_inativos-12-2019.ods",)
        employees = parser.parse(files, "12", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_servidores_ativos_jan_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "1469",
            "name": "ABEL VIEIRA DE MENEZES FILHO",
            "role": " AUXILIAR DE PROMOTORIA I ",
            "type": "servidor",
            "workplace": " AREA REGIONAL DA CAPITAL ",
            "active": True,
            "income": {
                "total": 7874.06,
                "wage": 6623.36,
                "perks": {"total": 1250.7},
                "other": {
                    "total": 0.0,
                    "trust_position": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 1612.73,
                "prev_contribution": 861.02,
                "ceil_retention": 0.0,
                "income_tax": 751.71,
            },
        }

        files = ("./output_test/Servidores_ativos-01-2020.ods",)
        employees = parser.parse(files, "01", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_servidores_ativos_dez_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "4895",
            "name": "ADRIANA SALTO",
            "role": "OFICIAL DE PROMOTORIA I",
            "type": "servidor",
            "workplace": "SERVICO TECNICO ADMINISTRATIVO DE TIETE",
            "active": True,
            "income": {
                "total": 11246.37,
                "wage": 6267.32,
                "perks": {"total": 1169.44},
                "other": {
                    "total": 3809.61,
                    "trust_position": 333.44,
                    "others_total": 3476.17,
                    "others": {
                        "Gratificação Natalina": 3476.17,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 3259.08,
                "prev_contribution": 1757.98,
                "ceil_retention": 0.0,
                "income_tax": 1501.1,
            },
        }

        files = ("./output_test/Servidores_ativos-12-2019.ods",)
        employees = parser.parse(files, "12", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    #  Tests for active members who have different table formats

    def test_active_members_january_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "3725",
            "name": "ABNER CASTORINO",
            "role": "PROMOTOR DE JUSTICA (ENTRANCIA FINAL)",
            "type": "membro",
            "workplace": "PROMOTORIA DE JUSTICA DE SAO BERNARDO DO CAMPO",
            "active": True,
            "income": {
                "total": 34609.1,
                "wage": 33689.1,
                "perks": {"total": 920.0, "food": 920.0, "housing_aid": 0.0},
                "other": {
                    "total": 0.0,
                    "trust_position": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Outras remunerações temporárias": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 11081.84,
                "prev_contribution": 3705.8,
                "ceil_retention": 0.0,
                "income_tax": 7376.04,
            },
        }

        files = ("./output_test/Membros_ativos-01-2019.ods",)
        employees = parser.parse(files, "01", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_members_march_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "3725",
            "name": "ABNER CASTORINO",
            "role": "PROMOTOR DE JUSTICA (ENTRANCIA FINAL)",
            "type": "membro",
            "workplace": "PROMOTORIA DE JUSTICA DE SAO BERNARDO DO CAMPO",
            "active": True,
            "income": {
                "total": 38651.78,
                "wage": 33689.1,
                "perks": {"total": 920.0, "food": 920.0, "ferias em pecunia": 0.0},
                "other": {
                    "total": 4042.68,
                    "trust_position": 0.0,
                    "others_total": 4042.68,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Outras remunerações temporárias": 4042.68,
                    },
                },
            },
            "discounts": {
                "total": 12193.58,
                "prev_contribution": 3705.8,
                "ceil_retention": 0.0,
                "income_tax": 8487.78,
            },
        }

        files = ("./output_test/Membros_ativos-03-2019.ods",)
        employees = parser.parse(files, "03", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_members_june_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "207",
            "name": "FREDERICO AUGUSTO NEVES ARAUJO",
            "role": "PROMOTOR DE JUSTICA (ENTRANCIA FINAL)",
            "type": "membro",
            "workplace": "PROMOTORIA DE JUSTICA DE TAUBATE",
            "active": True,
            "income": {
                "total": 34609.1,
                "wage": 33689.1,
                "perks": {
                    "total": 920.0,
                    "food": 920.0,
                    "ferias em pecunia": 0.0,
                    "LP em pecunia": 0.0,
                },
                "other": {
                    "total": 0.0,
                    "trust_position": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Outras remunerações temporarias": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 11081.84,
                "prev_contribution": 3705.8,
                "income_tax": 7376.04,
            },
        }

        files = ("./output_test/Membros_ativos-06-2019.ods",)
        employees = parser.parse(files, "06", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # #  Tests for inactive members who have different table formats

    def test_inactive_members_january_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "137707",
            "name": "ABEL PEDRO RIBEIRO",
            "role": "PROMOTOR DE JUSTICA (ENTRANCIA FINAL)",
            "type": "membro",
            "workplace": "PROMOTORIAS DE JUSTICA",
            "active": False,
            "income": {
                "total": 45627.43,
                "wage": 30418.28,
                "other": {
                    "total": 15209.15,
                    "others_total": 15209.15,
                    "others": {"Gratificação Natalina": 15209.15},
                },
            },
            "discounts": {
                "total": 18959.9,
                "prev_contribution": 6514.5,
                "ceil_retention": 0.0,
                "income_tax": 26667.53,
            },
        }

        files = ("./output_test/Membros_inativos-01-2019.ods",)
        employees = parser.parse(files, "01", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_inactive_members_may_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "137707",
            "name": "ABEL PEDRO RIBEIRO",
            "role": "PROMOTOR DE JUSTICA (ENTRANCIA FINAL)",
            "type": "membro",
            "workplace": "PROMOTORIAS DE JUSTICA",
            "active": False,
            "income": {
                "total": 35159.83,
                "wage": 35159.83,
                "perks": {"total": 0.0, "food": 0.0, "ferias em pecunia": 0.0},
                "other": {
                    "total": 0.0,
                    "trust_position": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 10614.29,
                "prev_contribution": 3225.24,
                "income_tax": 7389.05,
                "ceil_retention": 0.0,
            },
        }

        files = ("./output_test/Membros_inativos-05-2019.ods",)
        employees = parser.parse(files, "05", "2019")
        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_inactive_members_june_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "137707",
            "name": "ABEL PEDRO RIBEIRO",
            "role": "PROMOTOR DE JUSTICA (ENTRANCIA FINAL)",
            "type": "membro",
            "workplace": "PROMOTORIAS DE JUSTICA",
            "active": False,
            "income": {
                "total": 35159.83,
                "wage": 35159.83,
                "perks": {"total": 0.0, "food": 0.0, "ferias em pecunia": 0.0},
                "other": {
                    "total": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Abono de Permanência": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 10614.29,
                "prev_contribution": 3225.24,
                "income_tax": 7389.05,
                "ceil_retention": 0.0,
            },
        }

        files = ("./output_test/Membros_inativos-06-2019.ods",)
        employees = parser.parse(files, "06", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    #  Tests for Active servants who have different table formats

    def test_active_servants_january_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "1469",
            "name": "ABEL VIEIRA DE MENEZES FILHO",
            "role": "AREA REGIONAL DA CAPITAL",
            "type": "servidor",
            "workplace": "AUXILIAR DE PROMOTORIA I",
            "active": True,
            "income": {
                "total": 7573.02,
                "wage": 6371.44,
                "perks": {
                    "total": 1201.58,
                    "food": 920.0,
                    "transportation": 281.58,
                    "pre_school": 0.0,
                },
                "other": {
                    "total": 0.0,
                    "trust_position": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Gratificação de Qualificação": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 1518.32,
                "prev_contribution": 828.27,
                "ceil_retention": 0.0,
                "income_tax": 690.05,
            },
        }

        files = ("./output_test/Servidores_ativos-01-2019.ods",)
        employees = parser.parse(files, "01", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    #  Tests for Active servants who have different table formats

    def test_inactive_servants_january_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "1174",
            "name": "ABIGAIR MONTEIRO",
            "role": "OFICIAL DE PROMOTORIA I",
            "type": "servidor",
            "workplace": "AREA REGIONAL DE SAO JOSE DO RIO PRETO",
            "active": False,
            "income": {
                "total": 8180.43,
                "wage": 8180.43,
                "other": {
                    "total": 0.0,
                    "others_total": 0.0,
                    "others": {"Gratificação Natalina": 0.0},
                },
            },
            "discounts": {
                "total": 1266.27,
                "prev_contribution": 584.7,
                "income_tax": 681.57,
            },
        }
        files = ("./output_test/Servidores_inativos-01-2019.ods",)
        employees = parser.parse(files, "01", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_inactive_servants_may_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "4324",
            "name": "MILTON RANGEL DE QUADROS",
            "role": "OFICIAL DE PROMOTORIA I",
            "type": "servidor",
            "workplace": "SERVICO TECNICO ADMINISTRATIVO DE ARACATUBA",
            "active": False,
            "income": {
                "total": 8900.62,
                "wage": 5244.0,
                "perks": {
                    "total": 3496.0,
                    "food": 0.0,
                    "transportation": 0.0,
                    "ferias em pecunia": 3496.0,
                },
                "other": {
                    "total": 160.62,
                    "trust_position": 80.31,
                    "others_total": 80.31,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Abono de Permanência": 0.0,
                        "Outras Remunerações Temporárias": 80.31,
                    },
                },
            },
            "discounts": {
                "total": 701.3,
                "prev_contribution": 106.48,
                "income_tax": 594.82,
            },
        }
        files = ("./output_test/Servidores_inativos-05-2019.ods",)
        employees = parser.parse(files, "05", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_inactive_servants_june_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "386921",
            "name": "ANTONIA MARIA DE MATOS",
            "role": "AUXILIAR DE PROMOTORIA I",
            "type": "servidor",
            "workplace": "AREA DE ATIVIDADES COMPLEMENTARES",
            "active": False,
            "income": {
                "total": 6313.87,
                "wage": 5259.27,
                "perks": {"total": 726.78, "food": 562.22, "transportation": 164.56},
                "other": {
                    "total": 327.82,
                    "trust_position": 0.0,
                    "others_total": 327.82,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Abono de Permanência": 327.82,
                        "Gratificação de Qualificação": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 559.27,
                "prev_contribution": 459.95,
                "income_tax": 99.32,
            },
        }

        files = ("./output_test/Servidores_inativos-06-2019.ods",)
        employees = parser.parse(files, "06", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # Tests for archives containing indemnity funds and temporary remuneration

    def test_inactive_members_aug(self):
        self.maxDiff = None

        expected = {
            "reg": "322959",
            "name": "WALERIA GARCELAN LOMA GARCIA",
            "role": "PROCURADOR DE JUSTICA",
            "type": "membro",
            "workplace": "PROCURADORIA DE JUSTICA CRIMINAL",
            "active": False,
            "income": {
                "total": 88834.87,
                "wage": 38072.09,
                "perks": {"total": 50762.78, "vacation_pecuniary": 50762.78},
                "other": {
                    "total": 0.0,
                    "trust_position": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 11004.51,
                "prev_contribution": 5115.36,
                "ceil_retention": 0.0,
                "income_tax": 16119.87,
            },
        }

        files = (
            "./output_test/Membros_inativos-08-2020.ods",
            "./output_test/Membros_inativos-Verbas Indenizatorias-08-2020.ods",
        )
        employees = parser.parse(files, "08", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_inactive_members_sept(self):
        self.maxDiff = None

        expected = {
            "reg": "730",
            "name": "DIANA MARIA SILVA BRAUS",
            "role": "PROMOTOR DE JUSTICA (ENTRANCIA INTERMEDIARIA)",
            "type": "membro",
            "workplace": "PROMOTORIA DE JUSTICA DE BIRIGUI",
            "active": False,
            "income": {
                "total": 46228.93,
                "wage": 32004.65,
                "perks": {
                    "total": 14224.28,
                    "food": 0.0,
                    "vacation_pecuniary": 14224.28,
                },
                "other": {
                    "total": 0.0,
                    "trust_position": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 10936.73,
                "prev_contribution": 4144.57,
                "ceil_retention": 0.0,
                "income_tax": 6792.16,
            },
        }

        files = (
            "./output_test/Membros_inativos-09-2020.ods",
            "./output_test/Membros_inativos-Verbas Indenizatorias-09-2020.ods",
        )
        employees = parser.parse(files, "09", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_inactive_members_nov(self):
        self.maxDiff = None

        expected = {
            "reg": "204231",
            "name": "AIRTON GRAZZIOLI",
            "role": "PROCURADOR DE JUSTICA",
            "type": "membro",
            "workplace": "PROCURADORIA DE JUSTICA CRIMINAL",
            "active": False,
            "income": {
                "total": 54466.36,
                "wage": 37707.48,
                "perks": {
                    "total": 16758.88,
                    "vacation_pecuniary": 16758.88,
                    "premium_license_pecuniary": 0.0,
                },
                "other": {
                    "total": 0.0,
                    "trust_position": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 13651.37,
                "prev_contribution": 5725.76,
                "ceil_retention": 0.0,
                "income_tax": 7925.61,
            },
        }

        files = (
            "./output_test/Membros_inativos-11-2020.ods",
            "./output_test/Membros_inativos-Verbas Indenizatorias-11-2020.ods",
        )
        employees = parser.parse(files, "11", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_inactive_servants_sept(self):
        self.maxDiff = None

        expected = {
            "reg": "165",
            "name": "CLAUDIA REGINA DA SILVA LOPEZ ANTAO",
            "role": "OFICIAL DE PROMOTORIA I",
            "type": "servidor",
            "workplace": "CENTRAL DE INQUERITOS POLICIAIS E PROCESSOS - CIPP",
            "active": False,
            "income": {
                "total": 20577.06,
                "wage": 12543.02,
                "perks": {"total": 487.75, "food": 457.15, "transportation": 30.6},
                "other": {
                    "total": 7546.29,
                    "trust_position": 0.0,
                    "others_total": 7546.29,
                    "others": {
                        "Gratificação Natalina": 6271.5,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 961.22,
                        "INSALUBRIDADE": 0.0,
                        "QUALIFICACAO": 313.57,
                    },
                },
            },
            "discounts": {
                "total": 3838.08,
                "prev_contribution": 1557.99,
                "ceil_retention": 0.0,
                "income_tax": 2280.09,
            },
        }

        files = (
            "./output_test/Servidores_inativos-09-2020.ods",
            "./output_test/Servidores_inativos-Verbas Indenizatorias-09-2020.ods",
        )
        employees = parser.parse(files, "09", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_inactive_servants_aug(self):
        self.maxDiff = None

        expected = {
            "reg": "551283",
            "name": "GLORIMAR MAIA",
            "role": "OFICIAL DE PROMOTORIA I",
            "type": "servidor",
            "workplace": "AREA DE DOCUMENTACAO E DIVULGACAO",
            "active": False,
            "income": {
                "total": 12298.84,
                "wage": 10295.25,
                "perks": {
                    "total": 563.32,
                    "food": 685.72,
                    "transportation": -122.4,
                    "vacation_pecuniary": 0.0,
                },
                "other": {
                    "total": 1440.27,
                    "trust_position": 0.0,
                    "others_total": 1440.27,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 1061.07,
                        "INSALUBRIDADE": 0.0,
                        "QUALIFICACAO": 379.2,
                    },
                },
            },
            "discounts": {
                "total": 3061.69,
                "prev_contribution": 713.81,
                "ceil_retention": 0.0,
                "income_tax": 2347.88,
            },
        }

        files = (
            "./output_test/Servidores_inativos-08-2020.ods",
            "./output_test/Servidores_inativos-Verbas Indenizatorias-08-2020.ods",
        )
        employees = parser.parse(files, "08", "2020")
        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_members_july_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "3725",
            "name": "ABNER CASTORINO",
            "role": "PROMOTOR DE JUSTICA (ENTRANCIA FINAL)",
            "type": "membro",
            "workplace": "PROMOTORIA DE JUSTICA DE SAO BERNARDO DO CAMPO",
            "active": True,
            "income": {
                "total": 40213.32,
                "wage": 33689.1,
                "perks": {"total": 920.0, "food": 920.0, "vacation_pecuniary": 0.0},
                "other": {
                    "total": 5604.22,
                    "trust_position": 0.0,
                    "others_total": 5604.22,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "GRAT. CUMULATIVA": 5604.22,
                        "GRAT. NATUREZA ESPECIAL": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 12623.0,
                "prev_contribution": 3705.8,
                "ceil_retention": 0.0,
                "income_tax": 8917.2,
            },
        }

        files = (
            "./output_test/Membros_ativos-07-2019.ods",
            "./output_test/Membros_ativos-Verbas Indenizatorias-07-2019.ods",
        )
        employees = parser.parse(files, "07", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_members_march_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "3725",
            "name": "ABNER CASTORINO",
            "role": "PROMOTOR DE JUSTICA (ENTRANCIA FINAL)",
            "type": "membro",
            "workplace": "PROMOTORIA DE JUSTICA DE SAO BERNARDO DO CAMPO",
            "active": True,
            "income": {
                "total": 54113.85,
                "wage": 33689.1,
                "perks": {
                    "total": 15932.93,
                    "food": 960.0,
                    "compensatory_leave": 0.0,
                    "vacation_pecuniary": 14972.93,
                    "premium_license_pecuniary": 0.0,
                },
                "other": {
                    "total": 4491.82,
                    "trust_position": 0.0,
                    "others_total": 4491.82,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "GRAT. CUMULATIVA": 4491.82,
                        "GRAT. NATUREZA ESPECIAL": 0.0,
                        "GRAT. DE GRUPO DE ATUAÇÃO ESPECIAL": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 12317.09,
                "prev_contribution": 3705.8,
                "ceil_retention": 0.0,
                "income_tax": 8611.29,
            },
        }

        files = (
            "./output_test/Membros_ativos-03-2020.ods",
            "./output_test/Membros_ativos-Verbas Indenizatorias-03-2020.ods",
        )
        employees = parser.parse(files, "03", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_members_april_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "2526",
            "name": "ALEXANDRA FACCIOLLI MARTINS",
            "role": "PROMOTOR DE JUSTICA (ENTRANCIA FINAL)",
            "type": "membro",
            "workplace": "PROMOTORIA DE JUSTICA DE PIRACICABA",
            "active": True,
            "income": {
                "total": 50745.0,
                "wage": 33689.1,
                "perks": {
                    "total": 15932.93,
                    "food": 960.0,
                    "compensatory_leave": 0.0,
                    "vacation_pecuniary": 14972.93,
                },
                "other": {
                    "total": 1122.97,
                    "trust_position": 0.0,
                    "others_total": 1122.97,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "GRAT. CUMULATIVA": 0.0,
                        "GRAT. NATUREZA ESPECIAL": 0.0,
                        "GRAT. DE GRUPO DE ATUAÇÃO ESPECIAL": 1122.97,
                    },
                },
            },
            "discounts": {
                "total": 11390.66,
                "prev_contribution": 3705.8,
                "ceil_retention": 0.0,
                "income_tax": 7684.86,
            },
        }

        files = (
            "./output_test/Membros_ativos-04-2020.ods",
            "./output_test/Membros_ativos-Verbas Indenizatorias-04-2020.ods",
        )
        employees = parser.parse(files, "04", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_members_aug_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "8505",
            "name": "BRUNO GONDIM RODRIGUES",
            "role": "PROMOTOR DE JUSTICA (ENTRANCIA INICIAL)",
            "type": "membro",
            "workplace": "PROMOTORIA DE JUSTICA DE ITARARE",
            "active": True,
            "income": {
                "total": 54428.71,
                "wage": 30405.3,
                "perks": {
                    "total": 960.0,
                    "food": 960.0,
                    "transportation": 0.0,
                    "pre_school": 0.0,
                    "vacation_pecuniary": 0.0,
                    "premium_license_pecuniary": 0.0,
                    "compensatory_leave": 0.0,
                },
                "other": {
                    "total": 23063.41,
                    "trust_position": 0.0,
                    "others_total": 23063.41,
                    "others": {
                        "Gratificação Natalina": 15202.65,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "INSALUBRIDADE": 0.0,
                        "SUBS. DE FUNÇÃO": 0.0,
                        "VIATURA": 0.0,
                        "GRAT. CUMULATIVA": 6737.8,
                        "GRAT. DE QUALIFICAÇÃO": 0.0,
                        "GRAT. NATUREZA ESPECIAL": 1122.96,
                        "GRAT. DE GRUPO DE ATUAÇÃO ESPECIAL": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 15281.2,
                "prev_contribution": 6912.3,
                "ceil_retention": 0.0,
                "income_tax": 8368.9,
            },
        }

        files = (
            "./output_test/Membros_ativos-08-2020.ods",
            "./output_test/Membros_ativos-Verbas Indenizatorias-08-2020.ods",
        )
        employees = parser.parse(files, "08", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_members_aug_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "4435",
            "name": "ALEXANDRE AFFONSO CASTILHO",
            "role": "PROMOTOR DE JUSTICA (ENTRANCIA FINAL)",
            "type": "membro",
            "workplace": "PROMOTORIA DE JUSTICA DE GUARULHOS",
            "active": True,
            "income": {
                "total": 40263.97,
                "wage": 33689.1,
                "perks": {"total": 960.0, "vacation_pecuniary": 0.0},
                "other": {
                    "total": 5614.87,
                    "trust_position": 0.0,
                    "others_total": 5614.87,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "GRAT. CUMULATIVA": 0.0,
                        "GRAT. NATUREZA ESPECIAL": 4491.9,
                        "GRAT. DE GRUPO DE ATUAÇÃO ESPECIAL": 1122.97,
                    },
                },
            },
            "discounts": {
                "total": 13707.61,
                "prev_contribution": 5197.77,
                "ceil_retention": 0.0,
                "income_tax": 8509.84,
            },
        }

        files = (
            "./output_test/Membros_ativos-10-2020.ods",
            "./output_test/Membros_ativos-Verbas Indenizatorias-10-2020.ods",
        )
        employees = parser.parse(files, "10", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_servants_july_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "7103",
            "name": "ADEMAR RODRIGO CARETTA",
            "role": "AUXILIAR DE PROMOTORIA I",
            "type": "servidor",
            "workplace": "CENTRO TEC. INF. E COMUNICACAO",
            "active": True,
            "income": {
                "total": 6967.67,
                "wage": 3108.6,
                "perks": {
                    "total": 3781.36,
                    "food": 920.0,
                    "transportation": 314.16,
                    "pre_school": 423.0,
                    "vacation_pecuniary": 2124.2,
                },
                "other": {
                    "total": 77.71,
                    "trust_position": 0.0,
                    "others_total": 77.71,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "INSALUBRIDADE": 0.0,
                        "SUBSTITUIÇÃO DE FUNÇÃO": 0.0,
                        "VIATURA": 0.0,
                        "GRAT. DE QUALIFICAÇÂO": 77.71,
                    },
                },
            },
            "discounts": {
                "total": 475.96,
                "prev_contribution": 404.11,
                "ceil_retention": 0.0,
                "income_tax": 71.85,
            },
        }

        files = (
            "./output_test/Servidores_ativos-07-2019.ods",
            "./output_test/Servidores_ativos-Verbas Indenizatorias-07-2019.ods",
        )
        employees = parser.parse(files, "07", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_servants_oct_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "5641",
            "name": "ADELSON SANTOS DA CRUZ",
            "role": "AUXILIAR DE PROMOTORIA I",
            "type": "servidor",
            "workplace": "SERVICO TECNICO ADMINISTRATIVO DE SANTOS",
            "active": True,
            "income": {
                "total": 8711.12,
                "wage": 3170.76,
                "perks": {
                    "total": 3887.73,
                    "transportation": 314.16,
                    "food": 920.0,
                    "pre_school": 0.0,
                    "vacation_pecuniary": 2653.57,
                    "premium_license_pecuniary": 0.0,
                },
                "other": {
                    "total": 1652.63,
                    "trust_position": 712.52,
                    "others_total": 940.11,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Adic. Insalubridade": 712.52,
                        "Subst. Eventual": 0.0,
                        "Ato Norm 766/2013": 130.51,
                        "Gratificação Qualificação": 97.08,
                    },
                },
            },
            "discounts": {
                "total": 705.18,
                "prev_contribution": 507.43,
                "ceil_retention": 0.0,
                "income_tax": 197.75,
            },
        }

        files = (
            "./output_test/Servidores_ativos-10-2019.ods",
            "./output_test/Servidores_ativos-Verbas Indenizatorias-10-2019.ods",
        )
        employees = parser.parse(files, "10", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_servants_nov_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "4921",
            "name": "ADRIANE MOREIRA TEMPEST",
            "role": "ASSESSOR DO MP",
            "type": "servidor",
            "workplace": "SERVICO TECNICO ADMINISTRATIVO DE SANTOS",
            "active": True,
            "income": {
                "total": 19286.37,
                "wage": 16552.89,
                "perks": {
                    "total": 1259.2,
                    "transportation": 299.2,
                    "food": 960.0,
                    "pre_school": 0.0,
                    "vacation_pecuniary": 0.0,
                    "premium_license_pecuniary": 0.0,
                },
                "other": {
                    "total": 1474.28,
                    "trust_position": 761.76,
                    "others_total": 712.52,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Adic. Insalubridade": 712.52,
                        "Subst. Eventual": 0.0,
                        "Ato Norm 766/2013": 0.0,
                        "Gratificação Qualificação": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 4899.1,
                "prev_contribution": 987.63,
                "ceil_retention": 0.0,
                "income_tax": 3911.47,
            },
        }

        files = (
            "./output_test/Servidores_ativos-11-2019.ods",
            "./output_test/Servidores_ativos-Verbas Indenizatorias-11-2019.ods",
        )
        employees = parser.parse(files, "11", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_servants_mar_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "5641",
            "name": "ADELSON SANTOS DA CRUZ",
            "role": " AUXILIAR DE PROMOTORIA I ",
            "type": "servidor",
            "workplace": " SERVICO TECNICO ADMINISTRATIVO DE SANTOS ",
            "active": True,
            "income": {
                "total": 6117.71,
                "wage": 3295.87,
                "perks": {
                    "total": 1296.6,
                    "transportation": 336.6,
                    "food": 960.0,
                    "pre_school": 0.0,
                    "vacation_pecuniary": 0.0,
                    "premium_license_pecuniary": 0.0,
                },
                "other": {
                    "total": 1525.24,
                    "trust_position": 712.52,
                    "others_total": 812.72,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Adic. Insalubridade": 712.52,
                        "Subst. Eventual": 0.0,
                        "Ato Norm 766/2013": 0.0,
                        "Gratificação Qualificação": 100.2,
                    },
                },
            },
            "discounts": {
                "total": 716.43,
                "prev_contribution": 521.08,
                "ceil_retention": 0.0,
                "income_tax": 195.35,
            },
        }

        files = (
            "./output_test/Servidores_ativos-03-2020.ods",
            "./output_test/Servidores_ativos-Verbas Indenizatorias-03-2020.ods",
        )
        employees = parser.parse(files, "03", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_servants_april_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "5057",
            "name": "ALEX SANDRO CLEMENTE DE OLIVEIRA",
            "role": " AUXILIAR DE PROMOTORIA I ",
            "type": "servidor",
            "workplace": " SERVICO TECNICO ADMINISTRATIVO DE PRESIDENTE PRUDENTE ",
            "active": True,
            "income": {
                "total": 8602.73,
                "wage": 3738.17,
                "perks": {
                    "total": 1113.0,
                    "transportation": 153.0,
                    "food": 960.0,
                    "pre_school": 0.0,
                    "vacation_pecuniary": 0.0,
                },
                "other": {
                    "total": 3751.56,
                    "trust_position": 712.52,
                    "others_total": 3039.04,
                    "others": {
                        "Gratificação Natalina": 2215.25,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Adic. Insalubridade": 712.52,
                        "Subst. Eventual": 0.0,
                        "Ato Norm 766/2013": 0.0,
                        "Gratificação Qualificação": 111.27,
                    },
                },
            },
            "discounts": {
                "total": 1192.12,
                "prev_contribution": 981.03,
                "ceil_retention": 0.0,
                "income_tax": 211.09,
            },
        }

        files = (
            "./output_test/Servidores_ativos-04-2020.ods",
            "./output_test/Servidores_ativos-Verbas Indenizatorias-04-2020.ods",
        )
        employees = parser.parse(files, "04", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_servants_aug_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "5068",
            "name": "JULIANO SIMAO MOREIRA",
            "role": "AUXILIAR DE PROMOTORIA I",
            "type": "servidor",
            "workplace": "SERVICO TECNICO-ADMINISTRATIVO DE RIBEIRAO PRETO",
            "active": True,
            "income": {
                "total": 5392.04,
                "wage": 3609.93,
                "perks": {
                    "total": 929.4,
                    "transportation": -30.6,
                    "food": 960.0,
                    "pre_school": 0.0,
                    "vacation_pecuniary": 0.0,
                    "premium_license_pecuniary": 0.0,
                },
                "other": {
                    "total": 852.71,
                    "trust_position": 0.0,
                    "others_total": 852.71,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Adic. Insalubridade": 743.87,
                        "Substituição de Função": 0.0,
                        "Viatura": 0.0,
                        "Gratificação Qualificação": 108.84,
                    },
                },
            },
            "discounts": {
                "total": 785.75,
                "prev_contribution": 539.08,
                "ceil_retention": 0.0,
                "income_tax": 246.67,
            },
        }

        files = (
            "./output_test/Servidores_ativos-08-2020.ods",
            "./output_test/Servidores_ativos-Verbas Indenizatorias-08-2020.ods",
        )
        employees = parser.parse(files, "08", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_servants_oct_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "1469",
            "name": "ABEL VIEIRA DE MENEZES FILHO",
            "role": "AUX. DE PROMOTORIA ENCARREGADO",
            "type": "servidor",
            "workplace": "AREA REGIONAL DA CAPITAL",
            "active": True,
            "income": {
                "total": 7705.76,
                "wage": 6623.36,
                "perks": {
                    "total": 1082.4,
                    "transportation": 122.4,
                    "food": 960.0,
                    "pre_school": 0.0,
                    "vacation_pecuniary": 0.0,
                },
                "other": {
                    "total": 0.0,
                    "trust_position": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Adic. Insalubridade": 0.0,
                        "Substituição de Função": 0.0,
                        "Viatura": 0.0,
                        "Gratificação Qualificação": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 1580.82,
                "prev_contribution": 867.25,
                "ceil_retention": 0.0,
                "income_tax": 713.57,
            },
        }

        files = (
            "./output_test/Servidores_ativos-10-2020.ods",
            "./output_test/Servidores_ativos-Verbas Indenizatorias-10-2020.ods",
        )
        employees = parser.parse(files, "10", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_memberes_dez_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "2250",
            "name": "ADELMO PINHO",
            "role": "PROMOTOR DE JUSTICA (ENTRANCIA FINAL)",
            "type": "membro",
            "workplace": "PROMOTORIA DE JUSTICA DE ARACATUBA",
            "active": True,
            "income": {
                "total": 87007.52,
                "wage": 33689.1,
                "perks": {
                    "total": 30905.86,
                    "food": 960.0,
                    "vacation_pecuniary": 29945.86,
                },
                "other": {
                    "total": 22412.56,
                    "trust_position": 0.0,
                    "others_total": 22412.56,
                    "others": {
                        "Gratificação Natalina": 20728.12,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "GRAT. CUMULATIVA": 0.0,
                        "GRAT. NATUREZA ESPECIAL": 1684.44,
                        "GRAT. DE GRUPO DE ATUAÇÃO ESPECIAL": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 23737.92,
                "prev_contribution": 8461.43,
                "ceil_retention": 0.0,
                "income_tax": 15276.49,
            },
        }
        files = (
            "./output_test/Membros_ativos-12-2020.ods",
            "./output_test/Membros_ativos-Verbas Indenizatorias-12-2020.ods",
        )
        employees = parser.parse(files, "12", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_servants_dez_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "10322",
            "name": "ADAMO VINICIUS PINHEIRO CAROL",
            "role": "ANALISTA JURIDICO DO MP",
            "type": "servidor",
            "workplace": "AREA REGIONAL DA CAPITAL",
            "active": True,
            "income": {
                "total": 25645.96,
                "wage": 8145.02,
                "perks": {
                    "total": 12512.12,
                    "transportation": -122.4,
                    "food": 960.0,
                    "pre_school": 0.0,
                    "vacation_pecuniary": 11674.52,
                    "premium_license_pecuniary": 0.0,
                },
                "other": {
                    "total": 4988.82,
                    "trust_position": 0.0,
                    "others_total": 4988.82,
                    "others": {
                        "Gratificação Natalina": 4377.95,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Adic. Insalubridade": 0.0,
                        "Substituição de Função": 0.0,
                        "Gratificação Qualificação": 610.87,
                    },
                },
            },
            "discounts": {
                "total": 3636.88,
                "prev_contribution": 978.0,
                "ceil_retention": 0.0,
                "income_tax": 2658.88,
            },
        }
        files = (
            "./output_test/Servidores_ativos-12-2020.ods",
            "./output_test/Servidores_ativos-Verbas Indenizatorias-12-2020.ods",
        )
        employees = parser.parse(files, "12", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_inactive_servants_dez_2020(self):
        self.maxDiff = None

        expected = {
            "reg": "1210",
            "name": "ANTONIO AUGUSTO TAVARES",
            "role": "OFICIAL DE PROMOTORIA I",
            "type": "servidor",
            "workplace": "SERVICO TECNICO-ADMINISTRATIVO DE CAMPINAS",
            "active": False,
            "income": {
                "total": 15203.92,
                "wage": 11468.15,
                "perks": {
                    "total": -1266.0,
                    "food": -960.0,
                    "transportation": -306.0,
                    "vacation_pecuniary": 0.0,
                    "premium_license_pecuniary": 0.0,
                },
                "other": {
                    "total": 5001.77,
                    "trust_position": 0.0,
                    "others_total": 5001.77,
                    "others": {
                        "Gratificação Natalina": 5734.08,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": -732.31,
                        "INSALUBRIDADE": 0.0,
                    },
                },
            },
            "discounts": {
                "total": 4349.13,
                "prev_contribution": 1709.24,
                "ceil_retention": 0.0,
                "income_tax": 2639.89,
            },
        }
        files = (
            "./output_test/Servidores_inativos-12-2020.ods",
            "./output_test/Servidores_inativos-Verbas Indenizatorias-12-2020.ods",
        )
        employees = parser.parse(files, "12", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == "__main__":
    unittest.main()
