from datastructures.hash_table import hash_table 

def lookup(ht, key, disp=False):
    # Use the hash function belonging to the passed object
    index = ht.hash_function(key)
    
    # Access the buffer of the passed object
    retValTmp = ht.buffer[index].lookup(target=key, field='key')
    retVal = [r.value for r in retValTmp]

    if disp:
        print("Search of " , key , " found:")
        if retVal:
            for v in retVal:
                print("\t",end="")
                print(v)
        else: 
            print("\tNothing")
            
    return retVal
