#!/usr/bin/env python3
import os
import re
from typing import Literal

INPUT_REGEX_PATTERN = re.compile(
    r"(?P<on_or_off>on|off) "
    r"x=(?P<min_x>-?\d+)\.\.(?P<max_x>-?\d+),"
    r"y=(?P<min_y>-?\d+)..(?P<max_y>-?\d+),"
    r"z=(?P<min_z>-?\d+)..(?P<max_z>-?\d+)"
)

RebootStep = tuple[
    Literal["on", "off"], tuple[int, int], tuple[int, int], tuple[int, int]
]


def parse_input(
    f,
) -> list[RebootStep]:
    reboot_steps: list[RebootStep] = []
    for line in f:
        m = INPUT_REGEX_PATTERN.match(line.strip())
        if m is None:
            raise ValueError("Expected input match")
        reboot_step: RebootStep = (
            "on" if m.group("on_or_off") == "on" else "off",
            (int(m.group("min_x")), int(m.group("max_x"))),
            (int(m.group("min_y")), int(m.group("max_y"))),
            (int(m.group("min_z")), int(m.group("max_z"))),
        )
        reboot_steps.append(reboot_step)
    return reboot_steps


def count_cubes_on(reboot_steps: list[RebootStep]) -> int:
    grid = [[[0] * 101 for _ in range(101)] for _ in range(101)]
    for on_or_off, (min_x, max_x), (min_y, max_y), (min_z, max_z) in reboot_steps:
        if (
            min_x > 50
            or max_x < -50
            or min_y > 50
            or max_y < -50
            or min_z > 50
            or max_z < -50
        ):
            continue
        min_x = max(min_x, -50)
        max_x = min(max_x, 50)
        min_y = max(min_y, -50)
        max_y = min(max_y, 50)
        min_z = max(min_z, -50)
        max_z = min(max_z, 50)
        for i in range(min_x, max_x + 1):
            for j in range(min_y, max_y + 1):
                for k in range(min_z, max_z + 1):
                    grid[i + 50][j + 50][k + 50] = 1 if on_or_off == "on" else 0
    return sum(
        grid[i][j][k] for i in range(101) for j in range(101) for k in range(101)
    )


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input22.txt")) as f:
        reboot_steps = parse_input(f)

    print(count_cubes_on(reboot_steps))
