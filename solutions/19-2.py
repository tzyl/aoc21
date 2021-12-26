#!/usr/bin/env python3
import os
from typing import Generator


def parse_input(f) -> list[set[tuple[int, int, int]]]:
    scanners = []

    while f.readline():
        beacons = set()
        line = f.readline().strip()
        while line:
            x, y, z = [int(s) for s in line.split(",")]
            beacons.add((x, y, z))
            line = f.readline().strip()
        scanners.append(beacons)

    return scanners


def assemble_full_map(
    scanners: list[set[tuple[int, int, int]]]
) -> tuple[set[tuple[int, int, int]], set[tuple[int, int, int]]]:
    beacon_map = scanners[0]
    scanner_map = set([(0, 0, 0)])
    unknown_scanners = set(range(1, len(scanners)))
    while unknown_scanners:
        for index in unknown_scanners:
            unknown_scanner = scanners[index]
            has_matched_scanner = False

            for (
                candidate_scanner,
                candidate_scanner_origin,
            ) in generate_scanner_positions(beacon_map, unknown_scanner):
                if is_correct_scanner_position(beacon_map, candidate_scanner):
                    print(f"Matched scanner {index}")
                    has_matched_scanner = True
                    beacon_map = beacon_map.union(candidate_scanner)
                    scanner_map.add(candidate_scanner_origin)
                    break

            if has_matched_scanner:
                unknown_scanners.remove(index)
                break
    return beacon_map, scanner_map


def is_correct_scanner_position(
    map: set[tuple[int, int, int]], scanner: set[tuple[int, int, int]]
) -> bool:
    return len(map.intersection(scanner)) >= 12


def generate_scanner_positions(
    map: set[tuple[int, int, int]], original_scanner: set[tuple[int, int, int]]
) -> Generator[tuple[set[tuple[int, int, int]], tuple[int, int, int]], None, None]:
    """Generate all possible scanner positions for the current state
    of the map. Attempts all 24 possible scanner orientations translated
    to line up with each of the existing map beacons."""
    for scanner_orientation in generate_scanner_orientations(original_scanner):
        for (
            scanner_translation,
            scanner_translation_origin,
        ) in generate_scanner_translations(map, scanner_orientation):
            yield scanner_translation, scanner_translation_origin


def generate_scanner_orientations(
    original_scanner: set[tuple[int, int, int]]
) -> Generator[set[tuple[int, int, int]], None, None]:
    """Generate each of the 24 possible orientations of the scanner."""
    for scanner_orientation in zip(*(sequence(beacon) for beacon in original_scanner)):
        yield set(scanner_orientation)


def generate_scanner_translations(
    map: set[tuple[int, int, int]], scanner_orientation: set[tuple[int, int, int]]
) -> Generator[tuple[set[tuple[int, int, int]], tuple[int, int, int]], None, None]:
    """Generate each of the translations to line up a scanner beacon
    position with one of the existing map beacon positions."""
    for original_x, original_y, original_z in map:
        for candidate_x, candidate_y, candidate_z in scanner_orientation:
            dx = candidate_x - original_x
            dy = candidate_y - original_y
            dz = candidate_z - original_z
            scanner_translation = set(
                [(x - dx, y - dy, z - dz) for x, y, z in scanner_orientation]
            )
            scanner_translation_origin = (0 - dx, 0 - dy, 0 - dz)
            yield scanner_translation, scanner_translation_origin


# https://stackoverflow.com/a/16467849
def roll(v: tuple[int, int, int]) -> tuple[int, int, int]:
    return (v[0], v[2], -v[1])


def turn(v: tuple[int, int, int]) -> tuple[int, int, int]:
    return (-v[1], v[0], v[2])


def sequence(v: tuple[int, int, int]) -> Generator[tuple[int, int, int], None, None]:
    for _ in range(2):
        for _ in range(3):  # Yield RTTT 3 times
            v = roll(v)
            yield (v)  # Yield R
            for _ in range(3):  # Yield TTT
                v = turn(v)
                yield (v)
        v = roll(turn(roll(v)))  # Do RTR


def manhattan_distance(v1: tuple[int, int, int], v2: tuple[int, int, int]) -> int:
    return abs(v1[0] - v2[0]) + abs(v1[1] - v2[1]) + abs(v1[2] - v2[2])


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input19.txt")) as f:
        scanners = parse_input(f)

    beacon_map, scanner_map = assemble_full_map(scanners)
    print(max(manhattan_distance(v1, v2) for v1 in scanner_map for v2 in scanner_map))
