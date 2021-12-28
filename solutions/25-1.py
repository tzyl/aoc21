#!/usr/bin/env python3
import os


def count_steps_until_stationary(sea_cucumber_grid: list[list[str]]) -> int:
    steps = 0
    moves = -1
    while moves != 0:
        steps += 1
        sea_cucumber_grid, moves = step(sea_cucumber_grid)
    return steps


def step(sea_cucumber_grid: list[list[str]]) -> tuple[list[list[str]], int]:
    m = len(sea_cucumber_grid)
    n = len(sea_cucumber_grid[0])
    next_sea_cucumber_grid = [["."] * n for _ in range(m)]
    moves = 0

    # Move east-facing herd
    for i in range(m):
        for j in range(n):
            if sea_cucumber_grid[i][j] == ">":
                if sea_cucumber_grid[i][(j + 1) % n] == ".":
                    next_sea_cucumber_grid[i][(j + 1) % n] = ">"
                    moves += 1
                else:
                    next_sea_cucumber_grid[i][j] = ">"

    # Move south-facing herd
    for i in range(m):
        for j in range(n):
            if sea_cucumber_grid[i][j] == "v":
                if (
                    sea_cucumber_grid[(i + 1) % m][j] != "v"
                    and next_sea_cucumber_grid[(i + 1) % m][j] == "."
                ):
                    next_sea_cucumber_grid[(i + 1) % m][j] = "v"
                    moves += 1
                else:
                    next_sea_cucumber_grid[i][j] = "v"

    return next_sea_cucumber_grid, moves


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input25.txt")) as f:
        sea_cucumber_grid = [[c for c in line.strip()] for line in f]

    print(count_steps_until_stationary(sea_cucumber_grid))
