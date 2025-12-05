import sys
import os
from spacegroup import SpaceGroup

#Kept getting import error for db. So needed Gemini to help me with this
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from databases.MaterialDB import db

class SpaceGroup:
    def __init__(self, data_row):
        self.symbol = data_row['spg_symbol']
        self.number = data_row['spg_number']
        self.crystal_system = data_row['crys']

    def display(self):
        return f"[SpaceGroup: {self.symbol} (#{self.number}), System: {self.crystal_system}]"