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


def count_sliding_window_increases(xs: list[int]) -> int:
    count = 0
    first, second, third = xs[0], xs[1], xs[2]

    for i in range(3, len(xs)):
        fourth = xs[i]
        start = first + second + third
        end = start - first + fourth
        if end - start > 0:
            count += 1
        first, second, third = second, third, fourth

    return count


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input1.txt")) as f:
        measurements = [int(line) for line in f]

    print("Part One:")
    print(count_increases(measurements))

    print("Part Two:")
    print(count_sliding_window_increases(measurements))
