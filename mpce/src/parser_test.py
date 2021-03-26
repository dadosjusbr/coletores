import os
import parser
import unittest

class TestParser(unittest.TestCase):

    def test_membros_jan_2020(self):
        self.maxDiff = None

        expected = {
            'reg': "13861218",
            'name': "YTHALO FROTA LOUREIRO          ",
            'role': "   PROMOTOR JUST. ENT. FINAL  ",
            'type': 'membro',
            'workplace': "   111ª Promotoria de Justiça de Fortaleza ",
            'active': True,
            "income":
            {
                'total': 38920.04,
                'wage': 33689.11,
                'perks':{
                    'total': 1188.24,
                    'food': 1188.24,
                    'pre_school': 0.0,
                },
                'other':
                { 
                    'total': 4042.69,
                    'trust_position': 0.00,
                    'others_total': 4042.69,
                    'others': {
                        'Gratificação Natalina': 0.00,
                        'Férias (1/3 constitucional)': 0.00,
                        'Abono de permanência': 0.00,
                        'A.C. PROMOÇÃO': 0.00,
                        'A.C. DESLOCAMENTO': 0.00,
                        'A.C.F MESES ANTERIORES': 0.00,
                        'A.C.F MÊS CORRENTE': 4042.69,
                        'DIF. AUX. ALIMENTAÇÃO': 0.00,
                        'HORA EXTRA / SERVICO EXTRAORDINÁRIO': 0.00,
                        'DIF. DE SUBSÍDIO': 0.00,
                        'DIF. DE SUBSÍDIO POR SUBSTITUIÇÃO': 0.00,
                        'DIF. DE SUBSÍDIO SUBSTITUIÇÃO (MESES ANT.)': 0.00,
                        'DIF. DE SUBSÍDIO AFASTAMENTO': 0.00,
                        'GRAT.DE REPRES. DE GABINETE': 0.00,
                        'GRAT.REP.GABINETE POR ASSESSORAMENTO': 0.00,
                        'DIF.GRATIFICAÇÃO T.T.R': 0.00,
                        'GRAT.POR ENCARGO DE LICITAÇÃO - Presidente comitê': 0.00,
                        'GRAT.POR ENCARGO DE LICITAÇÃO - Pregoeiro': 0.00,
                        'GRAT.POR ENCARGO DE LICITAÇÃO - Membros Titular': 0.00,
                        'GRAT.POR ENCARGO DE LICITAÇÃO - Equipe de Apoio': 0.00,
                        'GRAT.TRAB.TEC./REL./CIENTIFICO - TTR': 0.00,
                        'DIF. DE GRAT.DE GABINETE': 0.00,
                    }
                },

            },
            'discounts':
            {
                'total': 12926.32,
                'prev_contribution': 4716.47,
                'ceil_retention': 0.00,
                'income_tax': 8209.85,
            }
        }

        files = ['./output_test/2020_01_remu.html','./output_test/2020_02_vi.html']
        employees = parser.parse(files)

        #Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

if __name__ == '__main__':
    unittest.main()