import parser
import unittest

class TestParser(unittest.TestCase):
    def test_membros_ativos_remuneracao_2018(self):
        self.maxDiff = None

        expected = {
            "reg": "16",
            "name": "CELSO LUIS DORIA LEO",
            "role": " PROCURADOR DE JUSTIÇA ",
            "type": "membro",
            "workplace": "SEDE/MP",
            "active": True,
            "income": {
                "total": 42145.06,
                "wage": 31519.76,
                "perks": {
                    "total": 6527.73,
                    "vacation": 0.0
                },
                "other": {
                    "total": 4097.57,
                    "trust_position": 0.0,
                    "eventual_benefits": 0.0,
                    "others_total": 4097.57,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Abono de Permanência": 4097.57
                    }
                }
            },
            "discounts": {
                "total": 11243.81,
                "prev_contribution": 4097.57,
                "ceil_retention": 0.0,
                "income_tax": 7146.24
            }
        }
        
        files = ['./output_test/remuneracao-membros-ativos-2-2018.ods']
        employees = parser.parse(files, '2018', '2')

        # Verificações
        self.assertEqual(len(employees), len(employees))
        self.assertDictEqual(employees[1], expected)


    def test_membros_ativos_remuneracao_2019(self):
        self.maxDiff = None

        expected = {
            "reg": "1454",
            "name": "ADALBERTO MENDES DE OLIVEIRA NETO",
            "role": "ANALISTA DO MP - DIREITO",
            "type": "membro",
            "workplace": "PROMOTORIA DE JUSTICA ESPECIAL CIVEL E CRIMINAL - ESTANCIA ",
            "active": True,
            "income": {
                "total": 13443.12,
                "wage": 7854.38,
                "perks": {
                    "total": 2598.78,
                    "vacation": 0.0
                },
                "other": {
                    "total": 2989.96,
                    "trust_position": 0.0,
                    "eventual_benefits": 0.0,
                    "others_total": 2989.96,
                    "others": {
                        "Gratificação Natalina": 2989.96,
                        "Abono de Permanência": 0.0
                    }
                }
            },
            "discounts": {
                "total": 1874.46,
                "prev_contribution": 1021.07,
                "ceil_retention": 0.0,
                "income_tax": 853.39
            }
        }

        files = ['./output_test/remuneracao-membros-ativos-6-2019.odt']
        employees = parser.parse(files, '2019', '6')

        # Verificações
        self.assertEqual(791, len(employees))
        self.assertDictEqual(employees[0], expected)


    def test_membros_ativos_remuneracao_2021_1(self):
        self.maxDiff = None

        expected = {
            "reg": "1741",
            "name": "ADEILDO JOSE DA SILVA",
            "role": "ANALISTA DO MP- CONTADOR",
            "type": "membro",
            "workplace": "DIVISAO DE PERICIA CONTABIL - GAAE",
            "active": True,
            "income": {
                "total": 9471.21,
                "wage": 7087.14,
                "perks": {
                    "total": 2384.07,
                    "vacation": 0.0,
                    "food": 1056.0,
                    "health": 1328.07
                },
                "other": {
                    "total": 0.0,
                    "trust_position": 0.0,
                    "eventual_benefits": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Abono de Permanência": 0.0,
                        "Auxilio Interiorização": 0.0,
                        "Auxilio lei 8.625/93": 0.0,
                        "Indenizações Férias/Licença-Prêmio": 0.0,
                        "Abono Pecuniário": 0.0,
                        "Ressarcimentos": 0.0,
                        "GEO": 0.0,
                        "Insalubridade": 0.0,
                        "Periculosidade": 0.0,
                        "Adicional Trabalho Tecnico": 0.0,
                        "Grat. Atividade Ensino": 0.0,
                        "Substituições": 0.0,
                        "Cumulação": 0.0,
                        "Represetação de Direção": 0.0,
                        "Grat. Turma Recursal": 0.0,
                        "Grat. Dificil Provimento": 0.0,
                        "Grat. Acessor": 0.0,
                        "Representação GAEGO": 0.0
                    }
                }
            },
            "discounts": {
                "total": 1694.67,
                "prev_contribution": 992.2,
                "ceil_retention": 0.0,
                "income_tax": 702.47
            }
        }

        files = ['./output_test/indenizacao-membros-ativos-1-2021.ods',
                './output_test/remuneracao-membros-ativos-1-2021.odt']

        employees = parser.parse(files, '2021', '1')

        # Verificações
        self.assertEqual(len(employees), len(employees))
        self.assertDictEqual(employees[0], expected)


    def test_membros_ativos_remuneracao_2021_2(self):
        self.maxDiff = None

        expected = {
            "reg": "1741",
            "name": "ADEILDO JOSE DA SILVA",
            "role": "ANALISTA DO MP- CONTADOR",
            "type": "membro",
            "workplace": "DIVISAO DE PERICIA CONTABIL - GAAE",
            "active": True,
            "income":{
                "total": 9471.21,
                "wage": 7087.14,
                "perks":{
                    "total": 2384.07,
                    "vacation": 0.0,
                    "food": 1056.0,
                    "health": 1328.07
                },
                "other": {
                    "total": 0.0,
                    "trust_position": 0.0,
                    "eventual_benefits": 0.0,
                    "others_total": 0.0,
                    "others":{
                        "Gratificação Natalina": 0.0,
                        "Abono de Permanência": 0.0,
                        "Auxilio Interiorização": 0.0,
                        "Auxilio lei 8.625/93": 0.0,
                        "Indenizações Férias/Licença-Prêmio": 0.0,
                        "Abono Pecuniário": 0.0,
                        "Ressarcimentos": 0.0,
                        "GEO": 0.0,
                        "Insalubridade": 0.0,
                        "Periculosidade": 0.0,
                        "Adicional Trabalho Tecnico": 0.0,
                        "Grat. Atividade Ensino": 0.0,
                        "Substituições": 0.0,
                        "Cumulação": 0.0,
                        "Represetação de Direção": 0.0,
                        "Grat. Turma Recursal": 0.0,
                        "Grat. Dificil Provimento": 0.0,
                        "Grat. Acessor": 0.0,
                        "Representação GAEGO": 0.0,
                        "Gratificação Diretor Subsede": 0.0
                    }
                }
            },
            "discounts": {
                "total": 1694.67,
                "prev_contribution": 992.2,
                "ceil_retention": 0.0,
                "income_tax": 702.47
            }
        }

        files = ['./output_test/indenizacao-membros-ativos-2-2021.ods',
                './output_test/remuneracao-membros-ativos-2-2021.odt']

        employees = parser.parse(files, '2021', '2')

        # Verificações
        self.assertEqual(len(employees), len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == '__main__':
    unittest.main()