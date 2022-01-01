#!/usr/bin/env python3
import os


def calculate_fuel_cost_part_one(positions: list[int]) -> float:
    median_position = median(positions)
    return sum(abs(position - median_position) for position in positions)


def median(xs: list[int]) -> float:
    sorted_xs = sorted(xs)
    return (sorted_xs[(len(sorted_xs) - 1) // 2] + sorted_xs[len(sorted_xs) // 2]) / 2


def calculate_fuel_cost_part_two(positions: list[int]) -> int:
    return min(
        sum(triangle_number(abs(x - i)) for x in positions)
        for i in range(min(positions), max(positions) + 1)
    )


def triangle_number(n: int) -> int:
    return n * (n + 1) // 2


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input7.txt")) as f:
        positions = [int(x) for x in f.readline().strip().split(",")]

    print("Part One:")
    print(calculate_fuel_cost_part_one(positions))

    print("Part Two:")
    print(calculate_fuel_cost_part_two(positions))
