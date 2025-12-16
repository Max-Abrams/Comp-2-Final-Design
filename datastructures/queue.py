from typing import Optional
from datastructures.dynamic_array import DynamicArray

# Source: Lab 3

class Queue():
    # constructor
    # input buffsize sets the fixed size of the buffer
    # two pointers are initialized to 0 to indicate empty queue
    def __init__(self , buffsize: int = 10) -> None:
        self.buffer = DynamicArray(buffsize)
        self.buffersize = buffsize
        self.start_pointer = 0
        self.end_pointer = 0
        self.current_size = 0

    # push <value> onto the queue modulo stack size, overwrite oldest element when full
    def push(self, value: int) -> None:
        if self.current_size == self.buffersize:
            raise ValueError("Buffer is full")
        self.buffer[self.end_pointer] = value
        self.end_pointer = (self.end_pointer + 1) % self.buffersize
        if self.current_size < self.buffersize:
            self.current_size += 1
        else:
            self.start_pointer = (self.start_pointer + 1) % self.buffersize
            

    # pop the first value from the queue, accounting for circularity
    # and return it. if the queue is empty, return <None>
    def pop(self) -> Optional[int]:
        if self.current_size != 0:
            target = self.buffer[self.start_pointer]
            self.buffer[self.start_pointer] = None
            self.start_pointer = (self.start_pointer + 1) % self.buffersize
            self.current_size -= 1
            return target
        return None

    # return the number of valid elements in the queue
    def count(self) -> int:
        return self.current_size