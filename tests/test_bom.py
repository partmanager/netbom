from netbom.bom import Bom, BomRow, BomData, BomRows
import unittest


class TestBom(unittest.TestCase):
    def test_bom_rows_from_list(self):
        bom = Bom(BomData())
        self.assertEqual(len(bom.rows), 0)
        bom.rows = BomRows([BomRow({"Part Number": "abc"}),
                            BomRow({"Part Number": "def"})])
        self.assertEqual(len(bom.rows), 2)
        self.assertEqual(bom.rows[0]["Part Number"], "abc")
        self.assertEqual(bom.rows[1]["Part Number"], "def")

    def test_bom_append_and_delete_row(self):
        bom = Bom(BomData())
        bom.rows.append(BomRow({"Part Number": "klm"}))
        bom.rows.append(BomRow({"Part Number": "xyz"}))
        self.assertEqual(len(bom.rows), 2)
        self.assertEqual(bom.rows[0]["Part Number"], "klm")
        self.assertEqual(bom.rows[1]["Part Number"], "xyz")
        bom.rows.delete(0)
        self.assertEqual(len(bom.rows), 1)
        self.assertEqual(bom.rows[0]["Part Number"], "xyz")

    def test_bom_add_rows(self):
        bom1 = Bom(BomData())
        bom1.rows.append(BomRow({"Part Number": "abc"}))
        bom1.rows.append(BomRow({"Part Number": "def"}))
        bom2 = Bom(BomData())
        bom2.rows.append(BomRow({"Part Number": "klm"}))
        bom2.rows.append(BomRow({"Part Number": "xyz"}))
        bom3 = Bom(BomData({"Project": "Test Add Rows"}))
        bom3.rows = bom1.rows + bom2.rows
        self.assertEqual(bom3.data["Project"], "Test Add Rows")
        self.assertEqual(len(bom3.rows), 4)
        self.assertEqual(bom3.rows[0]["Part Number"], "abc")
        self.assertEqual(bom3.rows[1]["Part Number"], "def")
        self.assertEqual(bom3.rows[2]["Part Number"], "klm")
        self.assertEqual(bom3.rows[3]["Part Number"], "xyz")

    def test_bom_change_data(self):
        bom = Bom(BomData())
        self.assertEqual(bom.data["Project"], "")
        self.assertEqual(bom.data["GerberVersion"], "")
        bom.data["Project"] = "Test Change Project"
        bom.data["GerberVersion"] = "GA"
        self.assertEqual(bom.data["Project"], "Test Change Project")
        self.assertEqual(bom.data["GerberVersion"], "GA")

    def test_bom_multiple_instances(self):
        bom1 = Bom(BomData())
        bom1.rows.append(BomRow({"Part Number": "abc"}))
        bom1.rows.append(BomRow({"Part Number": "def"}))
        bom2 = Bom(BomData())
        bom2.rows.append(BomRow({"Part Number": "ghi"}))
        bom2.rows.append(BomRow({"Part Number": "jkl"}))
        self.assertEqual(len(bom1.rows), 2)
        self.assertEqual(len(bom2.rows), 2)
        self.assertEqual(bom1.rows[0]["Part Number"], "abc")
        self.assertEqual(bom1.rows[1]["Part Number"], "def")
        self.assertEqual(bom2.rows[0]["Part Number"], "ghi")
        self.assertEqual(bom2.rows[1]["Part Number"], "jkl")
    
    def test_bom_append_row_by_designator(self):
        bom_rows = BomRows()
        bom_rows.append_by_designator("C1", data_dict={"Footprint": "C_0402"})
        bom_rows.append_by_designator("Q122", data_dict={"Footprint": "TO-92"})
        bom_rows.append_by_designator("FB3", data_dict={"Footprint": "R_0603"})
        self.assertEqual(len(bom_rows), 3)

    def test_bom_append_row_by_designator_with_roomletters(self):
        bom_rows = BomRows()
        bom_rows.append_by_designator("C10A", data_dict={"Footprint": "C_0402"})
        bom_rows.append_by_designator("C10B", data_dict={"Footprint": "C_0402"})

        bom_rows.append_by_designator("C11A", data_dict={"Footprint": "C_0603"})
        bom_rows.append_by_designator("C11B", data_dict={"Footprint": "C_0603"})
        bom_rows.append_by_designator("C11C", data_dict={"Footprint": "C_0603"})

        bom_rows.append_by_designator("C12D", data_dict={"Footprint": "C_1206"})

        self.assertEqual(len(bom_rows), 3)
        self.assertEqual(bom_rows[0]["Designator"], "C10")
        self.assertEqual(bom_rows[0]["Footprint"], "C_0402")
        self.assertEqual(bom_rows[1]["Designator"], "C11")
        self.assertEqual(bom_rows[1]["Footprint"], "C_0603")
        self.assertEqual(bom_rows[2]["Designator"], "C12")
        self.assertEqual(bom_rows[2]["Footprint"], "C_1206")

    def test__strip_designator_roomletters(self):
        bom_rows = BomRows()
        self.assertEqual(bom_rows._strip_designator_roomletter("C11A"), "C11")
        self.assertEqual(bom_rows._strip_designator_roomletter("C3BB"), "C3")
        self.assertEqual(bom_rows._strip_designator_roomletter("FB12345BB"), "FB12345")

    def test_fetch_row_by_designator(self):
        bom_rows = BomRows()
        bom_rows.append_by_designator("C129", data_dict={"Footprint": "C_1206"})
        row = bom_rows.fetch_row_by_designator("C129")
        self.assertEqual(row["Footprint"], "C_1206")
        self.assertEqual(row["Designator"], "C129")

        self.assertEqual(bom_rows.fetch_row_by_designator("FB4"), None)

if __name__ == '__main__':
    unittest.main()
