import os
import parser
import unittest


class TestParser(unittest.TestCase):
    def test_membros_ativos(self):
        self.maxDiff = None

        expected = {
            "reg": "128971",
            "name": "ACHILES DE JESUS SIQUARA FILHO",
            "role": "PROCURADOR DE JUSTICA",
            "type": "membro",
            "workplace": "PROCURADORIA DE JUSTICA CIVEL",
            "active": True,
            "income": {
                "total": 79435.09,
                "wage": 35462.22,
                "other": {
                    "total": 42672.87,
                    "trust_position": 0.0,
                    "others_total": 42672.87,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Férias (1/3 constitucional)": 35462.22,
                        "Abono de Permanência": 4964.71,
                        "Substituição de Membros": 2245.94,
                        "Serviço Extraordinário": 0.0,
                        "Substituição de Função": 0.0,
                        "Gratificação de Serviços Especiais": 0.0,
                        "Diferença de Entrância": 0.0,
                    },
                },
                "perks": {
                    "total": 1300.0,
                    "food": 1300.0,
                    "transportation": 0.0,
                    "housing_aid": 0.0,
                    "birth_aid": 0.0,
                    "subsistence": 0.0,
                },
            },
            "discounts": {
                "total": 22625.93,
                "prev_contribution": 4964.71,
                "ceil_retention": 0.0,
                "income_tax": 17661.22,
            },
        }
        files = (
            "./output_test/Membros ativos-01-2020.ods",
            "./output_test/Membros ativos-Verbas Indenizatorias-01-2020.ods",
        )
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == "__main__":
    unittest.main()
