#!/usr/bin/env python3
import json
import os
from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class SnailfishNumber:
    left: Union["SnailfishNumber", int]
    right: Union["SnailfishNumber", int]
    parent: Optional["SnailfishNumber"] = None

    def __repr__(self) -> str:
        left_repr = (
            self.left.__repr__()
            if isinstance(self.left, SnailfishNumber)
            else str(self.left)
        )
        right_repr = (
            self.right.__repr__()
            if isinstance(self.right, SnailfishNumber)
            else str(self.right)
        )
        return f"[{left_repr},{right_repr}]"

    @staticmethod
    def parse(snailfish_number_list: list) -> "SnailfishNumber":
        left = (
            SnailfishNumber.parse(snailfish_number_list[0])
            if isinstance(snailfish_number_list[0], list)
            else snailfish_number_list[0]
        )
        right = (
            SnailfishNumber.parse(snailfish_number_list[1])
            if isinstance(snailfish_number_list[1], list)
            else snailfish_number_list[1]
        )

        snailfish_number = SnailfishNumber(left, right)

        if isinstance(left, SnailfishNumber):
            left.parent = snailfish_number
        if isinstance(right, SnailfishNumber):
            right.parent = snailfish_number

        return snailfish_number

    def depth(self) -> int:
        if self.parent is None:
            return 0
        return 1 + self.parent.depth()

    def magnitude(self) -> int:
        left_magnitude = (
            self.left.magnitude()
            if isinstance(self.left, SnailfishNumber)
            else self.left
        )
        right_magnitude = (
            self.right.magnitude()
            if isinstance(self.right, SnailfishNumber)
            else self.right
        )
        return 3 * left_magnitude + 2 * right_magnitude

    def clone(self) -> "SnailfishNumber":
        return SnailfishNumber.parse(self.to_list())

    def to_list(self) -> list:
        return [
            self.left.to_list()
            if isinstance(self.left, SnailfishNumber)
            else self.left,
            self.right.to_list()
            if isinstance(self.right, SnailfishNumber)
            else self.right,
        ]

    def add(self, other: "SnailfishNumber") -> "SnailfishNumber":
        left = self.clone()
        right = other.clone()
        added = SnailfishNumber(left=left, right=right)
        left.parent = added
        right.parent = added
        added.reduce()
        return added

    def reduce(self) -> bool:
        has_changed = False
        while True:
            has_exploded = self.explode()
            if has_exploded:
                has_changed = True
                continue

            has_split = self.split()
            if has_split:
                has_changed = True
                continue
            break
        return has_changed

    def explode(self) -> bool:
        # We should only ever be exploding a leaf node with two int values.
        if isinstance(self.left, SnailfishNumber) and self.left.explode():
            return True
        if isinstance(self.right, SnailfishNumber) and self.right.explode():
            return True

        if (
            self.parent is None
            or isinstance(self.left, SnailfishNumber)
            or isinstance(self.right, SnailfishNumber)
            or self.depth() < 4
        ):
            return False

        self.increment_nearest_left_number(self.left)
        self.increment_nearest_right_number(self.right)

        if self.parent.left is self:
            self.parent.replace_left(0)
        else:
            self.parent.replace_right(0)

        return True

    def split(self) -> bool:
        if isinstance(self.left, SnailfishNumber) and self.left.split():
            return True

        if isinstance(self.left, int) and self.left >= 10:
            new_left = SnailfishNumber(
                left=self.left // 2, right=(self.left + 1) // 2, parent=self
            )
            self.left = new_left
            return True

        if isinstance(self.right, SnailfishNumber) and self.right.split():
            return True

        if isinstance(self.right, int) and self.right >= 10:
            new_right = SnailfishNumber(
                left=self.right // 2, right=(self.right + 1) // 2, parent=self
            )
            self.right = new_right
            return True

        return False

    def increment_nearest_left_number(self, value: int) -> bool:
        current: SnailfishNumber | None = self
        while current is not None:
            tmp = current
            current = current.parent
            if current is not None and current.left is not tmp:
                # We found an ancestor with a different left tree which
                # will contain the nearest left number.
                break

        if current is None:
            return False

        # Either the nearest left number is the immediate left node
        # of the ancestor or it is the right most node in its tree.
        if isinstance(current.left, int):
            current.left += value
        else:
            current = current.left
            while isinstance(current.right, SnailfishNumber):
                current = current.right
            current.right += value

        return True

    def increment_nearest_right_number(self, value: int) -> bool:
        current: SnailfishNumber | None = self
        while current is not None:
            tmp = current
            current = current.parent
            if current is not None and current.right is not tmp:
                # We found an ancestor with a different right tree which
                # will contain the nearest right number.
                break

        if current is None:
            return False

        # Either the nearest right number is the immediate right node
        # of the ancestor or it is the left most node in its tree.
        if isinstance(current.right, int):
            current.right += value
        else:
            current = current.right
            while isinstance(current.left, SnailfishNumber):
                current = current.left
            current.left += value

        return True

    def replace_left(self, new_left: Union["SnailfishNumber", int]) -> None:
        if isinstance(self.left, SnailfishNumber):
            self.left.parent = None
        self.left = new_left

    def replace_right(self, new_right: Union["SnailfishNumber", int]) -> None:
        if isinstance(self.right, SnailfishNumber):
            self.right.parent = None
        self.right = new_right


def parse_input(f) -> list[SnailfishNumber]:
    return [SnailfishNumber.parse(json.loads(line)) for line in f]


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input18.txt")) as f:
        snailfish_numbers = parse_input(f)

    added = snailfish_numbers[0]
    for snailfish_number in snailfish_numbers[1:]:
        added = added.add(snailfish_number)
    print(added.magnitude())
