netlist
=======
.. automodule:: netbom.netlist

Usage
-----

Recreating netlist manually based on Altium Designer's schematic shown above, then performing some simple operations:

.. doctest::

   >>> from netbom.netlist import Netlist

   >>> # Creating Netlist object
   >>> netlist = Netlist()

   >>> # Recreating Altium Designer's schematic shown above by appending pins one-by-one
   >>> netlist.append_pin('NetD1_1', 'D1', '1')
   >>> netlist.append_pin('NetD1_1', 'R1', '2')
   >>> netlist.append_pin('GND', 'J1', '2')
   >>> netlist.append_pin('GND', 'R1', '1')
   >>> netlist.append_pin('+3.3V', 'D1', '2')
   >>> netlist.append_pin('+3.3V', 'J1', '1')
   >>> print(netlist)
   {'NetD1_1': {'D1': ['1'], 'R1': ['2']}, 'GND': {'J1': ['2'], 'R1': ['1']}, '+3.3V': {'D1': ['2'], 'J1': ['1']}}

   >>> # Netlist length
   >>> print(len(netlist))
   3

   >>> # Filtering designators starting with 'R' string
   >>> print(netlist.filter_designator(startswith='R'))
   {'R1': {'1': 'GND', '2': 'NetD1_1'}}

   >>> # List of nets in Netlist object
   >>> print(netlist.nets())
   ['NetD1_1', 'GND', '+3.3V']

   >>> # Iterating over Netlist structure
   >>> for netline in netlist:
   ...   for connection in netline.connections:
   ...     for pin in connection.pins:
   ...       print([netline.net, connection.designator, pin])
   ['NetD1_1', 'D1', '1']
   ['NetD1_1', 'R1', '2']
   ['GND', 'J1', '2']
   ['GND', 'R1', '1']
   ['+3.3V', 'D1', '2']
   ['+3.3V', 'J1', '1']

   >>> # Converting Netlist object to dict
   >>> print(netlist.to_dict())
   {'NetD1_1': {'D1': ['1'], 'R1': ['2']}, 'GND': {'J1': ['2'], 'R1': ['1']}, '+3.3V': {'D1': ['2'], 'J1': ['1']}}

   >>> # Converting Netlist object to a serialized json
   >>> print(netlist.to_json())
   [{"net": "NetD1_1", "connections": [{"designator": "D1", "pins": ["1"]}, {"designator": "R1", "pins": ["2"]}]}, {"net": "GND", "connections": [{"designator": "J1", "pins": ["2"]}, {"designator": "R1", "pins": ["1"]}]}, {"net": "+3.3V", "connections": [{"designator": "D1", "pins": ["2"]}, {"designator": "J1", "pins": ["1"]}]}]

   >>> # Adding orphaned net which has only one component and only one pin connected
   >>> netlist.append_pin('NetR2_1', 'R2', '1')
   >>> print(netlist)
   {'NetD1_1': {'D1': ['1'], 'R1': ['2']}, 'GND': {'J1': ['2'], 'R1': ['1']}, '+3.3V': {'D1': ['2'], 'J1': ['1']}, 'NetR2_1': {'R2': ['1']}}
   >>> # Removing orphaned net
   >>> netlist.remove_orphans()
   >>> print(netlist)
   {'NetD1_1': {'D1': ['1'], 'R1': ['2']}, 'GND': {'J1': ['2'], 'R1': ['1']}, '+3.3V': {'D1': ['2'], 'J1': ['1']}}
   >>> # Two pins of the same component connected to the same net do not orphan the net
   >>> netlist.append_pin('NetR2_1', 'R2', '1')
   >>> netlist.append_pin('NetR2_1', 'R2', '2')
   >>> netlist.remove_orphans()
   >>> print(netlist)
   {'NetD1_1': {'D1': ['1'], 'R1': ['2']}, 'GND': {'J1': ['2'], 'R1': ['1']}, '+3.3V': {'D1': ['2'], 'J1': ['1']}, 'NetR2_1': {'R2': ['1', '2']}}

Reference
---------

.. autoclass:: netbom.netlist::Netlist
   :members:
