#!/usr/bin/env python3
import os


def calculate_fuel_cost(positions: list[int]):
    median_position = median(positions)
    return sum(abs(position - median_position) for position in positions)


def median(xs: list[int]):
    sorted = [x for x in xs]
    sorted.sort()
    return (sorted[(len(sorted) - 1) // 2] + sorted[len(sorted) // 2]) / 2


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input7.txt")) as f:
        positions = [int(x) for x in f.readline().strip().split(",")]

    best_position = calculate_fuel_cost(positions)
    print(best_position)
