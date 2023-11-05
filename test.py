import gc
import json
import random
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Callable, Literal, NoReturn, ParamSpec, Tuple, TypeVar

import heaps
import shells

# We do manual garbage collection, so that the memory calculation isn't erroneous
gc.disable()

DataType = Literal["sorted", "random", "reversed"]
T = TypeVar("T")
P = ParamSpec("P")
TYPES = ("sorted", "random", "reversed")
SIZES = (2**9, 2**13, 2**16)

# Start tracing memory allocations with tracemalloc
tracemalloc.start()


def measure_metric(f: Callable[P, T]) -> Callable[P, Tuple[int, float, T]]:
    """Decorator to wrap given function to measure the time and memory usage"""

    def wrapped(*args: P.args, **kwargs: P.kwargs):
        # Collect all garbage, set our gc to be in clean state before taking snapshot
        gc.collect()
        t_start = time.time()
        first = tracemalloc.take_snapshot()

        result = f(*args, **kwargs)

        second = tracemalloc.take_snapshot()
        t_end = time.time()

        # size_diff is in bytes, so we have to divide by 1024 later
        # t_end - t_start is in seconds
        return (
            second.compare_to(first, "filename")[0].size_diff,
            t_end - t_start,
            result,
        )

    return wrapped


# Wrap all of our test functions
heapsort = measure_metric(heaps.heapsort)
randomized_shellsort = measure_metric(shells.randomized_shellsort)


def test(arr: list[int], data_type: str, data_size: int):
    """Tests given array and returns the result for both heapsort and randomized shell sort"""
    result = {
        "type": data_type,
        "size": data_size,
        "heapsort": {
            "memory": 0,
            "time": 0.0,
        },
        "shellsort": {
            "memory": 0,
            "time": 0.0,
        },
    }
    new_arr = arr.copy()
    memory, t, _ = heapsort(new_arr)
    assert new_arr == sorted(arr)

    result["heapsort"]["memory"] = memory
    result["heapsort"]["time"] = t

    new_arr = arr.copy()
    memory, t, _ = randomized_shellsort(new_arr)
    assert new_arr == sorted(arr)

    result["shellsort"]["memory"] = memory
    result["shellsort"]["time"] = t

    Path(f"dataset/{data_type}/{data_size}/").mkdir(exist_ok=True, parents=True)
    with open(f"dataset/{data_type}/{data_size}/result.json", "w") as f:
        json.dump(result, f)
    with open(f"dataset/{data_type}/{data_size}/dataset.json", "w") as f:
        json.dump(arr, f)


def generate_dataset(size: int, data_type: DataType):
    """Generates dataset based on size and data type"""
    arr = list(range(size))
    if data_type == "random":
        random.shuffle(arr)
    elif data_type == "reversed":
        arr = list(reversed(arr))
    return arr


def help_and_exit() -> NoReturn:
    print(f"Usage: {sys.argv[0]} <type> <size> [--reuse]")
    print("   type: either 'sorted', 'random', or 'reversed'")
    print("   size: array size")
    print("--reuse: reuse existing dataset")
    exit()


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        help_and_exit()

    size = int(sys.argv[2])
    data_type = sys.argv[1]
    if len(sys.argv) == 3:
        if data_type not in TYPES:
            help_and_exit()

        arr = generate_dataset(size, data_type)

    else:
        if sys.argv[3] != "--reuse":
            help_and_exit()

        with open(f"dataset/{data_type}/{size}/dataset.json") as f:
            arr = json.load(f)

    test(arr, sys.argv[1], size)
