from datastructures.hash_table import hash_table
from datastructures.linked_list import linked_list
from datastructures.bst import bst
from datastructures.heap import MinBinaryHeap
from algorithms.hash_search import lookup as hash_lookup
from algorithms.heap_sort import heapSorter
from algorithms.top_k import top_k
from Materials.material import Material
from Materials.spacegroup import SpaceGroup
from databases.MaterialDB import db
from algorithms.bloom_search import contains as bf_search
from datastructures.bloom_filter import BloomFilter, hash_fn_1, hash_fn_2, hash_fn_3, hash_fn_4, hash_fn_5
from algorithms.quick_sort import base_sort


class MaterialHashTable(hash_table):
    def extract_key(self, value): 
        return value.name

if __name__ == "__main__":
    #Instantiating data structures
    ht = MaterialHashTable(200)
    density_bst = bst(key_extractor=lambda m: m.density)
    atom_bf = BloomFilter(1000, 3, [hash_fn_3, hash_fn_4, hash_fn_5, hash_fn_1, hash_fn_2]) 

    # load the db--- ONCE!
    all_materials = []
    for i, row in db.df.iterrows():
        mat = Material(row)
        all_materials.append(mat)
        ht.insert(mat)
        density_bst.insert(mat)

        #Need to insert each atom in the last into bf
        #so loop through
        for atom in mat.clean_atoms:
            #And just add
            atom_bf.add(atom)


    # test hash search
    #test = hash_lookup(ht, "DyB6")
    #if test: 
        #test[0].display()
    #else:
        #print("Material not found")

    #test = hash_lookup(ht, "NaCl")
    #if test: 
     #   test[0].display()
    #else:
     #   print("Material not found")
    #print("\n")

    ## test BST range query
    #low, high = 5.4192, 5.4315
    #results = density_bst.range_query(low, high)

    #print(f"BST range query: density between [{low} and {high}]")
    #print("Total count of materials that satisfy the search criteria:", len(results))
    #print("First 5 results:")
    #for m in results[:5]:
     #   print(m.formula, m.density)
    #print("\n")
    
    
    ## test HeapSort on densities
    #density_list = []
    #for i, row in db.df.iterrows():
     #   mat = Material(row)
      #  density_list.append((mat.density, mat.data_id, mat)) # ID added to (arbitrarily) break ties (ties=errors)

    #sorted_pairs = heapSorter(density_list)

    #printnum = 15
    # find the longest formula so alignment is even
    #max_formula_len = max(len(mat.formula) for _, _, mat in sorted_pairs[:printnum])

    # print formatted output
    #print(f"Heapsort: {printnum} lowest density materials:")
    #for density, jid, mat in sorted_pairs[:printnum]:
     #   print(f"{mat.formula:<{max_formula_len}}  {density:>10.4f}")
    #print("\n")


    #Bloom search
    #test = bf_search(atom_bf, "Na")
    #if test: 
     #   print("I mean, it's probably here!")
    #else:
        #print("DEF not!")

    #Bloom search
    #test = bf_search(atom_bf, "Ar")
    #if test: 
     #   print("I mean, it's probably here!")
    #else:
     #   print("DEF not!")


    # test heap data structure on top-k
    # use '-m.density' for max-heap behavior and smallest densities
    #k=8
    #best = top_k(all_materials, k=k, pull_val=lambda m: m.density)
    #print(f"\nTop {k} highest density materials from BST range query:")
    #for m in best:
     #   print(f"{m.formula}: {m.density}")

    #test quick sort
    #sorted_materials = base_sort(all_materials, key=lambda m: ((m.data_id, str(m.formula))))     #Tuple here because quick sort is unstable. So in equal cases, need to break ties
    #median_index = len(sorted_materials) // 2
    #print(f"Median material by formula (quick sort): {sorted_materials[median_index].formula}")

    print("Data loading complete.")
    while True:
        print("\n")
        print("Hello, esteemed material scientist! How can I help you today?\n")
        print("Please enter a number corresponding to your desired action:")
        print("1: Lookup material by name.")
        print("2: Find a range of materials, based on your desired attribute.")
        print("3: Find top-rated material, based on your desired attribute.")
        print("4: Do a QUICK search, to see if a material with your desired atom might exist.")
        print("5: Find the median material, based on your desired attribute.")
        print("0: Exit program.")

        choice = input("Enter your choice: ")

        if choice == '1':
            new_mat_in = input("\nPlease enter what material you would like to find: ")
            new_mat = hash_lookup(ht, new_mat_in)
            if new_mat: 
                new_mat[0].display()
            else:
                print("Material not found. Please try again.\n")
        elif choice == '2':
            print("\nOn which attribute would you like to perform your ranged query?\n")
            print("Please enter a number:")
            print("1: Density")
            print("2: Moment")
            print("3: Total Energy of system--usually negative!")
            attr_choice = input("Enter your choice: ")
            num = int(input("As a maximum, how many results would you like to see?\n"))
            if attr_choice not in ['1', '2', '3']:
                print("Invalid choice. Returning to main menu.")
                continue
            elif attr_choice == '1':
                key_extractor = lambda m: m.density
                searched_val = "density"
            elif attr_choice == '2':
                key_extractor = lambda m: m.moment
                searched_val = "moment"
            elif attr_choice == '3':
                key_extractor = lambda m: m.energy
                searched_val = "total energy"
            low = float(input("Enter the lower bound of the range: "))
            high = float(input("Enter the upper bound of the range: "))
            user_bst = bst(key_extractor)
            results = bst.range_query(low, high)
            print(f"BST range query: {searched_val} between [{low} and {high}]")
            print("\nTotal count of materials that satisfy the search criteria:\n", len(results))             #CANT HANDLE NEGATIVES?
            for m in results[:num]:
                print(m.formula, m.density)
            print("\n")

        elif choice == '3':
            print("\nFind top-rated material based on:")
            print("1: Density")
            print("2: Moment")
            print("3: Total Energy")
            attr_choice = input("Enter your choice: ")

            if attr_choice == '1':
                key_func = lambda m: m.density
            elif attr_choice == '2':
                key_func = lambda m: m.moment
            elif attr_choice == '3':
                key_func = lambda m: m.energy
            else:
                print("Invalid choice.")
                continue

            try:
                k = int(input("How many top results? "))
                for_dups = k * 20
                #This BST prints a lot of duplicates. Need to fix that. 
                best = top_k(all_materials, k=for_dups, pull_val=key_func)
                avoid_dups = []
                count = 0
                print(f"\nTop {k} results:")
                for m in best:
                    if m.formula not in avoid_dups:
                        avoid_dups.append(m.formula)
                        print(f"{count+1}: {m.formula} : {key_func(m)}")

                        count += 1
                        if count == k:
                            break

            except ValueError:
                print("Invalid number.")

        elif choice == '4':
            atom_in = input("\nEnter the element you are looking for! (e.g. 'Na'): ")
            if bf_search(atom_bf, atom_in):
                print(f"Bloom Filter: Element '{atom_in}' is PROBABLY present.")
            else:
                print(f"Bloom Filter: Element '{atom_in}' is DEFINITELY NOT present.")

        elif choice == '5':
            print("\nWhat median value are you searching for?:")
            print("1: Density")
            print("2: Moment")
            print("3: Total Energy")
            attr_choice = input("Enter choice: ")

            # As above, needed to make this a stable search. It doesn't actually change time complexity much, after amortization
            if attr_choice == '1':
                sort_key = lambda m: (m.density, m.data_id)
            elif attr_choice == '2':
                sort_key = lambda m: (m.moment, m.data_id)
            elif attr_choice == '3':
                sort_key = lambda m: (m.energy, m.data_id)
            else:
                print("Invalid choice.")
                continue

            print("Sorting...")
            sorted_materials = base_sort(all_materials, key=sort_key)
            median_index = len(sorted_materials) // 2
            mid_mat = sorted_materials[median_index]

            print(f"Median material: {mid_mat.formula}")
            
            # Print the value to confirm
            if attr_choice == '1': print(f"Density: {mid_mat.density}")
            elif attr_choice == '2': print(f"Moment: {mid_mat.moment}")
            elif attr_choice == '3': print(f"Energy: {mid_mat.energy}")

        elif choice == '0':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Sorry, I didn't understand that choice. Please try again.")