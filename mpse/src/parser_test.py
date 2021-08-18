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
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


    def test_membros_ativos_remuneracao_2018_5(self):
        self.maxDiff = None

        expected = {
            "reg": "2069",
            "name": "LEA ALVES SCHLINGMANN",
            "role": "TÉCNICO DO MP",
            "type": "membro",
            "workplace": "SEDE/MP",
            "active": True,
            "income": {
                "total": 13509.64,
                "wage": 2497.35,
                "perks": {
                    "total": 1000.0,
                    "vacation": 4169.88
                },
                "other": {
                    "total": 10012.29,
                    "trust_position": 10012.29,
                    "eventual_benefits": 0.0,
                    "others_total": 4169.88,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Abono de Permanência": 0.0
                    }
                }
            },
            "discounts": {
                "total": 2806.17,
                "prev_contribution": 324.66,
                "ceil_retention": 0.0,
                "income_tax": 2481.51
            }
        }

        second_expected = {
            "reg": "2134",
            "name": "JOSE AUGUSTO RAMOS DA SILVA",
            "role": "POLICIAL MILITAR ",
            "type": "membro",
            "workplace": "SEDE/MP",
            "active": True,
            "income": {
                "total": 1259.55,
                "wage": 1259.55,
                "perks": {
                    "total": 0.0,
                    "vacation": 0.0
                },
                "other": {
                    "total": 0.0,
                    "trust_position": 0.0,
                    "eventual_benefits": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Abono de Permanência": 0.0
                    }
                }
            },
            "discounts": {
                "total": 0.0,
                "prev_contribution": 0.0,
                "ceil_retention": 0.0,
                "income_tax": 0.0
            }
        }

        files = ['./output_test/remuneracao-membros-ativos-5-2018.ods']

        employees = parser.parse(files, '2018', '5')

        # Verificações
        self.assertEqual(2, len(employees))
        self.assertDictEqual(employees[0], expected)
        self.assertDictEqual(employees[1], second_expected)


    def test_membros_ativos_remuneracao_2018_10(self):
        self.maxDiff = None

        expected = {
            "reg": "2155",
            "name": "LARISSA CAROLAINE MENEZES DE OLIVEIRA",
            "role": "ASSESSOR OPERACIONAL",
            "type": "membro",
            "workplace": "SEDE/MP",
            "active": True,
            "income": {
                "total": 3091.82,
                "wage": 0.0,
                "perks": {
                    "total": 1020.9,
                    "vacation": 0.0
                },
                "other": {
                    "total": 2070.92,
                    "trust_position": 2070.92,
                    "eventual_benefits": 0.0,
                    "others_total": 0.0,
                    "others": {
                        "Gratificação Natalina": 0.0,
                        "Abono de Permanência": 0.0
                    }
                }
            },
            "discounts": {
                "total": 186.38,
                "prev_contribution": 186.38,
                "ceil_retention": 0.0,
                "income_tax": 0.0
            }
        }

        files = ['./output_test/remuneracao-membros-ativos-10-2018.ods']

        employees = parser.parse(files, '2018', '10')

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


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
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


    def test_membros_ativos_remuneracao_2019_8(self):
            self.maxDiff = None

            expected = {
                "reg": "1480",
                "name": "THIAGO LIMA FEITOZA",
                "role": "ANALISTA DO MP -Informática - G. e A.de P. de Sistemas",
                "type": "membro",
                "workplace": "DIRETORIA DE TECNOLOGIA DA INFORMACAO",
                "active": True,
                "income": {
                    "total": 14435.46,
                    "wage": 9132.61,
                    "perks": {
                        "total": 1735.39,
                        "vacation": 0.0,
                        "food": 1020.9,
                        "health": 714.49
                    },
                    "other": {
                        "total": 3567.46,
                        "trust_position": 3567.46,
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
                    "total": 3483.91,
                    "prev_contribution": 1187.24,
                    "ceil_retention": 0.0,
                    "income_tax": 2296.67
                }
            }

            files = ['./output_test/indenizacao-membros-ativos-8-2019.ods',
                    './output_test/remuneracao-membros-ativos-8-2019.odt']

            employees = parser.parse(files, '2019', '8')

            # Verificações
            self.assertEqual(1, len(employees))
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
        self.assertEqual(1, len(employees))
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
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == '__main__':
    unittest.main()