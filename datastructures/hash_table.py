from .linked_list import linked_list

class hash_table:

    class node:
        def __init__(self, k, v):
            self.key = k
            self.value = v

    def __init__(self, array_len = 50):
        #Hash table uses linked list as its buffer--that's two birds!
        self.buffer = [linked_list() for _ in range(array_len)]
        self.array_len = array_len

    def insert(self, value):
        key = self.extract_key(value)
        index = self.hash_function(key)
        self.buffer[index].insert( self.node(key,value) )
        
    # must be defined by the inheriting class
    #THIS MIGHT NOT WORK BECAUSE OF INTEGERS
    def hash_function(self, key):
        #Position sensitive hash function. Mods each character by its position
        key = str(key)       # force string
        s = 0
        it = 1
        for ch in key:
            #so creating our mod value to start off
            s += ord(ch) % it
            it += 1
        return s%self.array_len
 
    def extract_key(self, value): 
        raise NotImplementedError
        