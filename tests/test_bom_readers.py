from netbom.bom_readers import AltiumBomReader
import time
import unittest
import os


DIR =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples/bom/")


class TestAltiumBomReader(unittest.TestCase):
    def _template(self, file, quantity, first_pn, last_pn):
        start = time.time()
        bom = AltiumBomReader().from_excel(path=DIR + file)
        stop = int((time.time() - start) * 1000)
        print(__class__.__name__ + ":", file, 'imported in', stop, 'ms')
        self.assertEqual(len(bom.rows), quantity)
        self.assertEqual(bom.rows[0]["Part Number"], first_pn)
        self.assertEqual(bom.rows[quantity - 1]["Part Number"], last_pn)

    def test_bom_antelope(self):
        self._template(file="Altium_LED-Resistor.xlsx",
                       quantity=3,
                       first_pn="OL_G_0603_150060VS55040",
                       last_pn="R_1k_0402_1")


if __name__ == '__main__':
    unittest.main()
