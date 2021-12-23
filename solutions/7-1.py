#!/usr/bin/env python3
import os


def calculate_fuel_cost(positions: list[int]):
    median_position = median(positions)
    return sum(abs(position - median_position) for position in positions)


def median(xs: list[int]):
    sorted_xs = sorted(xs)
    return (sorted_xs[(len(sorted_xs) - 1) // 2] + sorted_xs[len(sorted_xs) // 2]) / 2


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input7.txt")) as f:
        positions = [int(x) for x in f.readline().strip().split(",")]

    best_position = calculate_fuel_cost(positions)
    print(best_position)
