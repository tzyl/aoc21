#!/usr/bin/env python3
import os


def calculate_fuel_cost(positions: list[int], target: int) -> int:
    return sum(triangle_number(abs(x - target)) for x in positions)


def triangle_number(n: int) -> int:
    return n * (n + 1) // 2


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input7.txt")) as f:
        positions = [int(x) for x in f.readline().strip().split(",")]

    best_position = min(
        calculate_fuel_cost(positions, i)
        for i in range(min(positions), max(positions) + 1)
    )
    print(best_position)
