from datastructures.heap import MinBinaryHeap

# basic algo to get top k items from the heap
def top_k(iterable: list, k: int, pull_val) -> list:
    heap = MinBinaryHeap()

    # build a min heap of size k
    # go through full list, pushing each item onto the heap
    for i in iterable:
        val = pull_val(i) #extract value to compare
        if val is None:
            continue
        heap.push((val, i.data_id, i)) #include tuple to break ties and prevent error
        if len(heap.data) > k: # build to size k
            heap.pop()

    top_k_list = []
    # extract items from heap into final list
    while heap.peek() is not None:
        val, jid, i = heap.pop()
        top_k_list.append(i)
    top_k_list.reverse()
    return top_k_list
