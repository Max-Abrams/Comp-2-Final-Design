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
from datastructures.graph import Graph 
from query_interface.query_interface import Query_Interface

if __name__ == "__main__":

    # load the db
    all_materials = []
    for i, row in db.df.iterrows():
        mat = Material(row)
        all_materials.append(mat)

    #Instantiate the CLI
    cli = Query_Interface(all_materials)

    #Start query interface
    cli.start()