# datastructures/bst_lab5plotter.py

# this is copied straight from lab 5 and works with the current bst implementation. adapt as needed.

import time
import math
import matplotlib.pyplot as plt
from bst import bst
import sys

sys.setrecursionlimit(20000)

# benchmarking function to measure and plot time complexity of balanced and unbalanced BST searches
# creates a tree of n size, then searches for nodes, measuring execution time
# prints times for reference and plots them using matplotlib.
def benchmark_time() -> None:
    ns = [10, 100, 1000, 10000]
    unscaled_theoretical_balanced_times = []
    unscaled_theoretical_unbalanced_times = []
    theoretical_balanced_times = []
    theoretical_unbalanced_times = []
    simulated_balanced_times = []
    simulated_unbalanced_times = []

    # recursively inserts median elements to build a balanced BST
    def insert_median(asc_array: list[int]) -> None:
        if asc_array ==[]:
            return
        median_index = len(asc_array) // 2
        median_value = asc_array[median_index]
        simulated_balanced_tree.insert(median_value)
        insert_median(asc_array[:median_index])
        insert_median(asc_array[median_index+1:])
    
    for n in ns:
        simulated_unbalanced_tree = bst(key_extractor=lambda x: x) # creates a new unbalanced BST with a key extractor
        for i in range(n):
            simulated_unbalanced_tree.insert(i)
        start = time.time()
        for i in range(n):
            simulated_unbalanced_tree.search(i)
        end = time.time()
        simulated_unbalanced_times.append((end - start) / n)

        simulated_balanced_tree = bst(key_extractor=lambda x: x) # creates a new balanced BST with a key extractor
        asc_array = []
        for i in range(n):
            asc_array.append(i)
        insert_median(asc_array)
        start = time.time()
        for i in range(n):
            simulated_balanced_tree.search(i)
        end = time.time()
        simulated_balanced_times.append((end - start) / n)


    for n in ns:
        unscaled_theoretical_balanced_times.append(math.log2(n))
        unscaled_theoretical_unbalanced_times.append(n)

    scalar_balanced = simulated_balanced_times[0] / unscaled_theoretical_balanced_times[0]
    scalar_unbalanced = simulated_unbalanced_times[0] / unscaled_theoretical_unbalanced_times[0]

    for n in ns:    
        theoretical_balanced_times.append(scalar_balanced * math.log2(n))
        theoretical_unbalanced_times.append(scalar_unbalanced * n)


    plt.plot(ns, simulated_balanced_times, label="Simulated Balanced BST", color="b")
    plt.plot(ns, simulated_unbalanced_times, label="Simulated Unbalanced BST", color="r")
    plt.plot(ns, theoretical_balanced_times, ':', label=" Theoretical Balanced BST", color="b")
    plt.plot(ns, theoretical_unbalanced_times, ':', label="Theoretical Unbalanced BST", color="r")

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("Avg time (sec)")
    plt.title("Theoretical vs Simulated Time Complexities for Binary Search Trees")
    plt.legend()
    plt.savefig("plots.pdf", dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    benchmark_time()