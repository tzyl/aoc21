#!/usr/bin/env python3
import os
from collections import Counter


def parse_input(f) -> tuple[str, dict[str, str]]:
    polymer_template = f.readline().strip()
    f.readline()
    pair_insertion_rules = {
        k: v for (k, v) in (line.strip().split(" -> ") for line in f)
    }
    return polymer_template, pair_insertion_rules


def insert_pairs(
    polymer_template: str, pair_insertion_rules: dict[str, str], steps: int
) -> str:
    result = polymer_template
    for _ in range(steps):
        result = insert_pairs_once(result, pair_insertion_rules)
    return result


def insert_pairs_once(
    polymer_template: str, pair_insertion_rules: dict[str, str]
) -> str:
    next_polymer = []
    for a, b in zip(polymer_template, polymer_template[1:]):
        next_polymer.append(a)
        pair = a + b
        if pair in pair_insertion_rules:
            next_polymer.append(pair_insertion_rules[pair])
    next_polymer.append(polymer_template[-1])
    return "".join(next_polymer)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input14.txt")) as f:
        polymer_template, pair_insertion_rules = parse_input(f)

    polymer = insert_pairs(polymer_template, pair_insertion_rules, 10)
    letters_by_count = Counter(polymer).most_common()
    print(letters_by_count[0][1] - letters_by_count[-1][1])
