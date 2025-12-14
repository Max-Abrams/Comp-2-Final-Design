from databases.MaterialDB import MaterialDatabase
from material import Material

class Atom(Material):
    def __init__(self, symbol, data_row):
        self._symbol = symbol

    def display(self):
        return f"<Atom: {self.symbol}, Atomic Number: {self.atomic_number}, Atomic Mass: {self.atomic_mass}>"