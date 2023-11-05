import json

TYPES = ("sorted", "random", "reversed")
SIZES = (2**9, 2**13, 2**16)


def print_result():
    for size in SIZES:
        for t in TYPES:
            print(t, size)
            try:
                with open(f"dataset/{t}/{size}/result.json") as f:
                    data = json.load(f)
            except FileNotFoundError:
                print("ERR: Cannot found result file, did the test fail?")
                print()
                print("------------------")
                continue

            print(
                "Shellsort",
                f'{round(data["shellsort"]["time"] * 1000)}ms',
                f'{round(data["shellsort"]["memory"] / 1024, 3)}KiB',
            )
            print(
                "Heapsort",
                f'{round(data["heapsort"]["time"] * 1000)}ms',
                f'{round(data["heapsort"]["memory"] / 1024, 3)}KiB',
            )
            print()
            print("------------------")


if __name__ == "__main__":
    print_result()
