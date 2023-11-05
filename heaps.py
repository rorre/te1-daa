def downheap(heap: list[int], n: int, pos: int):
    highest = pos
    left_idx = 2 * pos + 1
    right_idx = 2 * pos + 2

    if left_idx < n and heap[left_idx] > heap[highest]:
        highest = left_idx

    if right_idx < n and heap[right_idx] > heap[highest]:
        highest = right_idx

    if highest != pos:
        heap[pos], heap[highest] = heap[highest], heap[pos]
        downheap(heap, n, highest)


def heapsort(arr: list[int]):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        downheap(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        downheap(arr, i, 0)
