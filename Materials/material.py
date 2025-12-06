import sys
import os
from .spacegroup import SpaceGroup

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#Kept getting import error for db. So needed Gemini to help me with this
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from databases.MaterialDB import db

class Material:
    #I presume we are keying this by formula name. The IDs are kind of weird and non-user friedly
    def __init__(self, formula_name, data_row = None):
        self.name = formula_name
        
        # Only search the DB if data_row wasn't passed in
        if data_row is None:
            #unfortunatley some formulas appear twice, so we need to handle that
            #Also need to handle the case where no matches are found. Thats an easy error handle


            #so later this look up will by handled using a Hash Table
            matches = db.df[db.df['formula'] == formula_name]
            #Extract the first row found. 
            data_row = matches.iloc[0]

        # 4. Assign attributes from the row
        self.density = data_row['density']
        self.data_id = data_row['jid']
        self.formula = data_row['formula']
        self.moment = data_row['magmom_oszicar']
        #made into a set to avoid dubplicates
        self.atoms = set(data_row['atoms.elements'].split(','))
        #also need to get rid of annoying brackets
        self.clean_atoms = set([atom.strip().strip("[]'") for atom in self.atoms])

        self.space_group = SpaceGroup(data_row)

    def display(self):
        print(f"found!! \n<Material: {self.name}, Density: {self.density}, Formula: {self.formula}>")
        print("Atoms contained:\n")
        for atom in self.clean_atoms:
            print(f"- {atom}")
        return "Done"