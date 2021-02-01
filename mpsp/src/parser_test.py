import os
import parser
import unittest


class TestParser(unittest.TestCase):

    # Tests for parsers for the months from July 2019 to November 2020
    def test_membros_ativos_jan_2020(self):
        self.maxDiff = None

        expected = {'reg': '3725', 'name': 'ABNER CASTORINO', 'role': 'PROMOTOR DE JUSTICA (ENTRANCIA FINAL)', 'type': 'membro', 'workplace': 'PROMOTORIA DE JUSTICA DE SAO BERNARDO DO CAMPO', 'active': True, 'income': {'total': 40253.32, 'wage': 33689.1, 'perks': {'total': 960.0}, 'other': {
            'total': 5604.22, 'trust_position': 0.0, 'others_total': 5604.22, 'others': {'Gratificação Natalina': 0.0, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporárias': 5604.22}}}, 'discounts': {'total': 12623.0, 'prev_contribution': 3705.8, 'ceil_retention': 0.0, 'income_tax': 8917.2}}

        files = ('./output_test/Membros_ativos-01-2020.ods',)
        employees = parser.parse(files, "01", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_ativos_dez_2019(self):
        self.maxDiff = None

        expected = {'reg': '2970', 'name': 'ADINAN APARECIDO DE OLIVEIRA', 'role': 'PROMOTOR DE JUSTICA (ENTRANCIA FINAL)', 'type': 'membro', 'workplace': 'PROMOTORIA DE JUSTICA DE JABOTICABAL', 'active': True, 'income': {'total': 89843.27, 'wage': 33689.1, 'perks': {'total': 33900.45}, 'other': {
            'total': 22253.72, 'trust_position': 0.0, 'others_total': 22253.72, 'others': {'Gratificação Natalina': 22253.72, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporárias': 0.0}}}, 'discounts': {'total': 23764.14, 'prev_contribution': 9859.5, 'ceil_retention': 0.0, 'income_tax': 13904.64}}

        files = ('./output_test/Membros_ativos-12-2019.ods',)
        employees = parser.parse(files, "12", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_membros_inativos_jan_2020(self):
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

    def test_membros_inativos_dez_2019(self):
        self.maxDiff = None

        expected = {'reg': '948780', 'name': 'AGENOR NAKAZONE', 'role': 'PROCURADOR DE JUSTICA', 'type': 'membro', 'workplace': 'PROCURADORIA DE JUSTICA CRIMINAL', 'active': False, 'income': {'total': 57373.46, 'wage': 36742.01, 'perks': {'total': 0.0}, 'other': {'total': 20631.45, 'trust_position': 1506.96,
                                                                                                                                                                                                                                                                        'others_total': 19124.49, 'others': {'Gratificação Natalina': 19124.49, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporárias': 0.0}}}, 'discounts': {'total': 24777.39, 'prev_contribution': 8591.43, 'ceil_retention': 0.0, 'income_tax': 16185.96}}

        files = ('./output_test/Membros_inativos-12-2019.ods',)
        employees = parser.parse(files, "12", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_servidores_inativos_jan_2020(self):
        self.maxDiff = None

        expected = {'reg': '1174', 'name': 'ABIGAIR MONTEIRO', 'role': 'OFICIAL DE PROMOTORIA I', 'type': 'servidor', 'workplace': 'AREA REGIONAL DE SAO JOSE DO RIO PRETO', 'active': False, 'income': {'total': 8458.57, 'wage': 8458.57, 'perks': {'total': 0.0}, 'other': {'total': 0.0, 'trust_position': 0.0,
                                                                                                                                                                                                                                                                               'others_total': 0.0, 'others': {'Gratificação Natalina': 0.0, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporárias': 0.0}}}, 'discounts': {'total': 1372.38, 'prev_contribution': 604.18, 'ceil_retention': 0.0, 'income_tax': 768.2}}

        files = ('./output_test/Servidores_inativos-01-2020.ods', )
        employees = parser.parse(files, "01", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_servidores_inativos_dez_2019(self):
        self.maxDiff = None

        expected = {'reg': '953273', 'name': 'ALCIDES CAETANO', 'role': 'AUXILIAR DE PROMOTORIA I', 'type': 'servidor', 'workplace': 'AREA DE TRANSPORTES', 'active': False, 'income': {'total': 10768.1, 'wage': 6674.54, 'perks': {'total': 356.24}, 'other': {'total': 3737.32, 'trust_position': 0.0,
                                                                                                                                                                                                                                                                 'others_total': 3737.32, 'others': {'Gratificação Natalina': 3737.32, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporárias': 0.0}}}, 'discounts': {'total': 1546.78, 'prev_contribution': 447.16, 'ceil_retention': 0.0, 'income_tax': 1099.62}}

        files = ('./output_test/Servidores_inativos-12-2019.ods', )
        employees = parser.parse(files, "12", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_servidores_ativos_jan_2020(self):
        self.maxDiff = None

        expected = {'reg': '1469', 'name': 'ABEL VIEIRA DE MENEZES FILHO', 'role': ' AUXILIAR DE PROMOTORIA I ', 'type': 'servidor', 'workplace': ' AREA REGIONAL DA CAPITAL ', 'active': True, 'income': {'total': 7874.06, 'wage': 6623.36, 'perks': {'total': 1250.7}, 'other': {'total': 0.0, 'trust_position': 0.0,
                                                                                                                                                                                                                                                                                    'others_total': 0.0, 'others': {'Gratificação Natalina': 0.0, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporárias': 0.0}}}, 'discounts': {'total': 1612.73, 'prev_contribution': 861.02, 'ceil_retention': 0.0, 'income_tax': 751.71}}

        files = ('./output_test/Servidores_ativos-01-2020.ods', )
        employees = parser.parse(files, "01", "2020")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_servidores_ativos_dez_2019(self):
        self.maxDiff = None

        expected = {'reg': '4895', 'name': 'ADRIANA SALTO', 'role': 'OFICIAL DE PROMOTORIA I', 'type': 'servidor', 'workplace': 'SERVICO TECNICO ADMINISTRATIVO DE TIETE', 'active': True, 'income': {'total': 11246.37, 'wage': 6267.32, 'perks': {'total': 1169.44}, 'other': {'total': 3809.61, 'trust_position': 333.44,
                                                                                                                                                                                                                                                                                 'others_total': 3476.17, 'others': {'Gratificação Natalina': 3476.17, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporárias': 0.0}}}, 'discounts': {'total': 3259.08, 'prev_contribution': 1757.98, 'ceil_retention': 0.0, 'income_tax': 1501.1}}

        files = ('./output_test/Servidores_ativos-12-2019.ods', )
        employees = parser.parse(files, "12", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    #  Tests for active members who have different table formats

    def test_active_members_january_2019(self):
        self.maxDiff = None

        expected = {'reg': '3725', 'name': 'ABNER CASTORINO', 'role': 'PROMOTOR DE JUSTICA (ENTRANCIA FINAL)', 'type': 'membro', 'workplace': 'PROMOTORIA DE JUSTICA DE SAO BERNARDO DO CAMPO', 'active': True, 'income': {'total': 34609.1, 'wage': 33689.1, 'perks': {'total': 920.0, 'food': 920.0, 'housing_aid': 0.0}, 'other': {
            'total': 0.0, 'trust_position': 0.0, 'others_total': 0.0, 'others': {'Gratificação Natalina': 0.0, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporárias': 0.0}}}, 'discounts': {'total': 11081.84, 'prev_contribution': 3705.8, 'ceil_retention': 0.0, 'income_tax': 7376.04}}

        files = ('./output_test/Membros_ativos-01-2019.ods', )
        employees = parser.parse(files, "01", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_members_march_2019(self):
        self.maxDiff = None

        expected = {'reg': '3725', 'name': 'ABNER CASTORINO', 'role': 'PROMOTOR DE JUSTICA (ENTRANCIA FINAL)', 'type': 'membro', 'workplace': 'PROMOTORIA DE JUSTICA DE SAO BERNARDO DO CAMPO', 'active': True, 'income': {'total': 34609.1, 'wage': 33689.1, 'perks': {'total': 920.0, 'food': 920.0, 'ferias em pecunia': 0.0}, 'other': {
            'total': 4042.68, 'trust_position': 0.0, 'others_total': 4042.68, 'others': {'Gratificação Natalina': 0.0, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporárias': 4042.68}}}, 'discounts': {'total': 12193.58, 'prev_contribution': 3705.8, 'ceil_retention': 0.0, 'income_tax': 8487.78}}

        files = ('./output_test/Membros_ativos-03-2019.ods', )
        employees = parser.parse(files, "03", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_active_members_june_2019(self):
        self.maxDiff = None

        expected = {'reg': '207', 'name': 'FREDERICO AUGUSTO NEVES ARAUJO', 'role': 'PROMOTOR DE JUSTICA (ENTRANCIA FINAL)', 'type': 'membro', 'workplace': 'PROMOTORIA DE JUSTICA DE TAUBATE', 'active': True, 'income': {'total': 34609.1, 'wage': 33689.1, 'perks': {'total': 920.0, 'food': 920.0, 'ferias em pecunia': 0.0, 'LP em pecunia': 0.0}, 'other': {
            'total': 0.0, 'trust_position': 0.0, 'others_total': 0.0, 'others': {'Gratificação Natalina': 0.0, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Outras remunerações temporarias': 0.0}}}, 'discounts': {'total': 11081.84, 'prev_contribution': 3705.8, 'income_tax': 7376.04}}

        files = ('./output_test/Membros_ativos-06-2019.ods', )
        employees = parser.parse(files, "06", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # #  Tests for inactive members who have different table formats

    def test_inactive_members_january_2019(self):
        self.maxDiff = None

        expected = {'reg': '137707', 'name': 'ABEL PEDRO RIBEIRO', 'role': 'PROMOTOR DE JUSTICA (ENTRANCIA FINAL)', 'type': 'membro', 'workplace': 'PROMOTORIAS DE JUSTICA', 'active': False, 'income': {'total': 45627.43, 'wage': 30418.28, 'other': {
            'total': 15209.15, 'others_total': 15209.15, 'others': {'Gratificação Natalina': 15209.15}}}, 'discounts': {'total': 18959.9, 'prev_contribution': 6514.5, 'ceil_retention': 0.0, 'income_tax': 26667.53}}

        files = ('./output_test/Membros_inativos-01-2019.ods', )
        employees = parser.parse(files, "01", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_inactive_members_may_2019(self):
        self.maxDiff = None

        expected = {'reg': '137707', 'name': 'ABEL PEDRO RIBEIRO', 'role': 'PROMOTOR DE JUSTICA (ENTRANCIA FINAL)', 'type': 'membro', 'workplace': 'PROMOTORIAS DE JUSTICA', 'active': False, 'income': {'total': 35159.83, 'wage': 35159.83, 'perks': {'total': 0.0, 'food': 0.0, 'ferias em pecunia': 0.0}, 'other': {
            'total': 0.0, 'trust_position': 0.0, 'others_total': 0.0, 'others': {'Gratificação Natalina': 0.0, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0}}}, 'discounts': {'total': 10614.29, 'prev_contribution': 3225.24, 'income_tax': 7389.05, 'ceil_retention': 0.0}}

        files = ('./output_test/Membros_inativos-05-2019.ods', )
        employees = parser.parse(files, "05", "2019")
        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_inactive_members_june_2019(self):
        self.maxDiff = None

        expected = {'reg': '137707', 'name': 'ABEL PEDRO RIBEIRO', 'role': 'PROMOTOR DE JUSTICA (ENTRANCIA FINAL)', 'type': 'membro', 'workplace': 'PROMOTORIAS DE JUSTICA', 'active': False, 'income': {'total': 35159.83, 'wage': 35159.83, 'perks': {'total': 0.0, 'food': 0.0, 'ferias em pecunia': 0.0}, 'other': {
            'total': 0.0, 'others_total': 0.0, 'others': {'Gratificação Natalina': 0.0, 'Abono de Permanência': 0.0}}}, 'discounts': {'total': 10614.29, 'prev_contribution': 3225.24, 'income_tax': 7389.05, 'ceil_retention': 0.0}}

        files = ('./output_test/Membros_inativos-06-2019.ods', )
        employees = parser.parse(files, "06", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # #  Tests for Active Serveres who have different table formats

    def test_active_serveres_january_2019(self):
        self.maxDiff = None

        expected = {'reg': '1469', 'name': 'ABEL VIEIRA DE MENEZES FILHO', 'role': 'AREA REGIONAL DA CAPITAL', 'type': 'servidor', 'workplace': 'AUXILIAR DE PROMOTORIA I', 'active': True, 'income': {'total': 7573.02, 'wage': 6371.44, 'perks': {'total': 1201.58, 'food': 920.0, 'transportation': 281.58, 'pre_school': 0.0}, 'other': {
            'total': 0.0, 'trust_position': 0.0, 'others_total': 0.0, 'others': {'Gratificação Natalina': 0.0, 'Férias (1/3 constitucional)': 0.0, 'Abono de Permanência': 0.0, 'Gratificação de Qualificação': 0.0}}}, 'discounts': {'total': 1518.32, 'prev_contribution': 828.27, 'ceil_retention': 0.0, 'income_tax': 690.05}}

        files = ('./output_test/Servidores_ativos-01-2019.ods', )
        employees = parser.parse(files, "01", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    # #  Tests for Active Serveres who have different table formats

    def test_inactive_serveres_january_2019(self):
        self.maxDiff = None

        expected = {'reg': '1174', 'name': 'ABIGAIR MONTEIRO', 'role': 'OFICIAL DE PROMOTORIA I', 'type': 'servidor', 'workplace': 'AREA REGIONAL DE SAO JOSE DO RIO PRETO', 'active': False, 'income': {
            'total': 8180.43, 'wage': 8180.43, 'other': {'total': 0.0, 'others_total': 0.0, 'others': {'Gratificação Natalina': 0.0}}}, 'discounts': {'total': 1266.27, 'prev_contribution': 584.7, 'income_tax': 681.57}}
        files = ('./output_test/Servidores_inativos-01-2019.ods', )
        employees = parser.parse(files, "01", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_inactive_serveres_may_2019(self):
        self.maxDiff = None

        expected = {'reg': '4324', 'name': 'MILTON RANGEL DE QUADROS', 'role': 'OFICIAL DE PROMOTORIA I', 'type': 'servidor', 'workplace': 'SERVICO TECNICO ADMINISTRATIVO DE ARACATUBA', 'active': False, 'income': {'total': 8900.62, 'wage': 5244.0, 'perks': {'total': 3496.0, 'food': 0.0, 'transportation': 0.0,
                                                                                                                                                                                                                                                                  'ferias em pecunia': 3496.0}, 'other': {'total': 160.62, 'trust_position': 80.31, 'others_total': 80.31, 'others': {'Gratificação Natalina': 0.0, 'Abono de Permanência': 0.0, 'Outras Remunerações Temporárias': 80.31}}}, 'discounts': {'total': 701.3, 'prev_contribution': 106.48, 'income_tax': 594.82}}
        files = ('./output_test/Servidores_inativos-05-2019.ods', )
        employees = parser.parse(files, "05", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_inactive_serveres_june_2019(self):
        self.maxDiff = None

        expected = {'reg': '386921', 'name': 'ANTONIA MARIA DE MATOS', 'role': 'AUXILIAR DE PROMOTORIA I', 'type': 'servidor', 'workplace': 'AREA DE ATIVIDADES COMPLEMENTARES', 'active': False, 'income': {'total': 6313.87, 'wage': 5259.27, 'perks': {'total': 726.78, 'food': 562.22, 'transportation': 164.56}, 'other': {
            'total': 327.82, 'trust_position': 0.0, 'others_total': 327.82, 'others': {'Gratificação Natalina': 0.0, 'Abono de Permanência': 327.82, 'Gratificação de Qualificação': 0.0}}}, 'discounts': {'total': 559.27, 'prev_contribution': 459.95, 'income_tax': 99.32}}

        files = ('./output_test/Servidores_inativos-06-2019.ods', )
        employees = parser.parse(files, "06", "2019")

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == '__main__':
    unittest.main()
