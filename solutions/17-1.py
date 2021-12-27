#!/usr/bin/env python3
import os
import re

INPUT_REGEX_PATTERN = re.compile(
    r"target area: "
    r"x=(?P<min_x>\d+)\.\.(?P<max_x>\d+), "
    r"y=(?P<min_y>-?\d+)..(?P<max_y>-?\d+)"
)


def parse_input(f) -> tuple[int, int, int, int]:
    m = INPUT_REGEX_PATTERN.match(f.readline().strip())
    if m is None:
        raise ValueError("Expected input match")
    return (
        int(m.group("min_x")),
        int(m.group("max_x")),
        int(m.group("min_y")),
        int(m.group("max_y")),
    )


def max_trajectory_height(y_0: int) -> int:
    if y_0 <= 0:
        return 0
    # Based on the gravity rules the max trajectory height is 1 + 2 + ... + y_0
    # i.e. the y_0th triangle number.
    return y_0 * (y_0 + 1) // 2


def find_initial_velocity_values(
    target_area: tuple[int, int, int, int]
) -> list[tuple[int, int]]:
    (min_x, max_x, min_y, max_y) = target_area

    initial_velocity_values: list[tuple[int, int]] = []

    # We can use some simple bounds to narrow the search space to:
    #
    #   1 <= x_0 <= max_x, assuming min_x > 0
    #
    # - Initial x velocity must be positive to get to a positive
    #   target area width.
    # - Initial x velocity can be no larger than the max target area
    #   width otherwise we overshoot in a single step.
    #
    #   min_y <= y_0 < abs(min_y), assuming min_y < 0
    #
    # - Initial y velocity cannot be lower than the target area floor
    #   otherwise we drop below it in a single step.
    # - Initial y velocity can be no larger than the absolute value of
    #   the target area floor as our y velocity when we cross the x
    #   will be (1 + y_0) so otherwise we would drop below it in the
    #   following step.
    for x_0 in range(1, max_x + 1):
        for y_0 in range(min_y, abs(min_y)):
            x, y = 0, 0
            dx, dy = x_0, y_0
            while x <= max_x and y >= min_y:
                if min_x <= x <= max_x and min_y <= y <= max_y:
                    initial_velocity_values.append((x_0, y_0))
                    break
                x += dx
                y += dy
                dx = 0 if dx == 0 else dx - 1
                dy -= 1

    return initial_velocity_values


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input17.txt")) as f:
        target_area = parse_input(f)

    print(
        max(
            max_trajectory_height(y_0)
            for _, y_0 in find_initial_velocity_values(target_area)
        )
    )
