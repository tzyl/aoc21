#!/usr/bin/env python3
import os


def calculate_fuel_cost_part_one(positions: list[int]) -> float:
    median_position = median(positions)
    median_floor = int(median_position)
    median_ceil = int(median_position + 1)
    return min(
        sum(abs(position - median_floor) for position in positions),
        sum(abs(position - median_ceil) for position in positions),
    )


def median(xs: list[int]) -> float:
    sorted_xs = sorted(xs)
    return (sorted_xs[(len(sorted_xs) - 1) // 2] + sorted_xs[len(sorted_xs) // 2]) / 2


def calculate_fuel_cost_part_two(positions: list[int]) -> int:
    mean = sum(x for x in positions) / len(positions)
    mean_floor = int(mean)
    mean_ceil = int(mean + 1)
    return min(
        sum(triangle_number(abs(x - mean_floor)) for x in positions),
        sum(triangle_number(abs(x - mean_ceil)) for x in positions),
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
