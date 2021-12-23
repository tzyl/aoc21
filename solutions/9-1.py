#!/usr/bin/env python3
import os
from typing import Generator


def parse_input(f) -> list[list[int]]:
    return [[int(c) for c in line.strip()] for line in f]


def sum_risk_level(heightmap: list[list[int]]) -> int:
    return sum(1 + heightmap[i][j] for (i, j) in find_low_points(heightmap))


def find_low_points(heightmap: list[list[int]]) -> list[tuple[int, int]]:
    m = len(heightmap)
    n = len(heightmap[0])
    return [(i, j) for i in range(m) for j in range(n) if is_low_point(heightmap, i, j)]


def is_low_point(heightmap: list[list[int]], i: int, j: int) -> bool:
    m = len(heightmap)
    n = len(heightmap[0])
    return all(
        heightmap[x][y] > heightmap[i][j] for (x, y) in get_neighbours(i, j, m, n)
    )


def get_neighbours(
    i: int, j: int, m: int, n: int
) -> Generator[tuple[int, int], None, None]:
    if i > 0:
        yield i - 1, j
    if j > 0:
        yield i, j - 1
    if i + 1 < m:
        yield i + 1, j
    if j + 1 < n:
        yield i, j + 1


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input9.txt")) as f:
        heightmap = parse_input(f)

    print(sum_risk_level(heightmap))
