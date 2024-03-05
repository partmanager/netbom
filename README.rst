NetBOM Python library
=====================

.. start-intro

**NetBOM** - Netlist and Bill of Materials (BOM) tooling compatible with Altium Designer
and KiCad.

This library provides tooling to import, process and convert BOM and schematic netlists to
Python objects, and then convet them to JSON format or Python dictionaries. BOM and netlists
are supported by one library because some of netlist formats may also be a source of BOM.

Imported schematic netlist may be used to automate generation of documentation, where you need
to generate a table of pins and signals of a given connector. Interface control documents or
user manuals are often time-consuming to prepare and are examples of such documents. Correctly
drawn electrical schematics can become the only source of truth and can allow to completely
automate document generation. The proposed module can be used to generate connector pin maps,
and generate aesthetic documents in LaTeX.

Imported BOM file may be used as a part of custom Manufacturing Resource Planner, where you 
need to process electronic components required during the PCB assembly process.

.. end-intro
