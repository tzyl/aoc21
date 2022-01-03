#!/usr/bin/env python3
import os
from typing import Generator


def count_flashes(energy_levels: list[list[int]], steps: int) -> int:
    to_step = [[energy_levels[i][j] for j in range(10)] for i in range(10)]
    total_flashes = 0
    for _ in range(steps):
        flashed = step(to_step)
        total_flashes += len(flashed)
    return total_flashes


def count_steps_until_synchronized(energy_levels: list[list[int]]) -> int:
    to_step = [[energy_levels[i][j] for j in range(10)] for i in range(10)]
    steps = 0
    while not is_synchronized(to_step):
        step(to_step)
        steps += 1
    return steps


def is_synchronized(energy_levels: list[list[int]]) -> bool:
    return all(energy_levels[i][j] == 0 for i in range(10) for j in range(10))


def step(energy_levels: list[list[int]]) -> set[tuple[int, int]]:
    """Simulate a step and return the positions of the octopuses which flashed
    during this step."""
    for i in range(10):
        for j in range(10):
            energy_levels[i][j] += 1

    flashed = set()
    while True:
        new_flashes = set()
        for i in range(10):
            for j in range(10):
                if energy_levels[i][j] > 9 and (i, j) not in flashed:
                    flashed.add((i, j))
                    new_flashes.add((i, j))

        for i, j in new_flashes:
            for x, y in get_neighbors(i, j):
                energy_levels[x][y] += 1

        if not new_flashes:
            break

    for i, j in flashed:
        energy_levels[i][j] = 0

    return flashed


def get_neighbors(i: int, j: int) -> Generator[tuple[int, int], None, None]:
    offsets = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    for dx, dy in offsets:
        if 0 <= i + dx < 10 and 0 <= j + dy < 10:
            yield i + dx, j + dy


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input11.txt")) as f:
        energy_levels = [[int(c) for c in line.strip()] for line in f]

    print("Part One:")
    print(count_flashes(energy_levels, 100))

    print("Part Two:")
    print(count_steps_until_synchronized(energy_levels))
