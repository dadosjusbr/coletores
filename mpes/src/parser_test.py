import os
import parser
import unittest

class TestParser(unittest.TestCase):

    #O propósito deste teste é verificar a execução para meses anteriores á ago/2019
    def test_membros_jan_2019(self):
        self.maxDiff = None

        expected = {
            'reg': 'ZENALDO BAPTISTA DE SOUSA',
            'name': 'ZENALDO BAPTISTA DE SOUSA',
            'role': 'PROMOTOR DE JUSTIÇA',
            'type': 'membro',
            'workplace': 'PJ DE CASTELO',
            'active': True,
            'income': {
                'total': 57054.85,
                'wage': 35710.46,
                'perks': {
                    'total': 0.00,
                },
                'other': {
                    'total': 21344.39,
                    'trust_position': 0.00,
                    'others_total': 21344.39,
                    'others': {
                        '13º VENCIMENTO': 0.00,
                        'Férias (1/3 constitucional)': 0.00,
                        'Abono de permanência': 0.00,
                        'VERBAS INDENIZATÓRIAS 1': 21344.39,
                        'VERBAS INDENIZATÓRIAS 2': 0.00,
                        'REMUNERAÇÃO TEMPORÁRIA 1': 0.00,
                        'REMUNERAÇÃO TEMPORÁRIA 2': 0.00,

                    },
            },
        },
            'discounts': {
                'total': 11637.72,
                'prev_contribution': 3705.8,
                'ceil_retention': 0.00,
                'income_tax': 7931.92,
            }
    }
        files = ('./output_test/2019_01_remu.xlsx',
                 './output_test/2019_01_vi.xlsx')
        employees = parser.parse(files,'2019','01')

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)
    
    #O propósito deste teste é verificar a execução para os meses agosto, setembro e outubro de 2019
    def test_membros_aug_2019(self):
        self.maxDiff = None

        expected = {'reg': '1010', 'name': 'ALEX ITIBERÊ RODRIGUES DE CASTRO CAIADO', 'role': 'PROMOTOR DE JUSTIÇA', 'type': 'membro', 'workplace': 'PJ DA INFÂNCIA E JUVENTUDE DE GUARAPARI', 'active': True, 'income': {'total': 42474.54, 'wage': 36384.24, 'perks': {'total': 2721.39, 'food': 2240.33, 'health': 481.06}, 'other': {'total': 3368.91, 'trust_position': 0.0, 'eventual_benefits': 2245.94, 'others_total': 1122.97, 'others': {'Gratificação Natalina': 0.0, 'Férias (1/3 constitucional)': 0.0, 'Abono de permanência': 0.0, 'Plantão': 1122.97}}}, 'discounts': {'total': 12131.83, 'prev_contribution': 3705.8, 'ceil_retention': 0, 'income_tax': 8426.03}}
        files = ('./output_test/2019_08_remu.xlsx',
                 './output_test/2019_08_vi.xlsx')
        employees = parser.parse(files,'2019','08')

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)
    
    #O propósito deste teste é verificar a execução para novembro de 2019
    def test_membros_nov_2019(self):
        self.maxDiff = None

        expected = {'reg': '1001', 'name': 'ADELCION CALIMAN', 'role': 'PROMOTOR DE JUSTIÇA', 'type': 'membro', 'workplace': 'PJ CRIMINAL DE VITÓRIA', 'active': True, 'income': {'total': 74142.3, 'wage': 33876.27, 'perks': {'total': 36560.23, 'vacation': 33838.84, 'food': 2240.33, 'health': 481.06}, 'other': {'total': 3705.8, 'trust_position': 0.0, 'eventual_benefits': 0.0, 'others_total': 3705.8, 'others': {'Gratificação Natalina': 0.0, 'Férias (1/3 constitucional)': 0.0, 'Abono de permanência': 3705.8, 'Plantão': 0}}}, 'discounts': {'total': 10182.53, 'prev_contribution': 3705.8, 'ceil_retention': 0, 'income_tax': 6476.73}}
        files = ('./output_test/2019_11_remu.xlsx',
                 './output_test/2019_11_vi.xlsx')
        employees = parser.parse(files,'2019','11')

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)
    
    #O propósito deste teste é verificar a execução para dezembro de 2019
    def test_membros_dez_2019(self):
        self.maxDiff = None

        expected = {'reg': '1001', 'name': 'ADELCION CALIMAN', 'role': 'PROMOTOR DE JUSTIÇA', 'type': 'membro', 'workplace': 'PJ CRIMINAL DE VITÓRIA', 'active': True, 'income': {'total': 92450.05, 'wage': 33745.26, 'perks': {'total': 34181.93, 'vacation': 31443.17, 'food': 2240.33, 'health': 498.43, 'subsistence': 0}, 'other': {'total': 24522.86, 'trust_position': 0.0, 'eventual_benefits': 0.0, 'others_total': 24522.86, 'others': {'Gratificação Natalina': 17111.26, 'Férias (1/3 constitucional)': 0.0, 'Abono de permanência': 7411.6, 'Plantão': 0}}}, 'discounts': {'total': 20798.17, 'prev_contribution': 7411.6, 'ceil_retention': 0, 'income_tax': 13386.57}}
        files = ('./output_test/2019_12_remu.xlsx',
                 './output_test/2019_12_vi.xlsx')
        employees = parser.parse(files,'2019','12')

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # def test_membros_jan_2020(self):
    #     self.maxDiff = None

    #     expected = {
    #         'reg': '1001',
    #         'name': 'ADELCION CALIMAN',
    #         'role': 'PROMOTOR DE JUSTIÇA',
    #         'type': 'membro',
    #         'workplace': 'PJ CRIMINAL DE VITÓRIA',
    #         'active': True,
    #         'income': {
    #             'total': 57273.23,
    #             'wage': 33689.11,
    #             'perks': {
    #                 'total': 3033.76,
    #                 'food': 2240.33,
    #                 'health': 793.43,
    #             },
    #             'other': {
    #                 'total': 20550.36,
    #                 'trust_position': 0.00,
    #                 'others_total': 20550.36,
    #                 'eventual_benefits': 0.00,
    #                 'others': {
    #                     'Gratificação Natalina': 0.00,
    #                     'Férias (1/3 constitucional)': 16844.56,
    #                     'Abono de permanência': 3705.8,
    #                     'ABONO  FÉR. IND. EX. ANT': 0.00,
    #                     'Plantão': 0.00,
    #                 },
    #         },
    #     },
    #         'discounts': {
    #             'total': 13305.27,
    #             'prev_contribution': 3705.8,
    #             'ceil_retention': 0.00,
    #             'income_tax': 9599.47,
    #         }
    # }
    #     files = ('./output_test/2020_01_remu.xlsx',
    #              './output_test/2020_01_vi.xlsx')
    #     employees = parser.parse(files,'2020','01')
    #     print(employees)

    #     # Verificações
    #     self.assertEqual(1, len(employees))
    #     self.assertDictEqual(employees[0], expected)

    #O propósito deste teste é verificar a execução para meses anteriores á ago/2019
    

    # #Este teste é destinado a verificar se ocorre de acordo com o esperado para os meses de abril - jul de 2020
    # def test_membros_abr_2020(self):
    #     self.maxDiff = None

    #     expected = {
    #         'reg': '1408',
    #         'name': 'WAGNER EDUARDO VASCONCELLOS',
    #         'role': 'PROMOTOR DE JUSTIÇA',
    #         'type': 'membro',
    #         'workplace': 'PJ CÍVEL DE CACHOEIRO DE ITAPEMIRIM',
    #         'active': True,
    #         'income': {
    #             'total': 35485.87,
    #             'wage': 33689.11,
    #             'perks': {
    #                 'total': 3390.42,
    #                 'food': 2240.33,
    #                 'health': 1150.09,
    #             },
    #             'other': {
    #                 'total': 0.00,
    #                 'trust_position': 0.00,
    #                 'others_total': 0.00,
    #                 'eventual_benefits': 0.00,
    #                 'others': {
    #                     'Gratificação Natalina': 0.00,
    #                     'Férias (1/3 constitucional)': 0.00,
    #                     'Abono de permanência': 0.00,
    #                     'Plantão': 0.00,
    #                 },
    #         },
    #     },
    #         'discounts': {
    #             'total': 12308.7,
    #             'prev_contribution': 4716.48,
    #             'ceil_retention': 0.0,
    #             'income_tax': 7592.22,
    #         }
    # }
    #     files = ('./output_test/2020_04_remu.xlsx',
    #              './output_test/2020_04_vi.xlsx')
    #     employees = parser.parse(files,'2020','04')

    #     # Verificações
    #     self.assertEqual(1, len(employees))
    #     self.assertDictEqual(employees[0], expected)

    

if __name__ == '__main__':
    unittest.main()
