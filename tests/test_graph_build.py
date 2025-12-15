import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Materials.material import Material
from databases.MaterialDB import db
from datastructures.graph import Graph
import numpy as np


#Graph build using density similarity metric
def build_graph(sample_size, density_threshold=0.5):
    sample = db.df.sample(min(sample_size, len(db.df)))

    #Convert rows into Material objects
    materials = []
    for _, row in sample.iterrows():
        try:
            mat = Material(row)
            if not np.isnan(mat.density):  # ensure valid numeric density
                materials.append(mat)
        except Exception:
            continue

    graph = Graph()

    #Add all materials as nodes
    for m in materials:
        graph._add_node(m)

    edge_count = 0

    #Compare each pair ONLY by density for testing
    for i in range(len(materials)):
        for j in range(i + 1, len(materials)):
            d1 = materials[i].density
            d2 = materials[j].density
            diff = abs(d1 - d2)

            #build edge only if density is higher than threshold
            if diff <= density_threshold:
                weight = 1 / (1 + diff)
                graph._add_edge(materials[i], materials[j], weight)
                edge_count += 1

    return graph, materials, edge_count


#Find material by formula string
def find_material_by_formula(materials, formula):
    formula = formula.lower()
    return next((m for m in materials if m.formula.lower() == formula), None)


def main():
    print("\n==== MATERIAL DENSITY SIMILARITY GRAPH ====\n")

    #user prompt and test sizes
    user_formula = input("Enter material formula (e.g., Fe2O3): ").strip()
    test_sizes = [50, 500, 5000, 50000]  

    
    for size in test_sizes:
        print(f"\n--- Graph Build Using {size} Materials ---")

        #log times for build
        t0 = time.time()
        graph, materials, edges = build_graph(size, density_threshold=0.5)
        build_time = (time.time() - t0) * 1000

        print(f"Build Time: {build_time:.2f} ms")
        print(f"Nodes: {len(materials)}, Edges: {edges}")

        #if material not found in sample, output response
        query = find_material_by_formula(materials, user_formula)
        if not query:
            print(f"{user_formula}' not found in this sample.")
            continue

        #if no materials found in similarity range, output response
        if query not in graph.nodes:
            print(f"No similar-density matches found for '{user_formula}'.")
            continue

        
        q_idx = graph.nodes.index(query)
        neighbors = [(graph.nodes[i], w) for i, w in graph.adj[q_idx]]

        if not neighbors:
            print(f"No similar-density matches found for '{user_formula}'.")
            continue

        #Sort by descending similarity (highest weight)
        neighbors_sorted = sorted(neighbors, key=lambda x: x[1], reverse=True)

        print(f"\nTop Similar Materials by Density to '{user_formula}':")
        #Print top 10 results in similarity sorted list
        for nbr, w in neighbors_sorted[:10]:
            print(f"  - {nbr.formula}   (similarity score: {w:.3f})")

    print("\nDensity similarity test complete.\n")


if __name__ == "__main__":
    main()
