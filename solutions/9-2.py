#!/usr/bin/env python3
import os
from math import prod
from typing import Generator


def parse_input(f) -> list[list[int]]:
    return [[int(c) for c in line.strip()] for line in f]


def find_basin_sizes(heightmap: list[list[int]]) -> dict[tuple[int, int], int]:
    return {
        low_point: find_basin_size(heightmap, low_point)
        for low_point in find_low_points(heightmap)
    }


def find_basin_size(heightmap: list[list[int]], low_point: tuple[int, int]) -> int:
    m = len(heightmap)
    n = len(heightmap[0])
    basin: set[tuple[int, int]] = set([low_point])
    to_visit: list[tuple[int, int]] = [low_point]
    while to_visit:
        i, j = to_visit.pop()
        for x, y in get_neighbours(i, j, m, n):
            if (
                heightmap[x][y] != 9
                and heightmap[x][y] > heightmap[i][j]
                and (x, y) not in basin
            ):
                basin.add((x, y))
                to_visit.append((x, y))
    return len(basin)


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

    basin_sizes_by_low_point = find_basin_sizes(heightmap)
    print(
        prod(
            basin_sizes_by_low_point[low_point]
            for low_point in sorted(
                basin_sizes_by_low_point,
                key=lambda k: basin_sizes_by_low_point[k],
                reverse=True,
            )[:3]
        )
    )
