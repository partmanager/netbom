from netbom.netlist_readers import RinfNetlistReader
import time
import unittest
import os

DIR =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples", "netlist/")


class TestRINFNetlistReaderLineParser(unittest.TestCase):
    def _template_test_line_parser(self, input: str, command: str, params: list) -> None:
        parsed_command, parsed_params = RinfNetlistReader()._parse_line(input)
        self.assertEqual(parsed_command, command)
        self.assertEqual(parsed_params, params)

    def test_multiple_spaces_within_parameter_and_separator(self):
        self._template_test_line_parser(input='.ADD_COM  "Resistor   Network" "Resistor   Network"',
                                        command='.ADD_COM',
                                        params=['Resistor   Network',
                                                'Resistor   Network'])

    def test_split_altium_line_add_com(self):
        self._template_test_line_parser(input='.ADD_COM RN22C "RN4" "RN4"',
                                        command='.ADD_COM',
                                        params=['RN22C',
                                                'RN4',
                                                'RN4'])

    def test_split_altium_line_att_com(self):
        self._template_test_line_parser(input='.ATT_COM RN22C "Comment" "Resistors Network"',
                                        command='.ATT_COM',
                                        params=['RN22C',
                                                'Comment',
                                                'Resistors Network'])

    def test_split_altium_line_add_ter(self):
        self._template_test_line_parser(input='.ADD_TER U10 D4 "NetU10_D4"',
                                        command='.ADD_TER',
                                        params=['U10',
                                                'D4',
                                                'NetU10_D4'])

    def test_split_altium_line_ter(self):
        self._template_test_line_parser(input='.TER U11 D4',
                                        command='.TER',
                                        params=['U11',
                                                'D4'])

    def test_split_kicad_line_add_com(self):
        self._template_test_line_parser(input='.ADD_COM     C11     "100nF/50V/5%/X7R/C0603"     "C_0603"',
                                        command='.ADD_COM',
                                        params=['C11',
                                                '100nF/50V/5%/X7R/C0603',
                                                'C_0603'])

    def test_split_kicad_line_add_ter(self):
        self._template_test_line_parser(input='.ADD_TER   C11   2     "Net-(C11-Pad2)"',
                                        command='.ADD_TER',
                                        params=['C11',
                                                '2',
                                                'Net-(C11-Pad2)'])

    def test_split_kicad_line_ter(self):
        self._template_test_line_parser(input='.TER       C28   2',
                                        command='.TER',
                                        params=['C28',
                                                '2'])


class TestRINFNetlistReader(unittest.TestCase):
    def _template_test_import_example(self, file):
        start = time.time()
        bom, netlist = RinfNetlistReader().bom_and_netlist_from_file(DIR + file)
        stop = int((time.time() - start) * 1000)
        flavor = RinfNetlistReader().get_file_flavor(DIR + file)
        print(__class__.__name__ + ":", file, 'imported in', stop, 'ms, detected file flavor:', flavor)
        return bom, netlist

    def test_netlist_altium_lt3580_module(self):
        bom, netlist = self._template_test_import_example('Altium_LT3580-Module.FRP')

        self.assertEqual(len(bom.rows), 44)
        self.assertEqual(len(netlist), 22)

        filtered_designators = netlist.filter_designator('U1')
        self.assertEqual(len(filtered_designators), 1)
        self.assertEqual(len(filtered_designators['U1']), 9)

        filtered_designators = netlist.filter_designator('R')
        self.assertEqual(len(filtered_designators), 12)


if __name__ == '__main__':
    unittest.main()
