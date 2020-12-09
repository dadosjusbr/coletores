import os
import parser
import unittest

MONTH = 2
YEAR = 2019

# Como não será utilizado todos os dados que estão na planilha, separamos esses arquivos para realizar os testes
FILE_NAMES = ['/output_test/Membros ativos-1-2020.xlsx', '/output_test/Membros inativos-1-2020.xlsx', '/output_test/Servidores ativos-1-2020.xlsx', '/output_test/Servidores inativos-1-2020.xlsx', '/output_test/Pensionistas-1-2020.xlsx', '/output_test/Colaboradores-1-2020.xlsx', '/output_test/Membros ativos-Verbas Indenizatorias-1-2020.xlsx', '/output_test/Membros inativos-Verbas Indenizatorias-1-2020.xlsx', '/output_test/Servidores ativos-Verbas Indenizatorias-1-2020.xlsx', '/output_test/Servidores inativos-Verbas Indenizatorias-1-2020.xlsx', '/output_test/Pensionistas-Verbas Indenizatorias-1-2020.xlsx', '/output_test/Colaboradores-Verbas Indenizatorias-1-2020.xlsx']
 
# Saída esperada para um determinado membro ativo
expected_membros_ativos = [{'reg': '1191-6', 'name': 'ADILSON JOSE GUTIERREZ', 'role': 'PROMOTOR DE JUSTICA MILITAR', 'type': 'membros ativos ', 
                            'workplace': '1ª PROCURADORIA DE JUSTIÇA MILITAR EM SÃO PAULO/SP', 'active': True, 'income': {'total': 52059.5, 
                            'wage': 33689.11, 'perks': {'total': 910.08, 'food': 910.08, 'transportation': 0, 'birth_aid': 0, 'housing_aid': 0}, 
                            'other': {'total': 0, 'eventual_benefits': 11229.7, 'trust_position': 0, 'gratification': 16844.55, 'others_total': 0, 
                            'others': 0}}, 'discounts': {'total': 14319.74, 'prev_contribution': 3705.8, 'cell_retention': 0, 'income_tax': 10613.94}}]

# Saída esperada para um determinado membro inativo
expected_membros_inativos = [{'reg': '0004-3', 'name': 'ANETE VASCONCELOS DE BORBOREMA', 'role': 'SUBPROCURADOR-GERAL DA JUSTIÇA MILITAR', 
                            'type': 'membros inativos ', 'workplace': 'APOSENTADOS/INATIVOS', 'active': False, 'income': {'total': 44630.55, 
                            'wage': 37328.65, 'perks': {'total': 0, 'food': 0, 'transportation': 0, 'birth_aid': 0, 'housing_aid': 0}, 
                            'other': {'total': 0, 'eventual_benefits': 0, 'trust_position': 0, 'gratification': 18664.32, 'others_total': 0, 'others': 0}}, 
                            'discounts': {'total': 11362.42, 'prev_contribution': 3434.48, 'cell_retention': 0, 'income_tax': 7927.94}}]

test_crawler_result = parser.crawler_result(YEAR, MONTH, FILE_NAMES)
employee = test_crawler_result['employees']
membros_ativos = employee[0]
membros_inativos = employee[1]

class TestParser(unittest.TestCase):
      
    def test_membros_ativos(self):
        self.assertTrue(membros_ativos == expected_membros_ativos)
    
    def test_membros_inativos(self):
        self.assertTrue(membros_inativos == expected_membros_inativos)

if __name__ == '__main__':
    unittest.main()