"""
Module for netlist readers allowing to import well known schematic netlist files prepared
in Altium Designer or KiCad.
There are many netlist file formats which mainly contain simplified or comprehensive 
BOM and schematic netlist. This module import these files and returns unified Bom
and/or Netlist objects.
"""
from .rinf_netlist_reader import RinfNetlistReader
