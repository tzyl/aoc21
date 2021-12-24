#!/usr/bin/env python3
import os


def parse_input(f) -> dict[str, set[str]]:
    adjacency_list: dict[str, set[str]] = {}

    for line in f:
        v1, v2 = line.strip().split("-")

        if adjacency_list.get(v1) is None:
            adjacency_list[v1] = set()
        if adjacency_list.get(v2) is None:
            adjacency_list[v2] = set()

        adjacency_list[v1].add(v2)
        adjacency_list[v2].add(v1)

    return adjacency_list


def find_all_paths_one_small_cave_at_most_twice(
    adjacency_list: dict[str, set[str]]
) -> list[list[str]]:
    """Find all paths from start to end that do not visit small caves more
    than once except a single small cave which is not start or end at most
    twice.

    Returns the list of paths as lists of caves."""
    all_paths = []
    to_visit: list[tuple[str, list[str], str | None]] = [("start", [], None)]
    while to_visit:
        node, current_path, small_cave_twice = to_visit.pop()
        current_path = [*current_path, node]

        if node == "end":
            all_paths.append(current_path)

        for neighbour in adjacency_list[node]:
            if is_big_cave(neighbour):
                to_visit.append((neighbour, current_path, small_cave_twice))
            elif neighbour not in current_path:
                to_visit.append((neighbour, current_path, small_cave_twice))
            elif (
                small_cave_twice is None and neighbour != "start" and neighbour != "end"
            ):
                to_visit.append((neighbour, current_path, neighbour))
    return all_paths


def is_big_cave(node: str) -> bool:
    return node.isupper()


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input12.txt")) as f:
        adjacency_list = parse_input(f)

    print(len(find_all_paths_one_small_cave_at_most_twice(adjacency_list)))
