import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datastructures.hash_table import hash_table
from Materials.material import Material
from databases.MaterialDB import db


#create a subclass that defines extract_key for atoms 
class AtomHashTable(hash_table):
    def extract_key(self, value):
        return value
    
#Build hash table with random sampling from DB
def build_hash_table(sample_size):
    sample = db.df.sample(min(sample_size, len(db.df)))

    #Create hashtable of unqiue atoms
    ht = AtomHashTable(array_len=1000)
    atoms = set()  

    #Build Material objects and extract cleaned atom symbols
    for _, row in sample.iterrows():
        mat = Material(data_row=row)
        atoms.update(mat.clean_atoms)

    #Insert atoms into hash table and time the process
    t0 = time.time()
    for atom in atoms:
        ht.insert(atom)
    build_time = (time.time() - t0) * 1000 

    return ht, list(atoms), build_time

#Time atom lookup
def lookup_atom(ht, atom):
    t0 = time.time()
    found = len(ht.buffer[ht.hash_function(atom)].lookup(target=atom, field='key')) > 0
    lookup_time = (time.time() - t0) * 1000  
    return found, lookup_time

#Count collisions 
def count_collisions(ht):
    return sum(1 for bucket in ht.buffer if bucket.head and bucket.head.next)


def main():
    print("\n==== HASH TABLE PERFORMANCE TEST ====\n")
    atom = input("Enter an atom symbol to look up in the hash table (e.g., O): ").strip()

    test_sizes = [50, 500, 5000, 50000]

    
    for size in test_sizes:
        print(f"\n--- Testing with {size} materials ---")

        ht, atoms, build_time = build_hash_table(size)

        found, lookup_time = lookup_atom(ht, atom)

        #Count collisions (list buckets with >1 item)
        collisions = count_collisions(ht)

        #Outputs
        print(f"Unique atoms stored: {len(atoms)}")
        print(f"Build time: {build_time:.2f} ms")
        print(f"Lookup time: {lookup_time:.5f} ms")
        print(f"Collisions: {collisions} buckets")

        if found:
            print(f"{atom} was found in the hash table.")
        else:
            print(f"{atom} was NOT found in the hash table.")




if __name__ == "__main__":
    main()
