# tests/test_bst.py
import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datastructures.bst import bst
from Materials.material import Material
from databases.MaterialDB import db


#Build tree with bst class storing material values with temp value m 
#Randomly sample from pandas dataframe of csv
#Create empty materials list
def build_tree_from_sample(sample_size):
    sample = db.df.sample(min(sample_size, len(db.df)))
    tree = bst(lambda m: m.density)
    materials = []

    #Loop through each row of dataframe,extracting material and attributes
    #Append to materials list
    #insert into bst 
    for _, row in sample.iterrows():
        mat = Material(data_row=row)  
        materials.append(mat)
        tree.insert(mat)

    #Return built tree and list of materials in it    
    return tree, materials



def main():
    print("\n=== BST RANGE QUERY PERFORMANCE TEST ===")

    #prompt user for density range
    lo = float(input("Enter minimum density: "))
    hi = float(input("Enter maximum density: "))

    #test ranges
    test_sizes = [50, 500, 5000,50000]

    
    for size in test_sizes:
        print(f"\n--- Testing with {size} materials ---")

        #build tree
        t0 = time.time()
        tree, materials = build_tree_from_sample(size)
        build_time = time.time() - t0

        #perform range query
        t1 = time.time()
        results = tree.range_query(lo, hi)
        query_time = time.time() - t1

        #output test results
        print(f"Tree build time: {build_time*1000:.2f} ms")
        print(f"Range query time: {query_time*1000:.4f} ms")
        print(f"Materials found: {len(results)}")

        #show first 5 results in each test
        for m in results[:5]:
            print(f"  - {m.formula} (ρ={m.density:.3f})")

            

if __name__ == "__main__":
    main()
