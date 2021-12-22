#!/usr/bin/env python3
import os

Coordinates = tuple[int, int]


def parse_line_coordinates(f) -> list[tuple[Coordinates, Coordinates]]:
    line_coordinates: list[tuple[Coordinates, Coordinates]] = []
    for line in f:
        coordinates_string = line.strip().split(" -> ")
        x1, y1 = [int(c) for c in coordinates_string[0].split(",")]
        x2, y2 = [int(c) for c in coordinates_string[1].split(",")]
        line_coordinates.append(((x1, y1), (x2, y2)))
    return line_coordinates


def mark_line_coordinates(x: int, y: int, to_mark):
    key = make_key(x, y)
    existing = to_mark.get(key)
    if existing is None:
        to_mark[key] = 1
    else:
        to_mark[key] = existing + 1


def make_key(x, y):
    return f"{x}-{y}"


def count_most_dangerous_areas(
    line_coordinates: list[tuple[Coordinates, Coordinates]]
) -> int:
    number_of_lines: dict[tuple[int, int], int] = {}
    for (x1, y1), (x2, y2) in line_coordinates:
        if x1 != x2 and y1 != y2:
            continue
        elif x1 == x2:
            start, end = min(y1, y2), max(y1, y2)
            for y in range(start, end + 1):
                mark_line_coordinates(x1, y, number_of_lines)
        else:
            start, end = min(x1, x2), max(x1, x2)
            for x in range(start, end + 1):
                mark_line_coordinates(x, y1, number_of_lines)

    return sum(1 if v >= 2 else 0 for (_, v) in number_of_lines.items())


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input5.txt")) as f:
        line_coordinates = parse_line_coordinates(f)

    print(count_most_dangerous_areas(line_coordinates))
