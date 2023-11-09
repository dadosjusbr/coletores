import parser
import unittest
import json


class TestParser(unittest.TestCase):
    def test_jan_2018(self):
        self.maxDiff = None

        expected = {}

        files = (
            "./src/output_test/MPSC-1_2018-Membros Ativos.ods",
            "./src/output_test/MPSC-1_2018-Verbas Indenizatórias.ods",
        )

        parser.parse("MPSC", "2018", files, "/src/output_test", "teste")
        with open("./src/output_test/MPSC-1-2018.json") as json_file:
            data = json.load(json_file)
        employees = data["cr"]["employees"]

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

    def test_jan_2019(self):
        self.maxDiff = None

        expected = {}

        files = (
            "./src/output_test/MPSC-1_2019-Membros Ativos.ods",
            "./src/output_test/MPSC-1_2019-Verbas Indenizatórias.ods",
        )

        parser.parse("MPSC", "2019", files, "/src/output_test", "teste")
        with open("./src/output_test/MPSC-1-2019.json") as json_file:
            data = json.load(json_file)
        employees = data["cr"]["employees"]

        # Verificações
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)


if __name__ == "__main__":
    unittest.main()
