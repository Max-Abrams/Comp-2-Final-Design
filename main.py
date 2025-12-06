from datastructures.hash_table import hash_table
from datastructures.linked_list import linked_list
from datastructures.bst import bst
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
    if res: 
        res[0].display()
    else:
        print("Material not found")



    # test range query for bst
    energy_bst = bst(key_extractor=lambda m: m.density)

    for i, row in db.df.iterrows():
        energy_bst.insert(Material(row['formula'], row))

    low, high = 5.4192, 5.4315
    results = energy_bst.range_query(low, high)

    print(f"BST range query: density between [{low}, {high}]")
    print("Total count of materials that satisfy the search criteria:", len(results))
    print("First 5 results:")
    for m in results[:5]:
        print(m.formula, m.density)