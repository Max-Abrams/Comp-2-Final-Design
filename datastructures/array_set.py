from .dynamic_array import DynamicArray

class ArraySet:

    
    def __init__(self):
        #use dynamic array for storage
        self.data = DynamicArray()
    
    def add(self, x):
        #add element to set if not already in set
        if not self.contains(x):
            self.data.append(x)

    def contains(self, x):
        #check if element is already in set
        for i in range(len(self.data)):
            if self.data[i] == x:
                return True
        return False
