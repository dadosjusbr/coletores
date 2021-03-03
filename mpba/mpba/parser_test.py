import os
import unittest
import sys 
from parser import parse

class Tests(unittest.TestCase):

    expected = {
            'reg': 904023,
            'name': "IGOR ANDREYSON MENDES LOPES",
            'role': "DIGITADOR",
            'type': 'servidor',
            'workplace': "PJR DE PAULO AFONSO - APOIO TECNICO E ADMINISTRATIVO",
            'active': True,
            'income': {
                'total': 31787.14,
                'wage': 6392.39,
                'perks': {
                    'total': 1300.0,
                    'vacation': 0.0,
                },
                'other': {
                    'total': 24094.75,
                    "personal_benefits": 0.0,
                    "eventual_benefits": 1300.0,
                    "trust_position": 7093.93,
                    "gratification": 0.00,
                    "origin_pos": 15243.57,
                    "others_total": 457.25,
                    'others': {
                        "vlOutrasRemun": 0.0,
                    }}
            },
            'discounts': {
                'total': 4380.39,
                'prev_contribution': 1952.1,
                'ceil_retention': 0.0,
                'income_tax': 2428.29
            }
        } 
    #Teste voltado a verificar se a saída do parser segue os parâmetros desejados
    def test_parser_result(self):
        self.maxDiff = None

        filepath = './tests/output_test/mpba-1-2020.json'
        employees = parse(filepath)
        
        #Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], self.expected)

if __name__ == '__main__':
    unittest.main()