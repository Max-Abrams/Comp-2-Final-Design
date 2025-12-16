# algorithms/dynamic_array.py

# Sources: https://www.pythonpool.com/python-dynamic-array/ 
# https://www.bomberbot.com/python/mastering-dynamic-arrays-in-python-a-comprehensive-guide-for-efficient-data-structures/ 
# ChatGPT for correcting an issue relating to __setitem__ method

import ctypes

class DynamicArray(object):
    # constructor
    def __init__(self, capacity: int = 32):
        self.capacity = capacity
        self.size = 0
        self.A = self.make_array(self.capacity)

    # get the size of the array
    def __len__(self):
        return self.size

    # add a new element to the end of the array
    def append(self, element):
        if self.size == self.capacity:
            self._resize(2 * self.capacity)
        self.A[self.size] = element
        self.size += 1

    # create a new array with the given capacity
    def _resize(self, c):
        B = self.make_array(c)
        for i in range(self.size):
            B[i] = self.A[i]
        self.A = B
        self.capacity = c

    # get an element from a specific index number
    def __getitem__(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index is out of bounds!")
        return self.A[index]

    # place an element at a specific index number
    def __setitem__(self, index, value):
        if index < 0 or index >= self.capacity:
            raise IndexError("Index is out of bounds!")
        if index >= self.size:
            self.size = index + 1
        self.A[index] = value

    # return a new array with the 'new_capacity' capacity
    def make_array(self, c):
        return (c * ctypes.py_object)()

    # basic swap function
    def swap(self, i, j):
        self.A[i], self.A[j] = self.A[j], self.A[i]

    # remove an element at a specific index number
    def pop(self):
        if self.size == 0:
            raise IndexError("Can't pop, array is empty!")
        popped_element = self.A[self.size - 1]
        self.A[self.size - 1] = None
        self.size -= 1
        return popped_element