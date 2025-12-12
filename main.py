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
from datastructures.graph import Graph  # <-- NEW
import time


class MaterialHashTable(hash_table):
    def extract_key(self, value):
        return value.name

class SpaceGroupHashTable(hash_table):
    def extract_key(self, value):
        return value.space_group.number


if __name__ == "__main__":
    #Instantiating data structures
    ht = MaterialHashTable(200)
    sg_ht = SpaceGroupHashTable(100)
    density_bst = bst(key_extractor=lambda m: m.density)
    atom_bf = BloomFilter(1000, 3, [hash_fn_3, hash_fn_4, hash_fn_5, hash_fn_1, hash_fn_2])

    # load the db--- ONCE!
    all_materials = []
    for i, row in db.df.iterrows():
        mat = Material(row)
        all_materials.append(mat)
        ht.insert(mat)
        sg_ht.insert(mat)

        for atom in mat.clean_atoms:
            atom_bf.add(atom)

    print("Data loading complete.")
    while True:
        print("\n")
        print("============================================================")
        print("Hello, esteemed material scientist! How can I help you today?\n")
        print("Please enter a number corresponding to your desired action:")
        print("1: Lookup material by name or spacegroup.")
        print("2: Find a range of materials, based on your desired attribute.")
        print("3: Find top-rated material, based on your desired attribute.")
        print("4: Do a QUICK search, to see if a material with your desired atom might exist.")
        print("5: Find the median material, based on your desired attribute.")
        print("6: Build similarity graph and find similar materials.")  # <-- NEW
        print("0: Exit program.")
        print("============================================================")
        print("\n")

        choice = input("Enter your choice: ")

        if choice == '1':
            m_or_s = input("Would you like to find a Material or Space Group? (m/s): ").lower()
            if m_or_s == "m":
                new_mat_in = input("\nPlease enter what material you would like to find: ")
                new_mat = hash_lookup(ht, new_mat_in)
                if new_mat:
                    new_mat[0].display()
                    input("Press enter to return.")
                else:
                    print("Material not found. Please try again.\n")
                    input("Press enter to return.")

            elif m_or_s == "s":
                sg_in = int(input("\nPlease enter the space group number you would like to find: "))
                try:
                    sg_num = int(sg_in)
                    disp = int(input("How many materials should I display: "))

                    found_materials = hash_lookup(sg_ht, sg_num)

                    if found_materials:
                        count = 0
                        print(f"\nFound {len(found_materials)} materials in Space Group {sg_num}:")
                        for mat in found_materials:
                            if count < disp:
                                print(f"- {mat.formula} (ID: {mat.data_id})")
                                count +=1
                        input("\nPress enter to return.")
                    else:
                        print(f"\nNo materials found in Space Group {sg_num}.\n")
                        input("Press enter to return.")

                except ValueError:
                    print("Invalid space group number. Please try again.\n")
                    input("Press enter to return.")

        elif choice == '2':
            print("\nOn which attribute would you like to perform your ranged query?\n")
            print("Please enter a number:")
            print("1: Density")
            print("2: Moment")
            print("3: Total Energy of system--usually negative!")
            print("4: Spectroscopic Limited Maximum Efficiency (SLME)")
            attr_choice = input("Enter your choice: ")
            num = int(input("As a maximum, how many results would you like to see?\n"))
            if attr_choice not in ['1', '2', '3', '4']:
                print("Invalid choice. Returning to main menu.")
                continue
            elif attr_choice == '1':
                key_extractor = lambda m: m.density
                searched_val = "density"
            elif attr_choice == '2':
                def moment_key(m):
                    if m.moment is None:
                        return None
                    return (m.moment, m.data_id)
                key_extractor = moment_key
                searched_val = "moment"
            elif attr_choice == '3':
                key_extractor = lambda m: m.energy
                searched_val = "total energy"
            elif attr_choice == '4':
                def slme_key(m):
                    if m.slme is None:
                        return None
                    return (m.slme, m.data_id)
                key_extractor = slme_key
                searched_val = "slme"
            low = float(input("Enter the lower bound of the range: "))
            high = float(input("Enter the upper bound of the range: "))
            user_bst = bst(key_extractor)
            for m in all_materials:
                val = key_extractor(m)
                if val is not None:
                    user_bst.insert(m)
            results = user_bst.range_query(low, high)
            print(f"BST range query: {searched_val} between [{low} and {high}]")
            print("\nTotal count of materials that satisfy the search criteria:", len(results))
            print("\n\n")
            for m in results[:num]:
                print(m.formula, key_extractor(m))
            print("\n")
            input("\nPress enter to return.")

        elif choice == '3':
            print("\nFind top-rated material based on:")
            print("1: Density")
            print("2: Moment")
            print("3: Total Energy")
            print("4: Spectroscopic Limited Maximum Efficiency (SLME)")
            attr_choice = input("Enter your choice: ")

            if attr_choice == '1':
                key_func = lambda m: m.density
            elif attr_choice == '2':
                key_func = lambda m: m.moment
            elif attr_choice == '3':
                key_func = lambda m: m.energy
            elif attr_choice == '4':
                key_func = lambda m: m.slme
            else:
                print("Invalid choice.")
                continue

            try:
                k = int(input("How many top results? "))
                for_dups = k * 20
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
                input("Press enter to return.")

            except ValueError:
                print("Invalid number.")
                input("Press enter to return.")

        elif choice == '4':
            atom_in = input("\nEnter the element you are looking for! (e.g. 'Na'): ")
            if bf_search(atom_bf, atom_in):
                print(f"Bloom Filter: Element '{atom_in}' is PROBABLY present.")
                input("Press enter to return.")

            else:
                print(f"Bloom Filter: Element '{atom_in}' is DEFINITELY NOT present.")
                input("Press enter to return.")

        elif choice == '5':
            print("\nWhat median value are you searching for?:")
            print("1: Density")
            print("2: Moment")
            print("3: Total Energy")
            print("4: Spectroscopic Limited Maximum Efficiency (SLME)")
            attr_choice = input("Enter choice: ")

            if attr_choice == '1':
                sort_key = lambda m: (m.density, m.data_id)
                data = all_materials
            elif attr_choice == '2':
                sort_key = lambda m: (m.moment, m.data_id)
                data = [m for m in all_materials if m.moment is not None]
            elif attr_choice == '3':
                sort_key = lambda m: (m.energy, m.data_id)
                data = all_materials
            elif attr_choice == '4':
                sort_key = lambda m: (m.slme, m.data_id)
                data = [m for m in all_materials if m.slme is not None]
            else:
                print("Invalid choice.")
                continue

            print("Sorting...")
            print("\n")
            sorted_materials = base_sort(data, key=sort_key)
            median_index = len(sorted_materials) // 2
            mid_mat = sorted_materials[median_index]

            print(f"Median material: {mid_mat.formula}")

            if attr_choice == '1': print(f"Density: {mid_mat.density}")
            elif attr_choice == '2': print(f"Moment: {mid_mat.moment}")
            elif attr_choice == '3': print(f"Energy: {mid_mat.energy}")
            elif attr_choice == '4': print(f"SLME: {mid_mat.slme}")
            print("\n")
            input("Press enter to return.")

        elif choice == '6':
            target_formula = input("Enter a material formula (e.g., SiO2): ").strip()
            target = next((m for m in all_materials if m.formula == target_formula), None)
            if not target:
                print(f"Material '{target_formula}' not found in dataset.")
                input("Press enter to return.")
                continue
            g = Graph()
            print("Building similarity graph...")
            
            edges = g.build_local_similarity_graph(all_materials, target, threshold=1.5)
            

            print(f"Graph built with {edges} edges" )

            target = next((m for m in all_materials if m.formula == target_formula), None)
            if not target:
                print(f"Material '{target_formula}' not found in dataset.")
                input("Press enter to return.")
                continue

            visited = g.bfs(target)
            print(f"Reachable materials: {len(visited)}")

            neighbors = g.adj.get(target, [])
            sorted_neighbors = sorted(neighbors, key=lambda x: x[1], reverse=True)

            print("\nTop 5 similar materials:")
            for neighbor, sim in sorted_neighbors[:5]:
                print(f"{neighbor.formula}: similarity = {sim:.3f}")

            input("Press enter to return.")

        elif choice == '0':
            print("Exiting program. Goodbye!")
            time.sleep(2)
            break

        else:
            print("Sorry, I didn't understand that choice. Please try again.")
            input("Press enter to return.")
