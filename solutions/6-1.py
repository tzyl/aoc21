#!/usr/bin/env python3
import os


def number_of_lanternfish(target_n: int, target_t: int) -> int:
    cache: dict[tuple[int, int], int] = {}
    for n in range(9):
        cache[(n, 0)] = 1
    for t in range(1, target_t + 1):
        for n in range(9):
            if n == 0:
                cache[(n, t)] = cache[(6, t - 1)] + cache[(8, t - 1)]
            else:
                cache[(n, t)] = cache[(n - 1, t - 1)]
    return cache[(target_n, target_t)]


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input6.txt")) as f:
        start = [int(x) for x in f.readline().split(",")]

    total_lanternfish = sum(number_of_lanternfish(n, 80) for n in start)
    print(total_lanternfish)
