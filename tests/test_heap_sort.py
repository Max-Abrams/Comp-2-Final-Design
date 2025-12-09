import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.heap_sort import heapSorter
from Materials.material import Material
from databases.MaterialDB import db

#Valid attributes for search
def get_valid_attributes():
    """Return numeric attributes available for sorting"""
    return ["density", "moment"]

#Random sampling from DB
def sample_material_values(sample_size, attribute):
    """Randomly sample materials & extract chosen numeric attribute"""
    sample = db.df.sample(min(sample_size, len(db.df)))

    #empty list for sampled materials and their values
    materials = []
    values = []

    for _, row in sample.iterrows():
        mat = Material(data_row=row)
        val = getattr(mat, attribute, None)

        #Skip invalid (None, NaN, strings like "na")
        #Moment still not working.. may need to update material.py
        try:
            val = float(val)
        except:
            continue

        materials.append(mat)
        values.append(val)

    return materials, values


def main():
    print("\n==== HEAP SORT INTERACTIVE TEST ====\n")

    #Provide user with valid attributes to search
    valid_attrs = get_valid_attributes()
    print("Available attributes:", ", ".join(valid_attrs))

    attribute = input("Enter attribute to heap sort: ").strip()

    #error handling for incorrect attribute
    if attribute not in valid_attrs:
        print(f"\n❌ ERROR: '{attribute}' is not a valid attribute!")
        print("Valid options are:", ", ".join(valid_attrs))
        return

    #top k prompt
    k = int(input("Show top K results — enter K: "))

    test_sizes = [50, 500, 5000]

    for size in test_sizes:
        print(f"\n--- Sorting {size} materials by '{attribute}' ---")

        materials, values = sample_material_values(size, attribute)

        if len(values) == 0:
            print(f"No valid values for attribute '{attribute}' in data sample.")
            continue

        t0 = time.time()
        sorted_vals = heapSorter(values[:])  # keep original list intact
        sort_time = (time.time() - t0) * 1000  # ms

        print(f"Sort Time: {sort_time:.3f} ms")
        print(f"Lowest {attribute}:  {sorted_vals[0]:.3f}")
        print(f"Highest {attribute}: {sorted_vals[-1]:.3f}")

        #rReverse sorted values to show highest first
        top_vals = list(reversed(sorted_vals))[:k]
        printed = set()

        print(f"\nTop {k} materials by {attribute}:")
        for val in top_vals:
            for m in materials:
                if getattr(m, attribute) == val and m.formula not in printed:
                    printed.add(m.formula)
                    print(f"  {m.formula}: {attribute}={val:.3f}")
                    break




if __name__ == "__main__":
    main()
