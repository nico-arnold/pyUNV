from pyuff import pyuff


class UNVParser:
    set_types = None
    file = None

    def __init__(self, filename: str):
        self.filename = filename
        self.file = pyuff.UFF(filename)
        self.refresh(False)

    def refresh(self, reload: bool = True):
        if reload:
            self.file.refresh()
        self.set_types = list(self.file.get_set_types())
        self.dset = self.get_all_sets()
        for set in self.dset:
            if set["type"] == 2411:
                self.points = list(zip(set["x"], set["y"], set["z"]))
            if set["type"] == 2412:
                self.elements = set["all"]
                self.rods = set[11]
                self.triangles = set[
                    41
                ]  # + set[51] + set[61] + set[71] + set[] +
                # self.quads = set[44]# + set[54] + set[64] + set[74] + set[] +
                self.tetraeders = set[111]
            if set["type"] == 2420:
                self.name = set["Part_Name"]
            if set["type"] == 2467:
                self.groups = set

        print("Updated.")

    def get_set_types(self):
        return self.set_types

    def has_set(self, type: int) -> bool:
        if type in self.set_types:
            return True
        else:
            return False

    def get_set(self, set: int):
        print(f"Fetching dataset {set} with datatype {type(set)}")
        if self.has_set(set):
            return self.file.read_sets(self._set_index(set))
        else:
            return IndexError(f"Dataset type not found: {set}")

    def get_all_sets(self, sets=None):
        return self.file.read_sets(sets)

    def write_to_file(self, file: str):
        self._upate_dataset()
        outParser = pyuff.UFF(file)
        outParser.write_sets(self.dset, "overwrite")

    def _set_index(self, set: int):
        return self.set_types.index(set)

    def _upate_dataset(self):
        self._update_points()
        self._update_elements()
        print("Dataset updated.")

    def _update_points(self):
        set = self.dset[self._set_index(2411)]
        for i in range(len(self.points)):
            set["x"][i], set["y"][i], set["z"][i] = self.points[i]
        print("Done points")

    def _update_elements(self):
        pass
