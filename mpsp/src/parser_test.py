import os
import parser
import unittest


class TestParser(unittest.TestCase):

    # Tests for parsers for the months from July 2019 to November 2020 
    def test_membros_ativos(self):
        self.maxDiff = None

        expected = {'reg': '3725', 'name': 'ABNER CASTORINO', 'role': 'PROMOTOR DE JUSTICA (ENTRANCIA FINAL)', 'type': 'membro', 'workplace': 'PROMOTORIA DE JUSTICA DE SAO BERNARDO DO CAMPO', 'active': True, 'income': {'total': 40253.32, 'wage': 33689.1, 'perks': {'total': 960.0}, 'other': {
            'total': 5604.22, 'trust_position': 0.0, 'others_total': 5604.22, 'others': {'Gratificação Natalina': 0.0, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporárias': 5604.22}}}, 'discounts': {'total': 12623.0, 'prev_contribution': 3705.8, 'ceil_retention': 0.0, 'income_tax': 8917.2}}

        files = ('./output_test/Membros_ativos-01-2020.ods',)
        employees = parser.parse(files, "01", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_inativos(self):
        self.maxDiff = None

        expected = {'reg': '137707', 'name': 'ABEL PEDRO RIBEIRO', 'role': 'PROMOTOR DE JUSTICA (ENTRANCIA FINAL)', 'type': 'membro', 'workplace': 'PROMOTORIAS DE JUSTICA', 'active': False, 'income': {'total': 52739.74, 'wage': 35159.83, 'perks': {'total': 0.0}, 'other':
                                                                                                                                                                                                         {'total': 17579.91, 'trust_position': 0.0, 'others_total': 17579.91, 'others':
                                                                                                                                                                                                          {'Gratificação Natalina': 17579.91, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporárias': 0.0}}},
                    'discounts': {'total': 11884.88, 'prev_contribution': 4487.91, 'ceil_retention': 0.0, 'income_tax': 7396.97}}

        files = ('./output_test/Membros_inativos-01-2020.ods',)
        employees = parser.parse(files, "01", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_servidores_inativos(self):
        self.maxDiff = None

        expected = {'reg': '1174', 'name': 'ABIGAIR MONTEIRO', 'role': 'OFICIAL DE PROMOTORIA I', 'type': 'servidor', 'workplace': 'AREA REGIONAL DE SAO JOSE DO RIO PRETO', 'active': False, 'income': {'total': 8458.57, 'wage': 8458.57, 'perks': {'total': 0.0}, 'other': {'total': 0.0, 'trust_position': 0.0,
                                                                                                                                                                                                                                                                                 'others_total': 0.0, 'others': {'Gratificação Natalina': 0.0, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporárias': 0.0}}}, 'discounts': {'total': 1372.38, 'prev_contribution': 604.18, 'ceil_retention': 0.0, 'income_tax': 768.2}}

        files = ('./output_test/Servidores_inativos-01-2020.ods', )
        employees = parser.parse(files, "01", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_servidores_ativos(self):
        self.maxDiff = None

        expected = {'reg': '1469', 'name': 'ABEL VIEIRA DE MENEZES FILHO', 'role': ' AUXILIAR DE PROMOTORIA I ', 'type': 'servidor', 'workplace': ' AREA REGIONAL DA CAPITAL ', 'active': True, 'income': {'total': 7874.06, 'wage': 6623.36, 'perks': {'total': 1250.7}, 'other': {'total': 0.0, 'trust_position': 0.0,
                                                                                                                                                                                                                                                                                    'others_total': 0.0, 'others': {'Gratificação Natalina': 0.0, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporárias': 0.0}}}, 'discounts': {'total': 1612.73, 'prev_contribution': 861.02, 'ceil_retention': 0.0, 'income_tax': 751.71}}

        files = ('./output_test/Servidores_ativos-01-2020.ods', )
        employees = parser.parse(files, "01", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # Tests for active members who have different table formats

    def test_active_members_january_2019(self):
        self.maxDiff = None

        expected = {'reg': '3725', 'name': 'ABNER CASTORINO', 'role': 'PROMOTOR DE JUSTICA (ENTRANCIA FINAL)', 'type': 'membro', 'workplace': 'PROMOTORIA DE JUSTICA DE SAO BERNARDO DO CAMPO', 'active': True, 'income': {'total': 33689.1, 'wage': 33689.1, 'perks': {'total': 920.0, 'food': 920.0, 'housing_aid': 0.0}, 'other': {
            'total': 0.0, 'trust_position': 0.0, 'others_total': 0.0, 'others': {'Gratificação Natalina': 0.0, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporárias': 0.0}}}, 'discounts': {'total': 11081.84, 'prev_contribution': 3705.8, 'ceil_retention': 0.0, 'income_tax': 7376.04}}

        files = ('./output_test/Membros_ativos-01-2019.ods', )
        employees = parser.parse(files, "01", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_members_march_2019(self):
        self.maxDiff = None

        expected = {'reg': '3725', 'name': 'ABNER CASTORINO', 'role': 'PROMOTOR DE JUSTICA (ENTRANCIA FINAL)', 'type': 'membro', 'workplace': 'PROMOTORIA DE JUSTICA DE SAO BERNARDO DO CAMPO', 'active': True, 'income': {'total': 33689.1, 'wage': 33689.1, 'perks': {'total': 920.0, 'food': 920.0, 'ferias em pecunia': 0.0}, 'other': {
            'total': 4042.68, 'trust_position': 0.0, 'others_total': 4042.68, 'others': {'Gratificação Natalina': 0.0, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporárias': 4042.68}}}, 'discounts': {'total': 12193.58, 'prev_contribution': 3705.8, 'ceil_retention': 0.0, 'income_tax': 8487.78}}

        files = ('./output_test/Membros_ativos-03-2019.ods', )
        employees = parser.parse(files, "03", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_members_june_2019(self):
        self.maxDiff = None

        expected = {'reg': '207', 'name': 'FREDERICO AUGUSTO NEVES ARAUJO', 'role': 'PROMOTOR DE JUSTICA (ENTRANCIA FINAL)', 'type': 'membro', 'workplace': 'PROMOTORIA DE JUSTICA DE TAUBATE', 'active': True, 'income': {'total': 33689.1, 'wage': 33689.1, 'perks': {'total': 920.0, 'food': 920.0, 'ferias em pecunia': 0.0, 'LP em pecunia': 0.0}, 'other': {
            'total': 0.0, 'trust_position': 0.0, 'others_total': 0.0, 'others': {'Gratificação Natalina': 0.0, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporarias': 0.0}}}, 'discounts': {'total': 11081.84, 'prev_contribution': 3705.8, 'income_tax': 7376.04}}

        files = ('./output_test/Membros_ativos-06-2019.ods', )
        employees = parser.parse(files, "06", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == '__main__':
    unittest.main()
