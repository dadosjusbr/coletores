import unittest
from parser import parse

class TestParser(unittest.TestCase):
    def test_membros_ativos_2021_05(self):
        self.maxDiff = None

        expected = {
            "reg": "1070738",
            "name": "AARAO CARLOS LIMA CASTRO",
            "role": "Promotor de Justiï¿½a de Ent. Intermediï¿½ria",
            "type": "membro",
            "workplace": "Promotoria de Justiï¿½a da Comarca de Colinas",
            "active": True,
            "income": {
                "total": 64329.44,
                "wage": 32004.7,
                "perks": {
                    "total": 7787.81,
                    "Food": 3200.47,
                    "Health": 1920.28,
                    "Subsistence": 0.0,
                    "VacationPecuniary": 0.0,
                    "PremiumLicensePecuniary": 2667.06,
                    "HousingAid": 0.0
                },
                "other": {
                    "total": 27203.99,
                    "trust_position": 0.0,
                    "others_total": 27203.99,
                    "others": {
                        "Férias 1/3 constitucionais": 21336.46,
                        "Gratificação Natalina": 0.0,
                        "Abono de Permanência": 0.0,
                        "grat_encargo_curso_concurso": 0.0,
                        "ind_licenca_premio_espec_nao_gozada": 2667.06,
                        "inden_conv_ferias_em_pecunia_com_1_3": 0.0,
                        "dif_terco_conv_ferias_pecunia": 0.0,
                        "inden_conv_pec_licensa_especial": 0.0,
                        "dif_pen_alimenticia": 0.0,
                        "dif_subs_cumulativa": 0.0,
                        "dif_inden_conv_pec_lic_comp_subs_cumul_membro": 0.0,
                        "inden_conv_pec_lic_compensatoria_subs_cumul_membro": 0.0,
                        "dif_ress_conv_mestrado_int_direito": 0.0,
                        "ress_conv_mestrado_int_direito": 0.0,
                        "dif_subsidios": 0.0,
                        "dif_abono_permanencia": 0.0,
                        "resp_direcao_promotoria": 0.0,
                        "subs_cumulativa": 0.0,
                        "dif_gratificacao_por_funcao_ministerio_publico": 0.0,
                        "dif_resp_direcao_promotoria": 0.0,
                        "dif_direcao_promotoria": 0.0,
                        "subs_funcao_minis_pub": 0.0,
                        "dif_terco_const_ferias": 0.0,
                        "dif_13_salario": 0.0,
                        "direcao_promotoria": 3200.47
                    }
                }
            },
            "discounts": {
                "total": 12834.93,
                "prev_contribution": 5548.78,
                "ceil_retention": 0.0,
                "income_tax": 7286.15
            }
        }

        files = ['./output_test/05-2021-remuneracao-membros-ativos.html',
         './output_test/05-2021-verbas-indenizatorias-membros-ativos.html']
        employees = parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == '__main__':
    unittest.main()