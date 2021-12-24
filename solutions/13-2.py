#!/usr/bin/env python3
import os
from typing import Literal


def parse_input(f) -> tuple[list[list[int]], list[tuple[Literal["x", "y"], int]]]:
    dots = set()
    for line in f:
        if not line.strip():
            break
        x, y = (int(c) for c in line.strip().split(","))
        dots.add((x, y))

    m = max([dot[0] for dot in dots]) + 1
    n = max([dot[1] for dot in dots]) + 1

    dots_matrix: list[list[int]] = [[0] * n for _ in range(m)]
    for x, y in dots:
        dots_matrix[x][y] = 1

    fold_instructions: list[tuple[Literal["x", "y"], int]] = []
    for line in f:
        fold_line_split = line.strip().split("=")
        fold_direction, fold_position = fold_line_split[0], int(fold_line_split[1])
        if fold_direction == "fold along x":
            fold_instructions.append(("x", fold_position))
        elif fold_direction == "fold along y":
            fold_instructions.append(("y", fold_position))

    return dots_matrix, fold_instructions


def fold(
    dots_matrix: list[list[int]], fold_instruction: tuple[Literal["x", "y"], int]
) -> list[list[int]]:
    original_m = len(dots_matrix)
    original_n = len(dots_matrix[0])
    fold_direction, fold_position = fold_instruction

    m, n = (
        (fold_position, original_n)
        if fold_direction == "x"
        else (original_m, fold_position)
    )

    folded = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if (
                dots_matrix[i][j]
                or (
                    fold_direction == "x"
                    and 2 * fold_position - i < original_m
                    and dots_matrix[2 * fold_position - i][j]
                )
                or (
                    fold_direction == "y"
                    and 2 * fold_position - j < original_n
                    and dots_matrix[i][2 * fold_position - j]
                )
            ):
                folded[i][j] = 1

    return folded


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    m = len(matrix)
    n = len(matrix[0])
    transposed = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            transposed[i][j] = matrix[j][i]
    return transposed


def pretty_print_result(matrix: list[list[int]]) -> None:
    for row in matrix:
        print("".join("X" if dot else " " for dot in row))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input13.txt")) as f:
        dots_matrix, fold_instructions = parse_input(f)

    folded = dots_matrix
    for fold_instruction in fold_instructions:
        folded = fold(folded, fold_instruction)

    pretty_print_result(transpose(folded))
