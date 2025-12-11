from typing import Optional, Callable

# imported and adapted from lab 5

class bst:

    class node:
        # constructor for initializing an empty bst node class
        def __init__(self, val: int, key: float) -> None:
            self.val = val     #the object itself (e.g. Material)
            self.key = key     #attribute number (e.g. bandgap number)
            self.left  = None
            self.right = None

    # constructor for initializing an empty bst class
    def __init__(self, key_extractor: Callable)  -> None:
        self.root = None
        self.key_extractor = key_extractor  # function to extract attribute number from the object
        self.counter = [0,0,0]
    

    ## INSERTION
    # method for internal mechanics of bst insertion
    def insert_recursive(self,root: Optional[node],val) -> node:
        key_pull = self.key_extractor(val)
        if root is None:
            return self.node(val, key_pull)
        if key_pull < root.key:
            root.left = self.insert_recursive(root.left , val)
        else:
            root.right = self.insert_recursive(root.right , val)
        return root

    # insert method used to call insert_recursive method, avoids user needing to handle a root attribute
    def insert(self,val) -> None:
        self.root = self.insert_recursive(self.root,val)


    ## RANGE QUERY
    # method for internal mechanics of range query
    def range_query_recursive(self, curr_node: Optional[node], low: int, high: int, result: list) -> None:
        if curr_node is None:
            return
    
        # grab numeric part of tuple only, if key is a tuple
        if isinstance(curr_node.key, tuple):
            k = curr_node.key[0]
        else:
          k = curr_node.key

        if low <= k:
            self.range_query_recursive(curr_node.left, low, high, result)
        if low <= k <= high:
            result.append(curr_node.val)
        if k <= high:
            self.range_query_recursive(curr_node.right, low, high, result)

    # range query method called by user
    def range_query(self, low: int, high: int) -> list:
        result = []
        self.range_query_recursive(self.root, low, high, result)
        return result    
    

    ## SEARCH (FOR TIME COMPLEXITY PLOTTING)
    # added a (recursive) search method for the plotter to calculate time complexity
    # counting nodes is a different operation type and gave odd results
    def search_recursive(self, curr_node=None, search_val=0) -> bool:
        if curr_node is None:
            return False

        k = curr_node.key[0] if isinstance(curr_node.key, tuple) else curr_node.key
        if k == search_val:
            return True
        if search_val > k:
            return self.search_recursive(curr_node.right, search_val)
        else:
            return self.search_recursive(curr_node.left, search_val)
    
    # search method used to call search_recursive method, avoids user needing to handle a root attribute
    def search(self,search_val: int) -> bool:
        return self.search_recursive(self.root,search_val)
