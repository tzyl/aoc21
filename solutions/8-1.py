#!/usr/bin/env python3
import os


def parse_input(f) -> list[tuple[list[set[str]], list[set[str]]]]:
    return [parse_line(line) for line in f]


def parse_line(line) -> tuple[list[set[str]], list[set[str]]]:
    left, right = line.strip().split(" | ")
    signal_patterns = [make_segment_set(pattern) for pattern in left.split(" ")]
    output_patterns = [make_segment_set(pattern) for pattern in right.split(" ")]
    return signal_patterns, output_patterns


def make_segment_set(pattern: str) -> set[str]:
    return set(c for c in pattern)


def is_unique_segment_set(segment_set: set[str]) -> bool:
    return (
        len(segment_set) == 2  # Unique segment count for 1
        or len(segment_set) == 4  # Unique segment count for 4
        or len(segment_set) == 3  # Unique segment count for 7
        or len(segment_set) == 7  # Unique segment count for 8
    )


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input8.txt")) as f:
        entries = parse_input(f)

    print(
        sum(
            is_unique_segment_set(pattern)
            for _, output_patterns in entries
            for pattern in output_patterns
        )
    )
