import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datastructures.bloom_filter import BloomFilter, hash_fn_1, hash_fn_2, hash_fn_3
from Materials.material import Material
from databases.MaterialDB import db



#Select random sampling of data with pandas
#Build bloom filter with 10000 bits and k hash functions
#Create set to hold unique atomic symbols
def build_filter(sample_size):
    sample = db.df.sample(min(sample_size, len(db.df)))
    bf = BloomFilter(m=10000, k=3, hash_fns=[hash_fn_1, hash_fn_2, hash_fn_3])
    atoms = set()


   #Loop through sample rows and extrract a material and its attributes storing as mat
   #clean atoms from material class
    for _, row in sample.iterrows():
        mat = Material(data_row=row)
        atoms.update(mat.clean_atoms)

    #Measure time to insert each atom into filter
    t0 = time.time()
    for atom in atoms:
        bf.add(atom)
    build_time = (time.time() - t0) * 1000  

    #return our filtered atoms, list of atoms, and build time
    return bf, list(atoms), build_time


def evaluate_filter(bf, atoms, user_atom):
    # known test atoms
    known_test = atoms[:10]

    # unknown atoms to measure false positives
    unknown_test = ["Rn"]
    test_cases = known_test + unknown_test

    false_positives = 0
    total_negatives = len(unknown_test)

    t1 = time.time()
    for atom in test_cases:
        result = bf.contains(atom)
        if atom in unknown_test and result:
            false_positives += 1
    query_time = (time.time() - t1) * 1000  # ms

    fp_rate = (false_positives / total_negatives) * 100

    #User input
    user_result = bf.contains(user_atom)

    return fp_rate, query_time, user_result


def main():

    #test outputs 
    print("\n==== BLOOM FILTER PERFORMANCE TEST ====\n")

    #user prompt for atom symbol
    user_atom = input("Enter an atom symbol to look up (example: O): ").strip()
    test_sizes = [50, 500, 5000]

    for size in test_sizes:
        print(f"\n--- Testing with {size} materials ---")

        bf, atoms, build_time = build_filter(size)
        fp_rate, query_time, user_result = evaluate_filter(bf, atoms, user_atom)

        #print times
        print(f"Unique atoms stored: {len(atoms)}")
        print(f"Build time: {build_time:.2f} ms")
        print(f"Query time: {query_time:.4f} ms")
        print(f"False Positive Rate: {fp_rate:.2f}%")

        #output results
        if user_result:
            print(f"\n{user_atom} is PROBABLY in the dataset.")
        else:
            print(f"\n{user_atom} is definitely NOT in the dataset.")

   
if __name__ == "__main__":
    main()
