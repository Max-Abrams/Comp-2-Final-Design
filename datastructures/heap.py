#datastructures/heap.py
from typing import Optional, Any

## Implementation of a min binary heap data structure
class MinBinaryHeap():

    # basic constructor
    def __init__(self) -> None:
        self.data = []

    # peek at the minimum value of the heap
    def peek(self) -> Optional[Any]:
        if not self.data:
            return None
        return self.data[0]

    # helper to find parent index
    def _find_parent_idx(self, i: int) -> Optional[int]:
        if i == 0:
            return None
        return (i - 1) // 2 # discarding remainder works for right child too

    # insert new value in heap
    def push(self, value: Any) -> None:
        self.data.append(value)
        i = len(self.data)-1
        self._move_up(i)
    
    # helper to move a node up the heap to maintain heap property
    def _move_up(self, i: int) -> None:
        parent_idx = self._find_parent_idx(i)
        if parent_idx is None:
            return
        if self.data[parent_idx] > self.data[i]:
            parent_value = self.data[parent_idx]
            self.data[parent_idx] = self.data[i]
            self.data[i] = parent_value
            self._move_up(parent_idx)
        return
    
    # remove and return the minimum value from the heap
    def pop(self) -> Optional[Any]:
        if not self.data:
            return None
        if len(self.data) == 1:
            return self.data.pop()
        min_val = self.data[0]
        self.data[0] = self.data.pop()
        self._heapifier_down(0)
        return min_val

    # helper to move a node down the heap to maintain heap property
    def _heapifier_down(self, i: int) -> None:    

        heap_array = self.data
        n = len(heap_array)
        smallest = i

        # define left and right child indices
        left = 2 * i + 1     
        right = 2 * i + 2 

        # check if each child exists and ensure the root is the smallest value
        if left < n and heap_array[left] < heap_array[smallest]:
            smallest = left
        if right < n and heap_array[right] < heap_array[smallest]:
            smallest = right

        # if the smallest isn't the root, change it, then recursively heapify the affected sub-tree
        if smallest != i:
            heap_array[i], heap_array[smallest] = heap_array[smallest], heap_array[i]  # swap
            self._heapifier_down(smallest)
        return