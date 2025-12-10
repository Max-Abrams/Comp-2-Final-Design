# Quick sort from lab 8
import random

#need to add a key so we can extract based on a specific attribute
def base_sort(arr: list, key=lambda x: x):
    """
    The default sorting algorithm to use when no special pattern is detected.
    Args:
        arr: List of comparable elements
        
    Returns:
        list: New sorted list
    """
    # partition function
    def partition(arr, low, high):
        pivot_index = random.randint(low, high)
        arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            #Here, we are now comparinq based on the key the user provides
            if key(arr[j]) <= key(pivot):
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[high] = arr[high], arr[i+1]
        return i + 1

    # swap function
    def swap(arr: list, i: int, j: int) -> None:
        arr[i], arr[j] = arr[j], arr[i]

    # the QuickSort function implementation
    def quickSort(arr: list, low: int, high: int) -> None:
        if low < high:
            pi = partition(arr, low, high)
            
            # recursion calls for smaller elements
            # and greater or equals elements
            quickSort(arr, low, pi - 1)
            quickSort(arr, pi + 1, high)

    sorted_arr = arr.copy()
    quickSort(sorted_arr, 0, len(sorted_arr) - 1)
    return sorted_arr