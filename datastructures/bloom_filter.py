import random
import math


#taken from lab 07
class BloomFilter:
    def __init__(self, m: int, k: int, hash_fns: list):
        """
        Parameters
        ----------
        m : int
            Number of bits in the filter
        k : int
            Number of hash functions
        hash_fns : list[callable]
            List of functions that each take a key and return an integer in [0, m)
        """
        self.m = m
        self.k = k
        self.bits = [0] * m
        self.hash_fns = hash_fns


    #add items to bloom filter
    def add(self, key: str) -> None:
        #loop through hash functions
        for fn in self.hash_fns:
            #hash given key each time
            i = fn(self.m, key)
            #here we are flipping the bit at the hashed index to be 1, or "here"
            self.bits[i] = 1

    #check to see if key is *probably* in the filter
    def contains(self, key: str) -> bool:
        #loop through hash functions again
        for fn in self.hash_fns:
            #hash key each time
            i = fn(self.m, key)
            #if we run into a zero, we know it's DEFINITELY not in the bloom filter
            if self.bits[i] == 0:
                return False
        #else we know it probably is, so we can return true
        return True

    def __repr__(self):
        return f"BloomFilter(m={self.m}, k={self.k}, bits_set={sum(self.bits)})"
    
    #need to allow these to handle integers
    #Googled for this 
def string_to_int(key):
    if isinstance(key, int):
        return key
    hash_val = 0
    #its standard to use 31 as the multiplier, apparently
    for char in key:
        hash_val = (hash_val * 31 + ord(char))
    
    # Use 0xFFFFFFFF to keep the number within 32-bit bounds.
    # This prevents the integer from getting too big
    return hash_val & 0xFFFFFFFF


#I'll start by using our most simple hash function
def hash_fn_3(m, key):
    #just mod the key by the size of the has table
    key = string_to_int(key) 
    hashed = (key * 17) % m
    return hashed

# Now I'll use  classic multiplicative method. I used the source to help with this
def hash_fn_2(m, key):
    key = string_to_int(key)
    #I'll use the golden ratio for our prime number, which we learned about in class
    gr = 0.618
    #now multiply the size of the hash table by the GR and the key
    #then mod by 1 to get the remainder
    hashed = math.floor(m * ((key * gr) % 1))
    return hashed

#Finally, I'll use a bitwise function 
def hash_fn_1(m, key):
    key = string_to_int(key)
    #create a new, bit-manipulated key. 
    #This line shifts the given key twice then performs an XOR operation. 
    new_key = (key << 5) ^ (key >> 3)
    #then, as usual, mod the key by the hash's size
    return new_key % m

#To satsify the graphing requirements, I'll make a 4th and 5th hash

#Now I'll comibine the multiplicative with a bitshift 
def hash_fn_4(m, key):
    key = string_to_int(key)
    gr = 0.618
    # Use a different mix
    new_key = math.floor(key * gr) + (key >> 4) 
    return new_key % m

#Now I'll do another final simple one and pick an arbitray prime
def hash_fn_5(m, key):
    key = string_to_int(key)
    hashed = (key * 31) % m
    return hashed 
