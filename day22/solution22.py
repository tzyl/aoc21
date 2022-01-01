#!/usr/bin/env python3
import os
import re
from dataclasses import dataclass
from typing import Literal

INPUT_REGEX_PATTERN = re.compile(
    r"(?P<on_or_off>on|off) "
    r"x=(?P<min_x>-?\d+)\.\.(?P<max_x>-?\d+),"
    r"y=(?P<min_y>-?\d+)..(?P<max_y>-?\d+),"
    r"z=(?P<min_z>-?\d+)..(?P<max_z>-?\d+)"
)


@dataclass(frozen=True)
class Cuboid:
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int

    def volume(self) -> int:
        return (
            (self.x2 + 1 - self.x1) * (self.y2 + 1 - self.y1) * (self.z2 + 1 - self.z1)
        )

    def intersects(self, other: "Cuboid") -> bool:
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
            and self.z1 <= other.z2
            and self.z2 >= other.z1
        )

    def contains(self, other: "Cuboid") -> bool:
        return (
            self.x1 <= other.x1
            and self.x2 >= other.x2
            and self.y1 <= other.y1
            and self.y2 >= other.y2
            and self.z1 <= other.z1
            and self.z2 >= other.z2
        )

    def remove(self, other: "Cuboid") -> list["Cuboid"]:
        if not self.intersects(other):
            return [self]
        elif other.contains(self):
            return []
        # Trim down to just the interesecting cuboid
        intersecting = Cuboid(
            x1=max(other.x1, self.x1),
            x2=min(other.x2, self.x2),
            y1=max(other.y1, self.y1),
            y2=min(other.y2, self.y2),
            z1=max(other.z1, self.z1),
            z2=min(other.z2, self.z2),
        )
        # Split into up to 6 smaller non-overlapping cuboids
        split = []
        if intersecting.x1 > self.x1:
            # Left face cuboid
            split.append(
                Cuboid(
                    x1=self.x1,
                    x2=intersecting.x1 - 1,
                    y1=self.y1,
                    y2=self.y2,
                    z1=self.z1,
                    z2=self.z2,
                )
            )
        if intersecting.x2 < self.x2:
            # Right face cuboid
            split.append(
                Cuboid(
                    x1=intersecting.x2 + 1,
                    x2=self.x2,
                    y1=self.y1,
                    y2=self.y2,
                    z1=self.z1,
                    z2=self.z2,
                )
            )
        if intersecting.y1 > self.y1:
            # Forward face cuboid
            split.append(
                Cuboid(
                    x1=intersecting.x1,
                    x2=intersecting.x2,
                    y1=self.y1,
                    y2=intersecting.y1 - 1,
                    z1=self.z1,
                    z2=self.z2,
                )
            )
        if intersecting.y2 < self.y2:
            # Back face cuboid
            split.append(
                Cuboid(
                    x1=intersecting.x1,
                    x2=intersecting.x2,
                    y1=intersecting.y2 + 1,
                    y2=self.y2,
                    z1=self.z1,
                    z2=self.z2,
                )
            )
        if intersecting.z1 > self.z1:
            # Bottom face cuboid
            split.append(
                Cuboid(
                    x1=intersecting.x1,
                    x2=intersecting.x2,
                    y1=intersecting.y1,
                    y2=intersecting.y2,
                    z1=self.z1,
                    z2=intersecting.z1 - 1,
                )
            )
        if intersecting.z2 < self.z2:
            # Back face cuboid
            split.append(
                Cuboid(
                    x1=intersecting.x1,
                    x2=intersecting.x2,
                    y1=intersecting.y1,
                    y2=intersecting.y2,
                    z1=intersecting.z2 + 1,
                    z2=self.z2,
                )
            )

        return split


RebootStep = tuple[Literal["on", "off"], Cuboid]


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
            Cuboid(
                x1=int(m.group("min_x")),
                x2=int(m.group("max_x")),
                y1=int(m.group("min_y")),
                y2=int(m.group("max_y")),
                z1=int(m.group("min_z")),
                z2=int(m.group("max_z")),
            ),
        )
        reboot_steps.append(reboot_step)
    return reboot_steps


def count_cubes_on_restricted(reboot_steps: list[RebootStep]) -> int:
    grid = [[[0] * 101 for _ in range(101)] for _ in range(101)]
    for on_or_off, cuboid in reboot_steps:
        min_x, max_x, min_y, max_y, min_z, max_z = (
            cuboid.x1,
            cuboid.x2,
            cuboid.y1,
            cuboid.y2,
            cuboid.z1,
            cuboid.z2,
        )
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


def count_cubes_on_full(reboot_steps: list[RebootStep]) -> int:
    cuboids: set[Cuboid] = set()
    for on_or_off, cuboid in reboot_steps:
        new_cuboids: set[Cuboid] = set()
        # If we are turning off a cuboid we remove the cuboid from
        # all the existing cuboids.
        # If we are turning on a cuboid we treat it as first turning
        # it off and then turning it on so that we guarantee to only
        # have non-overlapping cuboids.
        if on_or_off == "on":
            new_cuboids.add(cuboid)
        for existing_cuboid in cuboids:
            new_cuboids.update(existing_cuboid.remove(cuboid))
        cuboids = new_cuboids
    return sum(cuboid.volume() for cuboid in cuboids)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input22.txt")) as f:
        reboot_steps = parse_input(f)

    print("Part One:")
    print(count_cubes_on_restricted(reboot_steps))

    print("Part Two:")
    print(count_cubes_on_full(reboot_steps))
