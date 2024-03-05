from netbom.bom import Bom, BomRow, BomData, BomRows
import pandas as pd


class AltiumBomReader:
    ROW_DATA = 0
    DATA_HEADERS_SUFIX = ":"
    ROW_HEADERS = 1

    def from_excel(self, path) -> Bom:
        bom = Bom(self._read_excel_bom_data(path))

        cols = self._extract_columns_by_key(self._read_excel_bom_rows(path))
        for i, __ in enumerate(cols[next(iter(cols))]):
            row = BomRow()
            for key in BomRow().keys():
                if len(cols[key]):
                    row._get_key_values({key: cols[key][i]})
            bom.rows.append(row)
        return bom

    def _read_excel_bom_data(self, path) -> BomData:
        df = pd.read_excel(path, header=self.ROW_DATA)
        bom_data = BomData()
        for i, cell in enumerate(df.keys().tolist()):
            for key in bom_data._data:
                if key + self.DATA_HEADERS_SUFIX == cell:
                    bom_data._get_key_values({key: df.keys().tolist()[i + 1]})
        return bom_data

    def _read_excel_bom_rows(self, path) -> BomRows:
        return pd.read_excel(path, header=self.ROW_HEADERS)

    def _extract_columns_by_key(self, data_frame) -> dict:
        cols_dict = {}
        for key in BomRow().keys():
            if key in data_frame:
                cols_dict.update({key: data_frame[key].tolist()})
            else:
                cols_dict.update({key: []})
        return cols_dict
