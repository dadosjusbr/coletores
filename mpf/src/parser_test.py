import jun19Backward
import july19Forward
import os
import unittest

# Teste de unidade para cada planilha do mpf, de modo a aumentar a confiança no processo de parsing.
# Objetos criados pela análise da unica linha em questão das planilhas referentes a Janeiro de 2020--- #


class TestParser(unittest.TestCase):
    def test_membros_ativos_july19_forward(self):
        self.maxDiff = None

        expected = {
            "reg": "844",
            "name": "LAURO PINTO CARDOSO NETO",
            "role": "PROCURADOR REGIONAL DA REPÚBLICA",
            "type": "membro",
            "workplace": "PRR1ª REGIÃO",
            "active": True,
            "income": {
                "total": 122883.68,
                "wage": 38819.79,
                "perks": {
                    "total": 35416.56,
                    "vacation": 0,
                    "food": 910.08,
                    "pre_school": 0,
                    "transportation": 0,
                    "furniture_transport": 0,
                    "birth_aid": 0,
                    "subsistence": 0,
                    "housing_aid": 0,
                    "pecuniary": 34506.48,
                    "premium_license_pecuniary": 0,
                },
                "other": {
                    "total": 48647.33,
                    "trust_position": 0,
                    "others_total": 48647.33,
                    "others": {
                        "Gratificação Natalina": 19409.9,
                        "Férias (1/3 constitucional)": 25879.86,
                        "Abono de Permanência": 0,
                        "Gratificação de Perícia e Projeto": 0,
                        "Gratificação Exercício Cumulativo de Ofício": 0,
                        "Gratificação Encargo de Curso e Concurso": 0,
                        "Gratificação Local de Trabalho": 0,
                        "Hora Extra": 0,
                        "Adicional Noturno": 0,
                        "Adicional Atividade Penosa": 0,
                        "Adicional Insalubridade": 0,
                        "Outras Verbas Remuneratórias": 3357.57,
                        "Outras Verbas Remuneratórias Retroativas/Temporárias": 0,
                    },
                },
            },
            "discounts": {
                "total": 18734.72,
                "prev_contribution": 4270.17,
                "ceil_retention": 0,
                "income_tax": 14464.55,
            },
        }
        files = (
            "./test_files/remuneracao-membros-ativos_2020_Janeiro.ods",
            "./test_files/Membros ativos-Verbas Indenizatorias-Janeiro-2020.ods",
        )
        employees = july19Forward.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_ativos_jun19_backward(self):
        self.maxDiff = None

        expected = {
            "name": "ACACIA SOARES PEIXOTO SUASSUNA",
            "role": "PROCURADOR DA REPUBLICA",
            "type": "membro",
            "workplace": "PRM-C.GRANDE",
            "active": True,
            "income": {
                "total": 29831.55,
                "wage": 28947.55,
                "perks": {"total": 884},
                "other": {
                    "total": 0,
                    "trust_position": 0,
                    "others_total": 0,
                    "others": {
                        "Gratificação Natalina": 0,
                        "Férias (1/3 constitucional)": 0,
                        "Abono de Permanência": 0,
                    },
                },
            },
            "discounts": {
                "total": 8808.64,
                "prev_contribution": 3184.23,
                "ceil_retention": 0,
                "income_tax": 5624.41,
            },
        }
        files = ("./test_files/Membros ativos-Janeiro-2018.xls",)
        employees = jun19Backward.parse(files, "2018", "1")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == "__main__":
    unittest.main()
