"""
Netlist module encapsulating electrical netlist into following structure:

.. image:: ./figures/Altium_LED-Resistor_netlist.svg

Netlist module simplifies electrical netlist processing in larger systems by providing
basic operations: simple netlist iterators, to dict and json converters. It also simplifies 
operations used in netlist file readers by providing append methods and add operators. 

Netlist object shown above was exported by Altium Designer to a RINF Netlist 
using following schematic diagram:

.. image:: ./figures/Altium_LED-Resistor.svg
   :align: center
"""

import json


class NetlistPins:
    """NetlistPins class used to store pins. It also provides basic converters and operators.
    """

    def __init__(self, pins: list = None) -> None:
        self._items = []
        if pins is not None:
            self._items = pins

    def to_list(self) -> list:
        """Method converting NetlistPins do a list.

        :return: pin list
        :rtype: list
        """
        return self._items

    def __add__(self, other):
        for pin in other:
            if pin not in self:
                self._items += [str(pin)]
        if len(self) > 1:
            self._items.sort()
        return self

    def __iter__(self):
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index) -> str:
        return self._items[index]

    def __str__(self) -> str:
        return '[' + ','.join(self._items) + ']'


class NetlistConnection:
    """NetlistConnection class used to store electrical connection between component
    designator and its pins connected to the same net.
    """

    def __init__(self, designator: str='', pins=NetlistPins()) -> None:
        """NetlistConnection object constructor with
        initializing designator and pins.

        :param designator: designator assigned to pins, defaults to ''
        :type designator: str, optional
        :param pins: NetlistPins object, defaults to NetlistPins()
        :type pins: NetlistPins, optional
        """
        self._designator = designator
        self._pins = pins

    @property
    def designator(self):
        """designator property

        :return: designator assined to pins
        :rtype: str
        """
        return self._designator

    @property
    def pins(self):
        """pins property

        :return: pins
        :rtype: NetlistPins
        """
        return self._pins


class NetlistConnections:
    """NetlistConnections class storing netlist connections composed
    of one or multiple NetlistConnection objects.
    """

    def __init__(self, connection=NetlistConnection()) -> None:
        self._items = {}
        if connection.designator and connection.pins:
            self.append(NetlistConnection(connection.designator, connection.pins))

    def append(self, connection=NetlistConnection()) -> None:
        """Method appending one NetlistConnection.

        :param connection: NetlistConnection object, defaults to NetlistConnection()
        :type connection: NetlistConnection, optional
        """
        pins = connection.pins
        if connection.designator in self.designators():
            pins += self[connection.designator].pins
        self._items.update({connection.designator: NetlistConnection(connection.designator, pins)})

    def designators(self):
        return self._items.keys()

    def to_dict(self) -> dict:
        return {i.designator: i.pins.to_list() for i in self}

    def __add__(self, other):
        for connection in other:
            self.append(connection)
        return self

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int) -> NetlistPins:
        return self._items[index]

    def __iter__(self):
        return iter(self._items.values())

    def __str__(self) -> str:
        return str(self.to_dict())


class NetlistNetline:
    def __init__(self, net='', connections=NetlistConnections()) -> None:
        self._net = net
        self._connections = connections

    @property
    def net(self):
        return self._net

    @property
    def connections(self):
        return self._connections

    def __str__(self) -> str:
        return str(self._net) + ': ' + str(self._connections)


class NetlistDesignator:
    def __init__(self, designator: str, pin_net: dict) -> None:
        self._designator = designator
        self._items = pin_net

    def append(self, pin_net: dict) -> None:
        """Method appending new {pin: net} pairs, deduplicating
        and sorting them.

        :param pin_net: {pin: net} dictionary
        :type pin_net: dict
        """
        self._items.update(pin_net)
        self._items = dict(sorted(self._items.items()))

    def to_dict(self) -> dict:
        """Method converting NetlistDesignator to dict.

        :return: NetlistDesignator converted to dict.
        :rtype: dict
        """
        return {self._designator: self._items}

    @property
    def designator(self):
        return self._designator

    @property
    def items(self):
        return self._items

    def __len__(self) -> int:
        return len(self._items)

    def __str__(self) -> str:
        return str(self.to_dict())


class NetlistDesignators:
    """NetlistDesignators storing component designators and their pins assigned to nets.
    """

    def __init__(self) -> None:
        self._items = {}

    def append(self, designator='', pin='', net='') -> None:
        """Method appending one NetlistDesignator with given parameters.

        :param designator: component designator (i.e. 'R1'), defaults to ''
        :type designator: str, optional
        :param pin: pin designator (i.e. '1'), defaults to ''
        :type pin: str, optional
        :param net: net (i.e. 'NetR1_1'), defaults to ''
        :type net: str, optional
        """
        current_designator = NetlistDesignator(designator, {pin: net})
        if designator in self._items:
            current_designator.append(self[designator].items)
        self._items.update({designator: current_designator})

    def to_dict(self) -> dict:
        """Method converting NetlistDesignators to dict.

        :return: NetlistDesignators converted to dict
        :rtype: dict
        """
        return {designator.designator: designator.items for designator in self}

    def to_json(self) -> str:
        """Method converting NetlistDesignators to valid RFC 8259 serialized JSON string.

        :return: NetlistDesignators converted to JSON
        :rtype: str
        """
        designators = []
        for designator in self:
            pin_net = []
            print(designator)
            for pin, net in designator.to_dict().values():
                pin_net.append({'pin': pin,
                                'net': net})
            designators.append({'designator': designator.designator,
                                'pin_nets': pin_net})
        return str(json.dumps(designators))

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int):
        return self._items[index]

    def __iter__(self):
        return iter(self._items.values())

    def __str__(self) -> str:
        return str(self.to_dict())


class Netlist:
    """NetlistNetlist class providing electrical netlist operations: appending Netline
    with automatic deduplication of nets, designators and pins.
    """

    def __init__(self, netline=NetlistNetline()) -> None:
        """__init__ method of Netlist class with opional initial Netline.

        :param netline: initial Netline, defaults to Netline()
        :type netline: Netline, optional
        """
        self._items = {}
        if netline.net and netline.connections:
            self.append(netline)

    def append(self, netline=NetlistNetline()):
        """Method appending one Netline. Appended net, designator and pins
        are concated and deduplicated with existing ones.

        :param netline: Netline to be appended, defaults to Netline()
        :type netline: Netline, optional
        """
        connections = NetlistConnections()
        if netline.net in self.nets():
            connections += self[netline.net].connections
        self._items.update({netline.net: NetlistNetline(netline.net,
                                                        connections + netline.connections)})

    def append_pin(self, net: str, designator: str, pin: str):
        """Method appending one pin to the Netlist. Appended net, designator and pins
        are deduplicated with existing ones. If there is no net, designator
        or pin: they are created sequentially.

        :param net: net name (i.e. 'NetR1_1')
        :type net: str
        :param designator: component designator (i.e. 'R1')
        :type designator: str
        :param pin: component pin (i.e. '1')
        :type pin: str
        """
        self.append(NetlistNetline(net,
                                   NetlistConnections(NetlistConnection(designator,
                                                                        NetlistPins([pin])))))

    def append_pins(self, net: str, designator: str, pins: list):
        """Method appending a list of pins to the Netlist. Appended net, designator and pins
        are deduplicated with existing ones. If there is no net, designator
        or pins: they are created sequentially.

        :param net: net name (i.e. 'NetR1_1')
        :type net: str
        :param designator: component designator (i.e. 'R1')
        :type designator: str
        :param pins: component pin list (i.e. ['1', '2'])
        :type pins: list of strings
        """
        for pin in pins:
            self.append_pin(net, designator, pin)

    def to_dict(self) -> dict:
        """Method converting Netlist to dict.

        :return: Converted Netlist to dict.
        :rtype: dict
        """
        return {i.net: i.connections.to_dict() for i in self}

    def to_json(self) -> str:
        """Method converting Netlist to valid RFC 8259 serialized JSON string.

        :return: serialized JSON string
        :rtype: str
        """
        netlist = []
        for netline in self:
            connections = []
            for connection in netline.connections:
                connections.append({'designator': connection.designator,
                                    'pins': connection.pins.to_list()})
            netlist.append({'net': netline.net,
                            'connections': connections})
        return str(json.dumps(netlist))

    def nets(self) -> list:
        """Method returning a list of net names.

        :return: List of net names
        :rtype: list
        """
        return list(self._items.keys())

    def filter_designator(self, startswith: str) -> NetlistDesignators:
        """Method which filters designators in Netlist with startswith
        pattern, returning NetlistDesignators object with filtered
        designators.

        :param startswith: Startswith pattern in designators
        :type startswith: str
        :return: NetlistDesignators object
        :rtype: NetlistDesignators
        """
        designators = NetlistDesignators()
        for netline in self:
            for connection in netline.connections:
                if connection.designator.startswith(startswith):
                    for pin in connection.pins:
                        designators.append(connection.designator, pin, netline.net)
        return designators

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int) -> NetlistConnections:
        return self._items[index]

    def __iter__(self):
        return iter(self._items.values())

    def __str__(self) -> str:
        return str(self.to_dict())
