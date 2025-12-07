from datastructures.bloom_filter import BloomFilter


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
