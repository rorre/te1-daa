import random

C = 4
rand = random.Random()


def compare_exchange(a: list[int], i: int, j: int):
    if (i < j and a[i] > a[j]) or (i > j and a[i] < a[j]):
        a[i], a[j] = a[j], a[i]


def permute_random(a: list[int]):
    for i in range(len(a)):
        j = rand.randint(0, len(a) - 1 - i) + i
        a[i], a[j] = a[j], a[i]


def compare_regions(a: list[int], s: int, t: int, offset: int):
    mate: list[int] = [0] * offset
    for count in range(C):
        for i in range(offset):
            mate[i] = i

        permute_random(mate)  # Comment for deterministic shell sort
        for i in range(offset):
            compare_exchange(a, s + i, t + mate[i])


def fori(start: int, end: int, gap: int):
    """Function to simulate `for (int i = start; i < end; i += gap)` loop"""
    i = start
    while i < end:
        yield i
        i += gap


def randomized_shellsort(a: list[int]):
    n = len(a)
    offset = n // 2
    while offset > 0:
        for i in fori(0, n - offset, offset):
            compare_regions(a, i, i + offset, offset)

        for i in range(n - offset, offset - 1, -offset):
            compare_regions(a, i - offset, i, offset)

        for i in fori(0, n - 3 * offset, offset):
            compare_regions(a, i, i + 3 * offset, offset)

        for i in fori(0, n - 2 * offset, offset):
            compare_regions(a, i, i + 2 * offset, offset)

        for i in fori(0, n, 2 * offset):
            compare_regions(a, i, i + offset, offset)

        for i in fori(offset, n - offset, 2 * offset):
            compare_regions(a, i, i + offset, offset)

        offset //= 2
