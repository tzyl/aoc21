#!/usr/bin/env python3
import heapq
import math
import os
from typing import Generator


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
        risk_levels = [[int(c) for c in line.strip()] for line in f]

    lowest_total_risk_path = find_lowest_total_risk_path(risk_levels)
    print(sum(risk_levels[i][j] for i, j in lowest_total_risk_path[1:]))
