from netbom.netlist import Netlist, NetlistConnections, NetlistPins, NetlistConnection
import unittest


class TestConnections(unittest.TestCase):
    def test_connections(self):
        connections = NetlistConnections(NetlistConnection('D1', NetlistPins(['1', '2'])))
        self.assertEqual(connections.to_dict(), {'D1': ['1', '2']})

        connections.append(NetlistConnection('D2', NetlistPins(['3', '4'])))
        self.assertEqual(connections.to_dict(), {'D1': ['1', '2'],
                                                 'D2': ['3', '4']})

        connections.append(NetlistConnection('D3', NetlistPins(['5', '6'])))
        self.assertEqual(connections.to_dict(), {'D1': ['1', '2'],
                                                 'D2': ['3', '4'],
                                                 'D3': ['5', '6']})

        connections.append(NetlistConnection('D3', NetlistPins(['7'])))
        self.assertEqual(connections.to_dict(), {'D1': ['1', '2'],
                                                 'D2': ['3', '4'],
                                                 'D3': ['5', '6', '7']})

        connections.append(NetlistConnection('D3', NetlistPins(['8'])))
        self.assertEqual(connections.to_dict(), {'D1': ['1', '2'],
                                                 'D2': ['3', '4'],
                                                 'D3': ['5', '6', '7', '8']})

        connections.append(NetlistConnection('D3', NetlistPins(['8'])))
        self.assertEqual(connections.to_dict(), {'D1': ['1', '2'],
                                                 'D2': ['3', '4'],
                                                 'D3': ['5', '6', '7', '8']})
        self.assertEqual(len(connections), 3)


class TestNetlist(unittest.TestCase):
    def _template_netlist(self):
        netlist = Netlist()
        netlist.append_pins('NetR1_1', 'R1', ['1', '2'])
        self.assertEqual(len(netlist), 1)
        return netlist

    def test_netlist_duplicated_net_designator_and_pins(self):
        netlist = self._template_netlist()
        netlist.append_pins('NetR1_1', 'R1', ['1', '2'])
        self.assertEqual(netlist.to_dict(), {'NetR1_1': {'R1': ['1', '2']}})

    def test_netlist_duplicated_designator_and_pins(self):
        netlist = self._template_netlist()
        netlist.append_pins('NetR2_2', 'R1', ['1', '2'])
        # [TODO] method: detecting designators and pins connected to the same net
        self.assertEqual(netlist.to_dict(), {'NetR1_1': {'R1': ['1', '2']},
                                             'NetR2_2': {'R1': ['1', '2']}})
        self.assertEqual(len(netlist), 2)

    def test_netlist_duplicated_net_and_designator(self):
        netlist = self._template_netlist()
        netlist.append_pins('NetR1_1', 'R1', ['3', '4'])
        self.assertEqual(netlist.to_dict(), {'NetR1_1': {'R1': ['1', '2', '3', '4']}})

    def test_netlist_numeric_pins_sorting(self):
        netlist = self._template_netlist()
        netlist.append_pins('NetR1_1', 'R1', ['4', '7'])
        self.assertEqual(netlist.to_dict(), {'NetR1_1': {'R1': ['1', '2', '4', '7']}})

    def test_netlist_alphanumeric_pins_sorting(self):
        netlist = self._template_netlist()
        netlist.append_pins('NetR1_1', 'R1', ['A44', 'A4'])
        self.assertEqual(netlist.to_dict(), {'NetR1_1': {'R1': ['1', '2', 'A4', 'A44']}})

    def test_large_netlist_and_append_pin(self):
        netlist = Netlist()
        for i in range(0, 1000):
            net = 'NetR' + str(i) + '_1'
            designator = 'R' + str(i)
            for pin in range(1, 5):
                netlist.append_pin(net, designator, str(pin))
        self.assertEqual(len(netlist), 1000)


if __name__ == '__main__':
    unittest.main()
