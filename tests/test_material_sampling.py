# tests/test_material_sampling.py

# --- Make project root importable ---
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from Materials.material import Material
from databases.MaterialDB import db

def sample_materials(n_samples: int):
    total_rows = len(db.df)
    n_samples = min(n_samples, total_rows)
    sampled_rows = random.sample(list(db.df.to_dict(orient='records')), n_samples)
    return [Material(data_row=row) for row in sampled_rows]

def main():
    sample_sizes = [50, 500, 5000]

    for n in sample_sizes:
        print(f"\n=== Sampling {n} materials ===")
        materials = sample_materials(n)
        print(f"Loaded {len(materials)} materials.")
        print("First 5 formulas:")
        for m in materials[:5]:
            print(f"  - {m.formula}")

if __name__ == "__main__":
    main()
