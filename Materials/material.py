import sys
import os
from .spacegroup import SpaceGroup
from databases.MaterialDB import db

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#Kept getting import error for db. So needed Gemini to help me with this
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


def clean_na(x):
    try:
        return float(x)
    except:
        return None


class Material:
    #I presume we are keying this by formula name. The IDs are kind of weird and non-user friedly
    def __init__(self, data_row = None):
        self._name = data_row['formula']
    

    #OLD LOOKUP BY FORMULA NAME, didnt use hash 

        # Only search the DB if data_row wasn't passed in
        #if data_row is None:
            #unfortunatley some formulas appear twice, so we need to handle that
            #Also need to handle the case where no matches are found. Thats an easy error handle

            #accesses column "formula" in df, then checks for the searched formula name, then saves that value
            #matches = db.df[db.df['formula'] == formula_name]
            #Extract the first row found. 
            #data_row = matches.iloc[0]

        ####


        # 4. Assign attributes from the row
        self._density = clean_na(data_row.get("density"))
        self._data_id = data_row['jid']
        self._formula = data_row['formula']
        self._moment = clean_na(data_row.get("magmom_oszicar"))
        self._slme = clean_na(data_row.get("slme"))
        #made into a set to avoid dubplicates
        self._atoms = set(data_row['atoms.elements'].split(','))
        #also need to get rid of annoying brackets
        self.clean_atoms = set([atom.strip().strip("[]'") for atom in self._atoms])
        self._energy = clean_na(data_row.get("optb88vdw_total_energy"))
        self._space_group = SpaceGroup(data_row)


    #We added protections after testing
    #So now we need these decorators to avoid errors when accessing missing data
    @property
    def density(self):
        return self._density

    @property
    def energy(self):
        return self._energy

    @property
    def moment(self):
        return self._moment
    
    @property
    def formula(self):
        return self._formula
    
    @property
    def data_id(self):
        return self._data_id
    
    @property
    def name(self):
        return self._name
    
    @property
    def atoms(self):
        return self.clean_atoms
    
    @property
    def space_group(self):
        return self._space_group
    
    @property
    def slme(self):
        return self._slme
    
        
    def display(self):
        print(f"\nMaterial found! \n\nMaterial: {self.name}\nId: {self.data_id}\nDensity: {self.density}\nMagnetic Moment: {self.moment}\nSpace Group: {self.space_group.symbol} ({self.space_group.number})\n")
        print("Atoms contained:")
        for atom in self.clean_atoms:
            print(f"- {atom}")
        return "Done"
