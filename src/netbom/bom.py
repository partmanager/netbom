class BomUtils:
    def _get_key_values(self, data_dict):
        for value in data_dict:
            for key in self._data:
                if key == value:
                    if type(self._data[key]) == type(data_dict[value]):
                        self._data[key] = data_dict[value]

    def _to_str_with_separator(self, separator):
        outstr = ""
        for i, key in enumerate(self._data):
            outstr += str(key) + ": " + str(self._data[key])
            if i != len(self._data) - 1:
                outstr += separator
        return outstr

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data


class BomRow(BomUtils):
    def __init__(self, data_dict={}, index=None, is_type_bom=True):
        self._data = {"Part Number": "",
                      "Value": "",
                      "Footprint": "",
                      "Quantity": int(0),
                      "Description": "",
                      "Voltage": "",
                      "Dielectric": "",
                      "Manufacturer Part Number": "",
                      "Comment": "",
                      "Designator": "",
                      "HelpURL": "",
                      "Index": index,
                      "isTypeBom": is_type_bom,
                      "Symbol": ""}
        self._get_key_values(data_dict)

    def set_index(self, index):
        self._data["Index"] = int(index)

    def __str__(self):
        return self._to_str_with_separator(", ")


class BomRows:
    def __init__(self, rows=None):
        if rows is None:
            rows = []
        self._current_index = 0
        self._rows = rows

    def append(self, row):
        if isinstance(row, BomRow):
            row.set_index(self.__len__())
            self._rows.append(row)
        else:
            raise ValueError

    def append_by_designator(self, designator: str, data_dict: dict) -> None:
        des = self._strip_designator_roomletter(designator)
        data_dict.update({"Designator": des, "Quantity": 1})
        if self._row_index_by_designator(des) is None:
            self._rows.append(BomRow(data_dict))

    def fetch_row_by_designator(self, designator: str) -> BomRow:
        index = self._row_index_by_designator(designator)
        if index is not None:
            return self._rows[index]

    def _row_index_by_designator(self, designator: str) -> int:
        for index, row in enumerate(self._rows):
            if row["Designator"] == designator:
                return index

    def _strip_designator_roomletter(self, designator: str) -> None:
        output = []
        was_char_numeric = False
        for char in designator:
            if was_char_numeric and not char.isnumeric():
                break
            output.append(char)
            was_char_numeric = char.isnumeric()
        return "".join(output)

    def delete(self, index):
        if isinstance(index, int):
            del self._rows[index]
        else:
            raise ValueError

    def items(self):
        return self._rows

    def __add__(self, other):
        if isinstance(other, BomRows):
            self._rows += other._rows
            return self
        else:
            raise ValueError

    def __getitem__(self, index):
        return self._rows[index]

    def __len__(self):
        return len(self._rows)

    def __next__(self):
        if self._current_index < len(self._rows):
            x = self._rows[self._current_index]
            self._current_index += 1
            return x
        raise StopIteration


class BomData(BomUtils):
    def __init__(self, data_dict={}):
        self._data = {"Project": "",
                      "Equipment": "",
                      "BatchNumber": "",
                      "Variant": "",
                      "GitHash": "",
                      "GerberVersion": ""}
        self._get_key_values(data_dict)

    def __str__(self):
        return self._to_str_with_separator(" | ")


class Bom:
    def __init__(self, data=None, rows=None):
        self._rows = BomRows()
        self._data = BomData()

        if isinstance(data, BomData):
            self._data = data
        if isinstance(rows, BomRows):
            self._rows = rows

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if isinstance(data, BomData):
            self._data = data
        else:
            raise ValueError

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, rows):
        if isinstance(rows, BomRows):
            self._rows = rows
        else:
            raise ValueError

    def __str__(self):
        return str(self.data) + " | Rows: " + str(len(self._rows))
