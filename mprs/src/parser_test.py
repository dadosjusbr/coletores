import parser
import unittest

class TestParser(unittest.TestCase):
    # Membros ativos sem folha complementar e de 13º
    def test_membros_ativos(self):
        self.maxDiff = None

        expected = {
            'reg': '3418723',
            'name': 'ADONIRAN LEMOS ALMEIDA FILHO',
            'role': 'PROMOTOR DE JUSTICA DE ENTRÂNCIA INICIAL',
            'type': 'membro',
            'workplace': 'PROMOTORIA DE JUSTIÇA DE PINHEIRO MACHADO',
            'active': True,
            'income': {
                'total': 26472.47,
                'wage': 25851.96,
                'perks': {
                    'total': 620.51
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 8253.96,
                'prev_contribution': 4008.95,
                'ceil_retention': 0.0,
                'income_tax': 4245.01
            }
        }

        second_expected = {
            'reg': '3427811',
            'name': 'BRUNO HERINGER JUNIOR', 
            'role': 'PROMOTOR DE JUSTICA DE ENTRÂNCIA FINAL', 
            'type': 'membro', 
            'workplace': 'SUBPROCURADORIA-GERAL DE JUSTIÇA PARA ASSUNTOS JURÍDICOS', 
            'active': True, 
            'income': {
                'total': 39563.9, 
                'wage': 31916.0, 
                'perks': {
                    'total': 910.08
                }, 
                'other': {
                    'total': 6737.82, 
                    'trust_position': 3191.6, 
                    'others_total': 3546.22, 
                    'others': {
                        'Gratificação Natalina': 0.0, 
                        'Férias (1/3 constitucional)': 3546.22, 
                        'Abono de Permanência': 0.0
                    }
                }
            }, 
            'discounts': {
                'total': 12632.88, 
                'prev_contribution': 5161.11, 
                'ceil_retention': 0.0, 
                'income_tax': 7471.77
            }
        }

        files = ["./output_test/M-NORMAL-12-2020.json"]
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(2, len(employees))
        self.assertDictEqual(employees[0], expected)
        self.assertDictEqual(employees[1], second_expected)

    # Membros ativos com folha complementar
    def test_membros_ativos_complementar(self):
        self.maxDiff = None

        expected = {
            'reg': '3418723',
            'name': 'ADONIRAN LEMOS ALMEIDA FILHO',
            'role': 'PROMOTOR DE JUSTICA DE ENTRÂNCIA INICIAL',
            'type': 'membro',
            'workplace': 'PROMOTORIA DE JUSTIÇA DE PINHEIRO MACHADO',
            'active': True,
            'income': {
                'total': 52324.43,
                'wage': 25851.96,
                'perks': {
                    'total': 26472.47
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 8253.96,
                'prev_contribution': 4008.95,
                'ceil_retention': 0.0,
                'income_tax': 4245.01
            }
        }

        second_expected = {
            'reg': '3427811',
            'name': 'BRUNO HERINGER JUNIOR', 
            'role': 'PROMOTOR DE JUSTICA DE ENTRÂNCIA FINAL', 
            'type': 'membro', 
            'workplace': 'SUBPROCURADORIA-GERAL DE JUSTIÇA PARA ASSUNTOS JURÍDICOS', 
            'active': True, 
            'income': {
                'total': 75167.97, 
                'wage': 31916.0, 
                'perks': {
                    'total': 36514.15
                }, 
                'other': {
                    'total': 6737.82, 
                    'trust_position': 3191.6, 
                    'others_total': 3546.22, 
                    'others': {
                        'Gratificação Natalina': 0.0, 
                        'Férias (1/3 constitucional)': 3546.22, 
                        'Abono de Permanência': 0.0
                    }
                }
            }, 
            'discounts': {
                'total': 12632.88, 
                'prev_contribution': 5161.11, 
                'ceil_retention': 0.0, 
                'income_tax': 7471.77
            }
        }

        files = ["./output_test/M-NORMAL-12-2020.json", 
                 "./output_test/M-COMPLEMENTAR-12-2020.json"]
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(2, len(employees))
        self.assertDictEqual(employees[0], expected)
        self.assertDictEqual(employees[1], second_expected)

    # Membros ativos com folha complementar e 13º
    def test_membros_ativos_decimo(self):
        self.maxDiff = None

        expected = {
            'reg': '3418723',
            'name': 'ADONIRAN LEMOS ALMEIDA FILHO',
            'role': 'PROMOTOR DE JUSTICA DE ENTRÂNCIA INICIAL',
            'type': 'membro',
            'workplace': 'PROMOTORIA DE JUSTIÇA DE PINHEIRO MACHADO',
            'active': True,
            'income': {
                'total': 78176.39,
                'wage': 51703.92,
                'perks': {
                    'total': 26472.47
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 17348.24,
                'prev_contribution': 8017.9,
                'ceil_retention': 0.0,
                'income_tax': 9330.34
            }
        }
        
        second_expected = {
            'reg': '3427811',
            'name': 'BRUNO HERINGER JUNIOR', 
            'role': 'PROMOTOR DE JUSTICA DE ENTRÂNCIA FINAL', 
            'type': 'membro', 
            'workplace': 'SUBPROCURADORIA-GERAL DE JUSTIÇA PARA ASSUNTOS JURÍDICOS', 
            'active': True, 
            'income': {
                'total': 110275.57, 
                'wage': 63832.0, 
                'perks': {
                    'total': 36514.15
                }, 
                'other': {
                    'total': 9929.42, 
                    'trust_position': 6383.2, 
                    'others_total': 3546.22, 
                    'others': {
                        'Gratificação Natalina': 0.0, 
                        'Férias (1/3 constitucional)': 3546.22, 
                        'Abono de Permanência': 0.0
                    }
                }
            }, 
            'discounts': {
                'total': 25159.92, 
                'prev_contribution': 10322.23, 
                'ceil_retention': 0.0, 
                'income_tax': 14837.69
            }
        }

        files = ["./output_test/M-NORMAL-12-2020.json", 
                 "./output_test/M-COMPLEMENTAR-12-2020.json",
                 "./output_test/M-13-12-2020.json"]
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(2, len(employees))
        self.assertDictEqual(employees[0], expected)
        self.assertDictEqual(employees[1], second_expected)

    # Membros ativos com folha complementar, 13º e verbas indenizatórias
    def test_membros_ativos_verbas(self):
        self.maxDiff = None

        expected = {
            'reg': '3418723',
            'name': 'ADONIRAN LEMOS ALMEIDA FILHO',
            'role': 'PROMOTOR DE JUSTICA DE ENTRÂNCIA INICIAL',
            'type': 'membro',
            'workplace': 'PROMOTORIA DE JUSTIÇA DE PINHEIRO MACHADO',
            'active': True,
            'income': {
                'total': 76165.68,
                'wage': 51703.92,
                'perks': {
                    'total': 26472.47,
                    'Subsistence': 0.0,
                    'Food': 620.51,
                    'Transportation': 0.0,
                    'PreSchool': 0.0,
                    'Conversões em Pecúnia': 25851.96
                },
                'other': {
                    'total': -2010.71,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Gratificação Natalina': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Abono de Permanência': 0.0,
                        'Comissão Especial': 0.0,
                        'Gratificação Setor': 0.0, 
                        'Adicional Insal / Periculosidade': 0.0, 
                        'Difícil Provimento': 0.0, 
                        'Honorário Concurso': 0.0, 
                        'Substituição': 0.0, 
                        'Diretor Promotoria': 0.0, 
                        'Hora Extra': 0.0, 
                        'Acúmulo funções': -2010.71
                    }
                }
            },
            'discounts': {
                'total': 17348.24,
                'prev_contribution': 8017.9,
                'ceil_retention': 0.0,
                'income_tax': 9330.34
            }
        }

        second_expected = {
            'reg': '3427811',
            'name': 'BRUNO HERINGER JUNIOR', 
            'role': 'PROMOTOR DE JUSTICA DE ENTRÂNCIA FINAL', 
            'type': 'membro', 
            'workplace': 'SUBPROCURADORIA-GERAL DE JUSTIÇA PARA ASSUNTOS JURÍDICOS', 
            'active': True, 
            'income': {
                'total': 110275.57, 
                'wage': 63832.0, 
                'perks': {
                    'total': 36514.15,
                    'Subsistence': 0.0, 
                    'Food': 910.08, 
                    'Transportation': 0.0, 
                    'PreSchool': 0.0, 
                    'Conversões em Pecúnia': 35604.07
                }, 
                'other': {
                    'total': 9929.42, 
                    'trust_position': 6383.2, 
                    'others_total': 3546.22, 
                    'others': {
                        'Gratificação Natalina': 0.0, 
                        'Férias (1/3 constitucional)': 3546.22, 
                        'Abono de Permanência': 0.0,
                        'Comissão Especial': 0.0, 
                        'Gratificação Setor': 0.0, 
                        'Adicional Insal / Periculosidade': 0.0, 
                        'Difícil Provimento': 0.0, 
                        'Honorário Concurso': 0.0, 
                        'Substituição': 0.0, 
                        'Diretor Promotoria': 0.0, 
                        'Hora Extra': 0.0, 
                        'Acúmulo funções': 0.0
                    }
                }
            }, 
            'discounts': {
                'total': 25159.92, 
                'prev_contribution': 10322.23, 
                'ceil_retention': 0.0, 
                'income_tax': 14837.69
            }
        }

        files = ["./output_test/M-NORMAL-12-2020.json", 
                 "./output_test/M-COMPLEMENTAR-12-2020.json",
                 "./output_test/M-13-12-2020.json",
                 "./output_test/verbas_indenizatorias_temporarias-12-2020.html"]
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(2, len(employees))
        self.assertDictEqual(employees[0], expected)
        self.assertDictEqual(employees[1], second_expected)

    # Membros inativos sem folha complementar e de 13º
    def test_membros_inativos(self):
        self.maxDiff = None

        expected = {
            'reg': '3425568',
            'name': 'ANTÔNIO CEZAR LIMA DA FONSECA',
            'role': 'PROCURADOR DE JUSTICA',
            'type': 'membro',
            'workplace': 'INATIVOS',
            'active': False,
            'income': {
                'total': 40359.38,
                'wage': 35462.22,
                'perks': {
                    'total': 4897.16
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 12532.64,
                'prev_contribution': 5756.53,
                'ceil_retention': 0.0,
                'income_tax': 6776.11
            }  
        }

        files = ["./output_test/MI-NORMAL-12-2020.json"]
        employees = parser.parse(files)
        
        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # Membros inativos com folha complementar
    def test_membros_inativos_complementar(self):
        self.maxDiff = None

        expected = {
            'reg': '3425568',
            'name': 'ANTÔNIO CEZAR LIMA DA FONSECA',
            'role': 'PROCURADOR DE JUSTICA',
            'type': 'membro',
            'workplace': 'INATIVOS',
            'active': False,
            'income': {
                'total': 75821.6,
                'wage': 35462.22,
                'perks': {
                    'total': 40359.38
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 12532.64,
                'prev_contribution': 5756.53,
                'ceil_retention': 0.0,
                'income_tax': 6776.11
            }  
        }

        files = ["./output_test/MI-NORMAL-12-2020.json", 
                 "./output_test/MI-COMPLEMENTAR-12-2020.json"]
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # Membros inativos com folha complementar e 13º
    def test_membros_inativos_decimo(self):
        self.maxDiff = None

        expected = {
            'reg': '3425568',
            'name': 'ANTÔNIO CEZAR LIMA DA FONSECA',
            'role': 'PROCURADOR DE JUSTICA',
            'type': 'membro',
            'workplace': 'INATIVOS',
            'active': False,
            'income': {
                'total': 113341.31,
                'wage': 70924.43,
                'perks': {
                    'total': 40359.38
                },
                'other': {
                    'total': 2057.5,
                    'trust_position': 0.0,
                    'others_total': 2057.5,
                    'others': {
                        'Abono de Permanência': 2057.5,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 24525.37,
                'prev_contribution': 10768.37,
                'ceil_retention': 0.0,
                'income_tax': 13757.0
            }            
        }

        files = ["./output_test/MI-NORMAL-12-2020.json", 
                 "./output_test/MI-COMPLEMENTAR-12-2020.json",
                 "./output_test/MI-13-12-2020.json"]
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # Membros inativos com folha complementar, 13º e verbas indenizatórias
    # (Membros inativos não estão presentes na folha de verbas indenizatórias)
    def test_membros_inativos_verbas(self):
        self.maxDiff = None

        expected = {
            'reg': '3425568',
            'name': 'ANTÔNIO CEZAR LIMA DA FONSECA',
            'role': 'PROCURADOR DE JUSTICA',
            'type': 'membro',
            'workplace': 'INATIVOS',
            'active': False,
            'income': {
                'total': 113341.31,
                'wage': 70924.43,
                'perks': {
                    'total': 40359.38
                },
                'other': {
                    'total': 2057.5,
                    'trust_position': 0.0,
                    'others_total': 2057.5,
                    'others': {
                        'Abono de Permanência': 2057.5,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 24525.37,
                'prev_contribution': 10768.37,
                'ceil_retention': 0.0,
                'income_tax': 13757.0
            }            
        }

        files = ["./output_test/MI-NORMAL-12-2020.json",
                 "./output_test/MI-COMPLEMENTAR-12-2020.json",
                 "./output_test/MI-13-12-2020.json",
                 "./output_test/verbas_indenizatorias_temporarias-12-2020.html"]
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # Servidores ativos sem folha complementar e de 13º
    def test_servidores_ativos(self):
        self.maxDiff = None

        expected = {
            'reg': '3407373',
            'name': 'SHANNA CANTO BERNARDI DE FARIAS',
            'role': 'ASSESSOR BACHAREL EM CIENCIAS JURIDICAS E SOCIAIS - R',
            'type': 'servidor',
            'workplace': 'PROMOTORIA DE JUSTIÇA ESPECIALIZADA DE NOVO HAMBURGO',
            'active': True,
            'income': {
                'total': 21501.55,
                'wage': 12878.23,
                'perks': {
                    'total': 8623.32
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 3545.42,
                'prev_contribution': 1611.58,
                'ceil_retention': 0.0,
                'income_tax': 1933.84
            }
        }

        files = ("./output_test/S-NORMAL-12-2020.json",)
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # Servidores ativos com folha complementar
    def test_servidores_ativos_complementar(self):
        self.maxDiff = None

        expected = {
            'reg': '3407373',
            'name': 'SHANNA CANTO BERNARDI DE FARIAS',
            'role': 'ASSESSOR BACHAREL EM CIENCIAS JURIDICAS E SOCIAIS - R',
            'type': 'servidor',
            'workplace': 'PROMOTORIA DE JUSTIÇA ESPECIALIZADA DE NOVO HAMBURGO',
            'active': True,
            'income': {
                'total': 25526.0,
                'wage': 12878.23,
                'perks': {
                    'total': 12647.77
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 3545.42,
                'prev_contribution': 1611.58,
                'ceil_retention': 0.0,
                'income_tax': 1933.84
            }
        }

        files = ("./output_test/S-NORMAL-12-2020.json", 
                 "./output_test/S-COMPLEMENTAR-12-2020.json")
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # Servidores ativos com folha complementar e 13º
    def test_servidores_ativos_decimo(self):
        self.maxDiff = None

        expected = {
            'reg': '3407373',
            'name': 'SHANNA CANTO BERNARDI DE FARIAS',
            'role': 'ASSESSOR BACHAREL EM CIENCIAS JURIDICAS E SOCIAIS - R',
            'type': 'servidor',
            'workplace': 'PROMOTORIA DE JUSTIÇA ESPECIALIZADA DE NOVO HAMBURGO',
            'active': True,
            'income': {
                'total': 37599.35,
                'wage': 24951.58,
                'perks': {
                    'total': 12647.77
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 7164.62,
                'prev_contribution': 3223.16,
                'ceil_retention': 0.0,
                'income_tax': 3941.46
            }
        }

        files = ("./output_test/S-NORMAL-12-2020.json", 
                 "./output_test/S-COMPLEMENTAR-12-2020.json",
                 "./output_test/S-13-12-2020.json")
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # Servidores ativos com folha complementar, 13º e verbas indenizatórias
    def test_servidores_ativos_verbas(self):
        self.maxDiff = None

        expected = {
            'reg': '3407373',
            'name': 'SHANNA CANTO BERNARDI DE FARIAS',
            'role': 'ASSESSOR BACHAREL EM CIENCIAS JURIDICAS E SOCIAIS - R',
            'type': 'servidor',
            'workplace': 'PROMOTORIA DE JUSTIÇA ESPECIALIZADA DE NOVO HAMBURGO',
            'active': True,
            'income': {
                'total': 37599.35,
                'wage': 24951.58,
                'perks': {
                    'total': 12647.77,
                    'Subsistence': 0.0,
                    'Food': 574.42,
                    'Transportation': 0.0,
                    'PreSchool': 0.0,
                    'Conversões em Pecúnia': 12073.35
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0,
                        'Comissão Especial': 0.0,
                        'Gratificação Setor': 0.0,
                        'Adicional Insal / Periculosidade': 0.0,
                        'Difícil Provimento': 0.0,
                        'Honorário Concurso': 0.0,
                        'Substituição': 0.0,
                        'Diretor Promotoria': 0.0,
                        'Hora Extra': 0.0,
                        'Acúmulo funções': 0.0
                    }
                }
            },
            'discounts': {
                'total': 7164.62,
                'prev_contribution': 3223.16,
                'ceil_retention': 0.0,
                'income_tax': 3941.46
            }
        }

        files = ["./output_test/S-NORMAL-12-2020.json",
                 "./output_test/S-COMPLEMENTAR-12-2020.json",
                 "./output_test/S-13-12-2020.json",
                 "./output_test/verbas_indenizatorias_temporarias-12-2020.html"]
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # Servidores inativos sem folha complementar e de 13º
    def test_servidores_inativos(self):
        self.maxDiff = None

        expected = {
            'reg': '3426602',
            'name': 'SANDRA MARIA PEIXOTO MEIRELLES',
            'role': 'SECRETARIO DE DILIGENCIAS - O',
            'type': 'servidor',
            'workplace': 'INATIVOS',
            'active': False,
            'income': {
                'total': 27797.61,
                'wage': 21607.32,
                'perks': {
                    'total': 6190.29
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 8007.44,
                'prev_contribution': 3793.92,
                'ceil_retention': 0.0,
                'income_tax': 4213.52
            }  
        }

        files = ["./output_test/SI-NORMAL-12-2020.json"]
        employees = parser.parse(files)
        
        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # Servidores inativos com folha complementar
    def test_servidores_inativos_complementar(self):
        self.maxDiff = None

        expected = {
            'reg': '3426602',
            'name': 'SANDRA MARIA PEIXOTO MEIRELLES',
            'role': 'SECRETARIO DE DILIGENCIAS - O',
            'type': 'servidor',
            'workplace': 'INATIVOS',
            'active': False,
            'income': {
                'total': 51379.65,
                'wage': 21607.32,
                'perks': {
                    'total': 29772.33
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 8007.44,
                'prev_contribution': 3793.92,
                'ceil_retention': 0.0,
                'income_tax': 4213.52
            }  
        }

        files = ["./output_test/SI-NORMAL-12-2020.json", 
                 "./output_test/SI-COMPLEMENTAR-12-2020.json"]
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # Servidores inativos com folha complementar e 13º
    def test_servidores_inativos_decimo(self):
        self.maxDiff = None

        expected = {
            'reg': '3426602',
            'name': 'SANDRA MARIA PEIXOTO MEIRELLES',
            'role': 'SECRETARIO DE DILIGENCIAS - O',
            'type': 'servidor',
            'workplace': 'INATIVOS',
            'active': False,
            'income': {
                'total': 72986.97,
                'wage': 43214.64,
                'perks': {
                    'total': 29772.33
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 15345.06,
                'prev_contribution': 6918.02,
                'ceil_retention': 0.0,
                'income_tax': 8427.04
            }  
        }

        files = ["./output_test/SI-NORMAL-12-2020.json", 
                 "./output_test/SI-COMPLEMENTAR-12-2020.json",
                 "./output_test/SI-13-12-2020.json"]
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # Servidores inativos com folha complementar, 13º e verbas indenizatórias
    def test_servidores_inativos_verbas(self):
        self.maxDiff = None

        expected = {
            'reg': '3426602',
            'name': 'SANDRA MARIA PEIXOTO MEIRELLES',
            'role': 'SECRETARIO DE DILIGENCIAS - O',
            'type': 'servidor',
            'workplace': 'INATIVOS',
            'active': False,
            'income': {
                'total': 72986.97,
                'wage': 43214.64,
                'perks': {
                    'total': 29772.33
                },
                'other': {
                    'total': 0.0,
                    'trust_position': 0.0,
                    'others_total': 0.0,
                    'others': {
                        'Abono de Permanência': 0.0,
                        'Férias (1/3 constitucional)': 0.0,
                        'Gratificação Natalina': 0.0
                    }
                }
            },
            'discounts': {
                'total': 15345.06,
                'prev_contribution': 6918.02,
                'ceil_retention': 0.0,
                'income_tax': 8427.04
            }  
        }

        files = ["./output_test/SI-NORMAL-12-2020.json",
                 "./output_test/SI-COMPLEMENTAR-12-2020.json",
                 "./output_test/SI-13-12-2020.json",
                 "./output_test/verbas_indenizatorias_temporarias-12-2020.html"]
        employees = parser.parse(files)

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

if __name__ == '__main__':
    unittest.main()
