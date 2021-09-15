import unittest
from parser import parse

class TestParser(unittest.TestCase):
    def test_membros_ativos_2020_01(self):
        self.maxDiff = None

        expected = {
            "reg": "1067354",
            "name": "ANDRE CHARLES ALCANTARA MARTINS OLIVEIRA",
            "role": "Promotor de Justiï¿½a de Ent. Intermediï¿½ria",
            "type": "membro",
            "workplace": "Promotoria de Justiï¿½a da Comarca de Vargem Grande",
            "active": True,
            "income": {
                "total": 44486.53,
                "wage": 32004.7,
                "perks": {
                    "total": 9281.36,
                    "Food": 3200.47,
                    "Health": 1920.28,
                    "Subsistence": 0.0,
                    "VacationPecuniary": 0.0,
                    "PremiumLicensePecuniary": 2667.06
                },
                "other": {
                    "total": 7894.49,
                    "trust_position": 0.0,
                    "others_total": 7894.49,
                    "others": {
                        "Férias 1/3 constitucionais": 0.0,
                        "Gratificação Natalina": 0.0,
                        "Abono de Permanência": 0.0,
                        "Dif. Inden. Conv. Pec. Lic. Comp. Subs. Cumul. Membro": 0.0,
                        "Inden. Conv. Pec. Lic. Compensatoria Subs. Cumul. Membro": 1493.55,
                        "Dif. Abono de Permanência": 0.0,
                        "Dif. Direção de Promotoria": 0.0,
                        "Dif. Gratificação por Função Mininistério Público": 0.0,
                        "Dif. RESP. Direção de Promotorias": 3200.47,
                        "Direção de Promotoria": 0.0,
                        "RESP. Direção de Promotorias": 3200.47
                    }
                }
            },
            "discounts": {
                "total": 10542.78,
                "prev_contribution": 5177.96,
                "ceil_retention": 0.0,
                "income_tax": 5364.82
            }
        }

        files = ['./output_test/07-2020-remuneracao-membros-ativos.html',
         './output_test/07-2020-verbas-indenizatorias-membros-ativos.html']
        employees = parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == '__main__':
    unittest.main()