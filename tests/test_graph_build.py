import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Materials.material import Material
from databases.MaterialDB import db
from datastructures.graph import Graph  # ensure this exists


def build_graph(sample_size):
    """Build similarity graph using shared atoms"""
    sample = db.df.sample(min(sample_size, len(db.df)))

    materials = []
    for _, row in sample.iterrows():
        materials.append(Material(data_row=row))

    g = Graph()

    # Insert nodes
    for mat in materials:
        g.add_node(mat)

    # Add edges weighted by shared atoms
    for i in range(len(materials)):
        for j in range(i + 1, len(materials)):
            shared = materials[i].clean_atoms & materials[j].clean_atoms
            if shared:
                g.add_edge(materials[i], materials[j], weight=len(shared))

    return g, materials


def find_material_by_formula(materials, formula):
    """Helper: find first match by formula"""
    for m in materials:
        if m.formula.lower() == formula.lower():
            return m
    return None


def main():
    print("\n==== SIMILARITY GRAPH TEST ====\n")

    user_formula = input("Enter a material formula to search (e.g., Fe2O3): ").strip()

    test_sizes = [50, 500, 5000]

    for size in test_sizes:
        print(f"\n--- Building graph from {size} materials ---")

        t0 = time.time()
        graph, materials = build_graph(size)
        build_time = (time.time() - t0) * 1000

        print(f"Graph build time: {build_time:.2f} ms")

        query = find_material_by_formula(materials, user_formula)

        if not query:
            print(f"⚠ '{user_formula}' not found in this sample.")
            continue

        neighbors = graph.get_neighbors(query)
        if not neighbors:
            print(f"No similarity edges found for {user_formula} in this subset")
            continue

        print(f"\nSimilar materials to {user_formula}:")
        for nbr, weight in neighbors:
            print(f"  {nbr.formula}  (shared atoms = {weight})")

    print("\n✓ Similarity graph test complete!\n")


if __name__ == "__main__":
    main()
