NetBOM Python library
=====================

.. start-intro

**NetBOM** - Library to read, convert and process electrical netlists and Bill of Materials (BOM)
generated both in Alitum Designer and KiCad.

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

Installing
----------

As usual, you can use package installer for Python:

   pip install netbom

Repository
----------

Code is maintained on GitHub: `github.com/partmanager/netbom <https://github.com/partmanager/netbom>`_.

.. end-intro

Documentation
-------------

Get the latest documentation build: `partmanager.github.io/netbom <https://partmanager.github.io/netbom>`_.

How does it work
----------------

Let's assume you have to write a document describing electrical interfaces, based on
schematics drawn in Altium Designer. Exemplary schematic diagram is shown below:

.. image:: https://raw.githubusercontent.com/partmanager/netbom/poc/docs/figures/Altium_LED-Resistor.svg
   :align: center

Normally you will open a Word document and start puting the signal names into the table.
Then you will describe each of the signals. Doing it the first time is not a problem yet,
but maintaining it later is time-consuming.
Usign the Netbom library, and some markup language like LaTex or Markdown, you may
generate pinout logical diagrams, physical diagrams and tables automatically using schematic
netlist (i.e. RINF Netlist) exported directly from Altium Designer. The previously shown 
schematic diagram was loaded into the Netlist object shown below:

.. image:: https://raw.githubusercontent.com/partmanager/netbom/poc/docs/figures/Altium_LED-Resistor_netlist.svg
   :align: center

Then it can be processed and the extracted content can be automatically placed in a table
or on an SVG template.
