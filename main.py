from datastructures.hash_table import hash_table
from datastructures.linked_list import linked_list
from datastructures.bst import bst
from algorithms.hash_search import lookup as hash_lookup
from algorithms.heap_sort import heapSorter
from Materials.material import Material
from Materials.spacegroup import SpaceGroup
from databases.MaterialDB import db
from algorithms.bloom_search import contains as bf_search
from datastructures.bloom_filter import BloomFilter, hash_fn_1, hash_fn_2, hash_fn_3, hash_fn_4, hash_fn_5


class MaterialHashTable(hash_table):
    def extract_key(self, value): 
        return value.name

if __name__ == "__main__":
    #Instantiating data structures
    ht = MaterialHashTable(200)
    density_bst = bst(key_extractor=lambda m: m.density)
    atom_bf = BloomFilter(1000, 3, [hash_fn_3, hash_fn_4, hash_fn_5, hash_fn_1, hash_fn_2]) 

    # load the db--- ONCE!
    for i, row in db.df.iterrows():
        mat = Material(row)
        ht.insert(mat)

        density_bst.insert(mat)

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
    print("\n")

    ## test BST range query
    low, high = 5.4192, 5.4315
    results = density_bst.range_query(low, high)

    print(f"BST range query: density between [{low} and {high}]")
    print("Total count of materials that satisfy the search criteria:", len(results))
    print("First 5 results:")
    for m in results[:5]:
        print(m.formula, m.density)
    print("\n")
    
    
    ## test HeapSort on densities
    density_list = []
    for i, row in db.df.iterrows():
        mat = Material(row)
        density_list.append((mat.density, mat.data_id, mat)) # ID added to (arbitrarily) break ties (ties=errors)

    sorted_pairs = heapSorter(density_list)

    printnum = 15
    # find the longest formula so alignment is even
    max_formula_len = max(len(mat.formula) for _, _, mat in sorted_pairs[:printnum])

    # print formatted output
    print(f"Heapsort: {printnum} lowest density materials:")
    for density, jid, mat in sorted_pairs[:printnum]:
        print(f"{mat.formula:<{max_formula_len}}  {density:>10.4f}")
    print("\n")


    #Bloom search
    test = bf_search(atom_bf, "Na")
    if test: 
        print("I mean, it's probably here!")
    else:
        print("DEF not!")

    #Bloom search
    test = bf_search(atom_bf, "Ar")
    if test: 
        print("I mean, it's probably here!")
    else:
        print("DEF not!")