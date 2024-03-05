"""RINF Netlist Reader module offering RINF Netlist importer that imports
comprehensive BOM and schematic netlist from frp file.
RINF Netlist file may exported by Altium Designer or KiCad. These platforms 
export sligtly different flavours of RINF Netlist but it is well handled by 
this module.
RINF Netlist file is a native netlist file format developed by Zuken.
"""
from netbom.bom import Bom
from netbom.netlist import Netlist


class RinfNetlistReader:
    """RINF Netlist Reader class is a RINF Netlist importer that imports
    comprehensive BOM and schematic netlist from frp file.
    """

    FILE_HEADER = '.HEA'
    FILE_END = '.END'
    SEPARATOR = ' '
    STRING_DELIMITER = '"'

    def bom_from_file(self, path: str) -> Bom:
        """RINF Netlist importer from a file with frp extension.
        It imports comprehensive BOM only.
        
        :param path: RINF Netlist file path with frp extension.
        :type path: str
        :return: imported BOM.
        :rtype: Bom
        """
        bom, _ = self.bom_and_netlist_from_file(path)
        return bom

    def netlist_from_file(self, path: str):
        """RINF Netlist importer from a file with frp extension.
        It imports netlist only.

        :param path: RINF Netlist file path with frp extension.
        :type path: str
        :return: imported Netlist.
        :rtype: Netlist
        """
        _, netlist = self.bom_and_netlist_from_file(path)
        return netlist

    def bom_and_netlist_from_file(self, path: str) -> Bom:
        """RINF Netlist importer from a file with frp extension.
        It imports both comprehensive BOM and netlist.

        :param path: RINF Netlist file path with frp extension.
        :type path: str
        :return: imported tuple of Bom and Netlist.
        :rtype: tuple(Bom, Netlist)
        """

        data_dict = {}
        designator = ''
        net = ''
        bom = Bom()
        netlist = Netlist()
        if self.is_file_valid(path):
            flavor = self.get_file_flavor(path)
            for line in self._read_file_lines(path):
                command, params = self._parse_line(line)

                if command == '.ADD_COM':
                    if designator != params[0]:
                        if designator:
                            bom.rows.append_by_designator(designator, data_dict)
                        designator = params[0]
                        data_dict = {}
                    if 'Eeschema' in flavor and len(params) == 3:
                        symbol = ''
                        footprint = ''
                        if len(params[2].split(':')) == 2:
                            symbol = params[2].split(':')[0]
                            footprint = params[2].split(':')[1]
                        data_dict = {'Value': params[1],
                                     'Symbol': symbol,
                                     'Footprint': footprint}
                elif command == '.ATT_COM' and designator == params[0]:
                    if 'Protel 2004' in flavor:
                        data_dict.update({params[1]: params[2]})

                if command == '.ADD_TER':
                    net = params[2]
                    netlist.append_pin(net, params[0], params[1])
                    if designator:
                        bom.rows.append_by_designator(designator, data_dict)
                elif command == '.TER' or (net and len(params) == 2):
                    netlist.append_pin(net, params[0], params[1])

                if command == '.END':
                    break
        return bom, netlist

    def is_file_valid(self, path: str) -> bool:
        """It verifies frp file validity.

        :param path: A path to frp file to be verified.
        :type path: str
        :return: True if given frp file is correct or False if it is not.
        :rtype: bool
        """
        lines = self._read_file_lines(path)
        return bool(lines and lines[0] == self.FILE_HEADER and lines[-1] == self.FILE_END)

    def get_file_flavor(self, path) -> str:
        """Mathod returning file flavor by reading .APP parameter.

        :param path: Path to frp file to be checked
        :type path: str
        :return: .APP parameter value
        :rtype: str
        """
        lines = self._read_file_lines(path)
        for line in lines:
            command, params = self._parse_line(line)
            if command == '.APP':
                return str(params[0])

    def _read_file_lines(self, path: str) -> list:
        """It reads frp file and returns its lines.

        :param path: Path to frp file to be imported.
        :type path: str
        :return: Lines imported from frp file.
        :rtype: list
        """
        with open(path, 'r', encoding='utf-8') as file:
            return [line.rstrip() for line in file]

    def _parse_line(self, line: str) -> tuple:
        """RINF Netlist line parser. It gives one RINF Netlist line and process
        it returning command and parameters. It is used internally by RINF Netlist Reader.

        :param line: single line (with no newline) from RINF Netlist file
        :type line: str
        :return: a tuple of command (str) and params (list)
        :rtype: tuple(command, params)
        """
        params = []
        output = []
        output_line = []
        is_within_parameter = False

        for char in line:
            if char == self.STRING_DELIMITER:
                is_within_parameter = not is_within_parameter
            else:
                if is_within_parameter or char is not self.SEPARATOR:
                    output_line.append(char)
            if not is_within_parameter and char == self.SEPARATOR and output_line:
                output.append("".join(output_line))
                output_line = []

        output.append("".join(output_line))
        command = None
        if output[0].startswith('.'):
            command = output.pop(0)
        params = output
        return command, params
