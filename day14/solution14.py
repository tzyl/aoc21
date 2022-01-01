#!/usr/bin/env python3
import os
from collections import Counter, defaultdict


def parse_input(f) -> tuple[str, dict[str, str]]:
    polymer_template = f.readline().strip()
    f.readline()
    pair_insertion_rules = {
        k: v for (k, v) in (line.strip().split(" -> ") for line in f)
    }
    return polymer_template, pair_insertion_rules


def count_letters_in_polymer(
    polymer_template: str, pair_insertion_rules: dict[str, str], steps: int
) -> dict[str, int]:
    pair_counts: dict[str, int] = defaultdict(int)
    for a, b in zip(polymer_template, polymer_template[1:]):
        pair_counts[a + b] += 1

    for _ in range(steps):
        pair_counts = calculate_next_step_pair_counts(pair_counts, pair_insertion_rules)

    letter_counts: dict[str, int] = defaultdict(int)
    for pair, count in pair_counts.items():
        letter_counts[pair[0]] += count
        letter_counts[pair[1]] += count
    # The first and last letter are the only letters in the polymer template
    # which only appear in one pair in the final polymer.
    letter_counts[polymer_template[0]] += 1
    letter_counts[polymer_template[-1]] += 1
    # As each (adjusted) letter is counted in two pairs the number of times it
    # appears in the final polymer is exactly half of this.
    for letter in letter_counts:
        letter_counts[letter] //= 2

    return letter_counts


def calculate_next_step_pair_counts(
    pair_counts: dict[str, int], pair_insertion_rules: dict[str, str]
) -> dict[str, int]:
    next_pair_counts: dict[str, int] = defaultdict(int)
    for pair, count in pair_counts.items():
        if pair not in pair_insertion_rules:
            next_pair_counts[pair] += count
            continue
        inserted = pair_insertion_rules[pair]
        next_pair_counts[pair[0] + inserted] += count
        next_pair_counts[inserted + pair[1]] += count
    return next_pair_counts


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input14.txt")) as f:
        polymer_template, pair_insertion_rules = parse_input(f)

    polymer_letter_counts = count_letters_in_polymer(
        polymer_template, pair_insertion_rules, 10
    )
    letters_by_count = Counter(polymer_letter_counts).most_common()
    print("Part One:")
    print(letters_by_count[0][1] - letters_by_count[-1][1])

    polymer_letter_counts = count_letters_in_polymer(
        polymer_template, pair_insertion_rules, 40
    )
    letters_by_count = Counter(polymer_letter_counts).most_common()
    print("Part Two:")
    print(letters_by_count[0][1] - letters_by_count[-1][1])
