#!/usr/bin/env python3
import os


def count_increases(xs: list[int]) -> int:
    count = 0
    current = xs[0]

    for i in range(1, len(xs)):
        next = xs[i]
        if next - current > 0:
            count += 1
        current = next

    return count


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input1.txt")) as f:
        measurements = [int(line) for line in f]
    print(count_increases(measurements))
