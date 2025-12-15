# JARVIS 3D DFT Materials Database Explorer


## Project Overview
This project is a database system built on top of the **JARVIS 3D DFT materials dataset**. It allows users to efficiently store, search, filter, sort, and analyze materials using custom-built data structures and algorithms.

The goal of the project is to implement a materials database using custom-built data structures and algorithms written from scratch, selecting the appropriate data structures for the query type, analyzing time complexity, and demonstrating algorithmic reasoning on materials data.


## Features
- Lookup materials by material ID or space group
- Query materials by numeric ranges (density, energy, moment, SLME)
- Find top-k materials by any numeric attribute
- Compute median materials using full sorting
- Bloom filter for probabilistic exclusion searches
- Build a material similarity graph and recommend similar materials
- Fully interactive CLI


## Dataset
- **Source:** https://jarvis.nist.gov/
- **Format:** CSV
- **Size:** 1000 materials (small demo dataset)
- **Attributes used (subset):**
  - `jid` (material ID)
  - `formula`
  - `spg_number` and `spg_symbol`
  - `density`
  - `magmom_total`
  - `optb88vdw_total_energy`
  - `slme`
  - `atom_elements`


  ## Project Structure
- `main.py` – Program entry point and CLI
- `Materials/` – Domain classes (`Material`, `SpaceGroup`, `Atom`)
- `datastructures/` – Custom data structure implementations
- `algorithms/` – Sorting and query algorithms
- `databases/` – Dataset loading and database logic
- `tests/` – Complexity tests


## Data Structures and Algorithms Used
- Hash Table: O(1) lookup by material ID and space group
- Binary Search Tree (BST): Numeric range queries
- Heap (Min Binary Heap): Top-K queries
- Graph (Adjacency List): Material similarity relationships
- Bloom Filter: Fast probabilistic exclusion searches
- QuickSort: Fully ordered lists for median and full ranking. Average time complexity of O(n log n)
- HeapSort: Fully ordered lists with O(n log n) worst-case


## How to Run

### Requirements
- Python 3.9+
- External libraries:
  - pandas
  - numpy

### Installation
From the project root directory, run:

```bash
python -m pip install pandas numpy
```

### Running the Program
1. Clone the repository and navigate into the project root directory.
2. The program automatically loads the included CSV dataset from the `databases/` directory. No additional configuration is required.
3. From the project root directory:

```bash
python main.py
```
This will load the included materials dataset, build all required data structures, 
and launch the command-line interface.


## Expected Output

When the program starts, you should see:

```text
Data loading complete.

============================================================
Hello, esteemed material scientist! How can I help you today?

Please enter a number corresponding to your desired action:
1: Lookup material by name or spacegroup.
2: Find a range of materials, based on your desired attribute.
3: Find top-rated material, based on your desired attribute.
4: Do a QUICK search, to see if a material with your desired atom might exist.
5: Find the median material, based on your desired attribute.
6: Build similarity graph and find similar materials.
0: Exit program.
============================================================
```

Entering 0 exits the program:
```text
Exiting program. Goodbye!
```