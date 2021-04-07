import os
import parser
import unittest


class TestParser(unittest.TestCase):
    def test_membros_ativos(self):
        self.maxDiff = None

        expected = {
            "reg": "10092",
            "name": "ANDRÉ LUIZ CAPPI PEREIRA ",
            "role": " PROMOTOR DE JUSTIÇA",
            "type": "membro",
            "workplace": "Procuradoria-Geral de Justiça do Ministério Público do Distrito Federal e Territórios",
            "active": True,
            "income": {
                "total": 59661.15,
                "wage": 33689.11,
                "other": {
                    "total": 24342.34,
                    "trust_position": 3225.42,
                    "others_total": 21116.92,
                    "others": {
                        "Gratificação Natalina": 19343.81,
                        "Férias (1/3 constitucional)": 0.0,
                        "Abono de Permanência": 0.0,
                        "Substituição de Membros": 0.0,
                        "Função de Substituição": 0.0,
                        "Gratificação por Encargo de Curso": 0.0,
                        "Adicional de Insalubridade": 0.0,
                        "Gratificação por Encargo de Concurso": 0.0,
                        "Adicional de Periculosidade": 0.0,
                        "Gratificação de Exercício Cumulativo com Ofício Sem Psss": 0.0,
                        "Gratificação Exercício Cumulativo com Ofício Com Psss": 0.0,
                        "Membros Substituição": 1773.11,
                        "Hora Extra Sem Psss": 0.0,
                        "Adicional Noturno Sem Psss": 0.0,
                        "Substituição Membros MS2013": 0.0,
                        "Adicional Penosidade": 0.0,
                    },
                },
                "perks": {
                    "total": 1629.7,
                    "food": 910.08,
                    "pre_school": 719.62,
                    "transportation": 0.0,
                    "housing_aid": 0.0,
                    "vacation": 0.0,
                    "pecuniary": 0.0,
                    "subsistence": 0.0,
                    "birth_aid": 0.0,
                    "premium_license_pecuniary": 0.0,
                },
            },
            "discounts": {
                "total": 9442.44,
                "prev_contribution": 671.11,
                "ceil_retention": 0.0,
                "income_tax": 8771.33,
            },
        }
        files = (
            "./output_test/Membros ativos-1-2020.ods",
            "./output_test/Membros ativos-Verbas Indenizatorias-1-2020.ods",
            "./output_test/Membros ativos-Verbas Temporarias-1-2020.ods",
        )
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == "__main__":
    unittest.main()
