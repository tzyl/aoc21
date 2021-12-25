#!/usr/bin/env python3
import heapq
import math
import os
from typing import Generator


def generate_full_risk_levels(risk_levels_tile: list[list[int]]) -> list[list[int]]:
    m = len(risk_levels_tile)
    n = len(risk_levels_tile[0])
    risk_levels = [[0] * 5 * n for _ in range(5 * m)]
    for tile_x in range(5):
        for tile_y in range(5):
            for i in range(m):
                for j in range(n):
                    adjusted_i = (m * tile_x) + i
                    adjusted_j = (n * tile_y) + j
                    adjusted_risk_level = (
                        (risk_levels_tile[i][j] + tile_x + tile_y - 1) % 9
                    ) + 1
                    risk_levels[adjusted_i][adjusted_j] = adjusted_risk_level
    return risk_levels


def find_lowest_total_risk_path(risk_levels: list[list[int]]) -> list[tuple[int, int]]:
    m = len(risk_levels)
    n = len(risk_levels[0])
    visited = [[False] * n for _ in range(m)]
    distances = [[math.inf] * n for _ in range(m)]
    previous: list[list[tuple[int, int] | None]] = [[None] * n for _ in range(m)]
    priority_queue: list[tuple[int, tuple[int, int]]] = []

    distances[0][0] = 0
    heapq.heappush(priority_queue, (0, (0, 0)))

    while priority_queue:
        current_distance, (i, j) = heapq.heappop(priority_queue)
        visited[i][j] = True
        for x, y in get_neighbours(i, j, m, n):
            if not visited[x][y]:
                candidate_distance = current_distance + risk_levels[x][y]
                if candidate_distance < distances[x][y]:
                    distances[x][y] = candidate_distance
                    previous[x][y] = (i, j)
                    heapq.heappush(priority_queue, (candidate_distance, (x, y)))

    lowest_total_risk_path = [(m - 1, n - 1)]
    i, j = m - 1, n - 1
    while (previous_value := previous[i][j]) is not None:
        lowest_total_risk_path.append(previous_value)
        i, j = previous_value
    return lowest_total_risk_path[::-1]


def get_neighbours(
    i: int, j: int, m: int, n: int
) -> Generator[tuple[int, int], None, None]:
    offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dx, dy in offsets:
        if 0 <= i + dx < m and 0 <= j + dy < n:
            yield i + dx, j + dy


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input15.txt")) as f:
        risk_levels_tile = [[int(c) for c in line.strip()] for line in f]

    risk_levels = generate_full_risk_levels(risk_levels_tile)
    lowest_total_risk_path = find_lowest_total_risk_path(risk_levels)
    print(sum(risk_levels[i][j] for i, j in lowest_total_risk_path[1:]))
