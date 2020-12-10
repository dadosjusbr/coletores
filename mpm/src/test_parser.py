import os
import parser
import unittest

MONTH = 2
YEAR = 2019

# Como não será utilizado todos os dados que estão na planilha, separamos esses arquivos para realizar os testes
FILE_NAMES = ['/output_test/Membros ativos-1-2020.xlsx', '/output_test/Membros inativos-1-2020.xlsx', '/output_test/Servidores ativos-1-2020.xlsx', '/output_test/Servidores inativos-1-2020.xlsx', '/output_test/Pensionistas-1-2020.xlsx', '/output_test/Colaboradores-1-2020.xlsx', '/output_test/Membros ativos-Verbas Indenizatorias-1-2020.xlsx', '/output_test/Membros inativos-Verbas Indenizatorias-1-2020.xlsx', '/output_test/Servidores ativos-Verbas Indenizatorias-1-2020.xlsx', '/output_test/Servidores inativos-Verbas Indenizatorias-1-2020.xlsx', '/output_test/Pensionistas-Verbas Indenizatorias-1-2020.xlsx', '/output_test/Colaboradores-Verbas Indenizatorias-1-2020.xlsx']
 
# Saídas esperadas
expected_membros_ativos = [{'reg': '1191-6', 'name': 'ADILSON JOSE GUTIERREZ', 'role': 'PROMOTOR DE JUSTICA MILITAR', 'type': 'membro', 
                            'workplace': '1ª PROCURADORIA DE JUSTIÇA MILITAR EM SÃO PAULO/SP', 'active': True, 'income': {'total': 52059.5, 
                            'wage': 33689.11, 'perks': {'total': 910.08, 'food': 910.08, 'transportation': 0, 'birth_aid': 0, 'housing_aid': 0}, 
                            'other': {'total': 28074.25, 'eventual_benefits': 11229.7, 'trust_position': 0, 'gratification': 16844.55, 'others_total': 0, 
                            'others': 0}}, 'discounts': {'total': 14319.74, 'prev_contribution': 3705.8, 'ceil_retention': 0, 'income_tax': 10613.94}}]

expected_membros_inativos = [{'reg': '0004-3', 'name': 'ANETE VASCONCELOS DE BORBOREMA', 'role': 'SUBPROCURADOR-GERAL DA JUSTIÇA MILITAR', 
                            'type': 'membro', 'workplace': 'APOSENTADOS/INATIVOS', 'active': False, 'income': {'total': 44630.55, 
                            'wage': 37328.65, 'perks': {'total': 0, 'food': 0, 'transportation': 0, 'birth_aid': 0, 'housing_aid': 0}, 
                            'other': {'total': 18664.32, 'eventual_benefits': 0, 'trust_position': 0, 'gratification': 18664.32, 'others_total': 0, 'others': 0}}, 
                            'discounts': {'total': 11362.42, 'prev_contribution': 3434.48, 'ceil_retention': 0, 'income_tax': 7927.94}}]

expected_servidores_ativos = [{'reg': '0376-0', 'name': 'ABEL DA COSTA VALE NETO', 'role': 'TECNICO DO MPU/ADMINISTRAÇÃO', 'type': 'servidor',
                             'workplace': 'COORDENADORIA ADMINISTRATIVA DO PLAN-ASSISTE', 'active': True, 'income': {'total': 27232.94, 'wage': 11992.04,
                             'perks': {'total': 2928.98, 'food': 910.08, 'transportation': 484.93, 'birth_aid': 0, 'housing_aid': 0}, 'other': {'total': 18298.66, 
                             'eventual_benefits': 5185.32, 'trust_position': 3563.93, 'gratification': 7777.98, 'others_total': 1533.97, 'others': 237.46}}, 
                             'discounts': {'total': 4452.77, 'prev_contribution': 1319.12, 'ceil_retention': 0, 'income_tax': 3133.65}}]

expected_servidores_inativos = [{'reg': '1103-7', 'name': 'ALBA REGINA BITENCOURT PEREIRA', 'role': 'TECNICO DO MPU/ADMINISTRAÇÃO', 'type': 'servidor', 'workplace': 'APOSENTADOS/INATIVOS', 
                            'active': False, 'income': {'total': 15453.4, 'wage': 11754.58, 'perks': {'total': 0, 'food': 0, 'transportation': 0, 'birth_aid': 0, 'housing_aid': 0}, 
                            'other': {'total': 6709.17, 'eventual_benefits': 0, 'trust_position': 0, 'gratification': 6154.58, 'others_total': 0, 'others': 554.59}}, 'discounts': 
                            {'total': 3010.35, 'prev_contribution': 682.33, 'ceil_retention': 0, 'income_tax': 2328.02}}]

expected_pensionistas = [{'reg': '1522-9', 'name': 'ABRAAO ANTONIO XAVIER DINIZ', 'role': 'PENSÃO CIVIL', 'type': 'pensionista', 'workplace': 'PENSÃO ESPECIAL', 'active': True, 'income': 
                        {'total': 4030.39, 'wage': 2860.13, 'perks': {'total': 0, 'food': 0, 'transportation': 0, 'birth_aid': 0, 'housing_aid': 0}, 'other': {'total': 1377.66, 
                        'eventual_benefits': 0, 'trust_position': 0, 'gratification': 1377.66, 'others_total': 0, 'others': 0}}, 'discounts': {'total': 207.4, 'prev_contribution': 146.7, 
                        'ceil_retention': 0, 'income_tax': 60.7}}]

expected_colaboradores = [{'reg': '7822-1', 'name': 'ANA VICTÓRIA DE PAULA SANTOS GUIMARÃES', 'role': 'ESTAGIÁRIO', 'type': 'indefinido', 'workplace': '5ª PROCURADORIA DE JUSTIÇA MILITAR NO RIO DE JANEIRO/RJ', 
                        'active': True, 'income': {'total': 983, 'wage': 850, 'perks': {'total': 133, 'food': 0, 'transportation': 133, 'birth_aid': 0, 'housing_aid': 0}, 'other': {'total': 0, 'eventual_benefits': 0, 
                        'trust_position': 0, 'gratification': 0, 'others_total': 0, 'others': 0}}, 'discounts': {'total': 0, 'prev_contribution': 0, 'ceil_retention': 0, 'income_tax': 0}}]

class TestParser(unittest.TestCase):

    test_crawler_result = parser.crawler_result(YEAR, MONTH, FILE_NAMES)
    employee = test_crawler_result['employees']
    
    def test_membros_ativos(self):
        membros_ativos = self.employee[0]
        # Verifica se contêm apenas 1 servidor do grupo membros ativos.
        self.assertEqual(1, len(membros_ativos))
        # Verifica se o resultado do parser para os membros ativos é igual ao resultado esperado.
        self.assertEqual(membros_ativos, expected_membros_ativos)
    
    def test_membros_inativos(self):
        membros_inativos = self.employee[1]
        self.assertEqual(1, len(membros_inativos))
        self.assertEqual(membros_inativos, expected_membros_inativos)

    def test_servidores_ativos(self):
        servidores_ativos = self.employee[2]
        self.assertEqual(1, len(servidores_ativos))
        self.assertEqual(servidores_ativos, expected_servidores_ativos)

    def test_servidores_inativos(self):
        servidores_inativos = self.employee[3]
        self.assertEqual(1, len(servidores_inativos))
        self.assertEqual(servidores_inativos, expected_servidores_inativos)

    def test_pensionistas(self):
        pensionistas = self.employee[4]
        self.assertEqual(1, len(pensionistas))
        self.assertEqual(pensionistas, expected_pensionistas)
         
    def test_colaboradores(self):
        colaboradores = self.employee[5]
        self.assertEqual(1, len(colaboradores))
        self.assertEqual(colaboradores, expected_colaboradores)

if __name__ == '__main__':
    unittest.main()