class SpaceGroup:
    def __init__(self, data_row):
        self.symbol = data_row["spg_symbol"]
        self.number = data_row["spg_number"]
        self.crystal_system = data_row["crys"]

    def display(self):
        return f"[SpaceGroup: {self.symbol} (#{self.number}), System: {self.crystal_system}]"
