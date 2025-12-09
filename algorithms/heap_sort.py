# algorithms/heap_sort.py

## Implementation of max heap sort algorithm

# Heapifies a subtree with root node 'i' which is an index in heap_array
def heapifier(heap_array: list, n: int, i: int) -> None:
    # largest value = root
    largest = i
    
    # define left and right child indices
    left = 2 * i + 1     
    right = 2 * i + 2 

    # check if each child exists and ensure the root is the largest value
    if left < n and heap_array[i] < heap_array[left]:
        largest = left
    if right < n and heap_array[largest] < heap_array[right]:
        largest = right

    # if the largest isn't the root, change it, then recursively heapify the affected sub-tree
    if largest != i:
        heap_array[i], heap_array[largest] = heap_array[largest], heap_array[i]  # swap
        heapifier(heap_array, n, largest)


# Main function to do heap sort
def heapSorter(heap_array: list) -> list:
    n = len(heap_array) # define size of array

    # Build heap or rearrange array
    for i in range(n // 2 - 1, -1, -1): # start from last internal node and decrement to root
        heapifier(heap_array, n, i)

    # Extract elements 1 by 1
    for i in range(n - 1, 0, -1): # decrement from last index to beginning

        # Remove the max element and place at the end (sorted position)
        heap_array[0], heap_array[i] = heap_array[i], heap_array[0]

        # Call max heapify on the reduced heap (heap size is i now)
        heapifier(heap_array, i, 0)
    return heap_array