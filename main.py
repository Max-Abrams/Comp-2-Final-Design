from datastructures.hash_table import hash_table
from datastructures.linked_list import linked_list
from datastructures.bst import bst
from algorithms.hash_search import lookup as hash_lookup
from Materials.material import Material
from Materials.spacegroup import SpaceGroup
from databases.MaterialDB import db
from algorithms.bloom_search import contains as bf_search
from datastructures.bloom_filter import BloomFilter


class MaterialHashTable(hash_table):
    def extract_key(self, value): 
        return value.name

if __name__ == "__main__":
    #Instantiating data structures
    ht = MaterialHashTable(200)
    energy_bst = bst(key_extractor=lambda m: m.density)
    atom_bf = BloomFilter(1000, 3) 

    # load the db--- ONCE!
    for i, row in db.df.iterrows():
        mat = Material(row)
        ht.insert(mat)

        energy_bst.insert(mat)

        #Need to insert each atom in the last into bf
        #so loop through
        for atom in mat.clean_atoms:
            #And just add
            atom_bf.add(atom)


    # test hash search
    test = hash_lookup(ht, "DyB6")
    if test: 
        test[0].display()
    else:
        print("Material not found")

    test = hash_lookup(ht, "NaCl")
    if test: 
        test[0].display()
    else:
        print("Material not found")


    low, high = 5.4192, 5.4315
    results = energy_bst.range_query(low, high)

    print(f"BST range query: density between [{low}, {high}]")
    print("Total count of materials that satisfy the search criteria:", len(results))
    print("First 5 results:")
    for m in results[:5]:
        print(m.formula, m.density)



    #Bloom search
    test = bf_search("Na")
    if test: 
        print("I mean, it's probably here!")
    else:
        print("DEF not!")

    #Bloom search
    test = bf_search("Ar")
    if test: 
        print("I mean, it's probably here!")
    else:
        print("DEF not!")
