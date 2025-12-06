from datastructures.hash_table import hash_table
from datastructures.linked_list import linked_list
from algorithms.hash_search import lookup
from Materials.material import Material
from Materials.spacegroup import SpaceGroup
from databases.MaterialDB import db

class MaterialHashTable(hash_table):
    def extract_key(self, value): 
        return value.name

if __name__ == "__main__":
    ht = MaterialHashTable(200)

    # load the db
    for i, row in db.df.iterrows():
        ht.insert(Material(row['formula'], row))

    # test search
    res = lookup(ht, "DyB6")
    if res: res[0].display()