#!/usr/bin/env python3
import os


def parse_line(line: str) -> tuple[str, int]:
    split = line.split(" ")
    return split[0], int(split[1])


def find_position_and_depth(instructions: list[tuple[str, int]]) -> tuple[int, int]:
    position = 0
    depth = 0

    for (direction, amount) in instructions:
        if direction == "forward":
            position += amount
        elif direction == "down":
            depth += amount
        else:
            depth -= amount

    return position, depth


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input2.txt")) as f:
        instructions = [parse_line(line) for line in f]
    position, depth = find_position_and_depth(instructions)
    print(position * depth)
