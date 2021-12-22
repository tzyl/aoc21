#!/usr/bin/env python3
import os


def find_oxygen_generator_rating(binary_numbers: list[list[int]]) -> int:
    return find_rating(binary_numbers, True)


def find_co2_scrubber_rating(binary_numbers: list[list[int]]) -> int:
    return find_rating(binary_numbers, False)


def find_rating(binary_numbers: list[list[int]], most_common: bool):
    candidates = binary_numbers
    for i in range(12):
        if len(candidates) == 1:
            break

        bit_sum = sum(x[i] for x in candidates)
        has_more_or_equal_one_bits = bit_sum >= (len(candidates) + 1) // 2

        if most_common:
            dominant_bit = 1 if has_more_or_equal_one_bits else 0
        else:
            dominant_bit = 0 if has_more_or_equal_one_bits else 1

        candidates = [x for x in candidates if x[i] == dominant_bit]

    if len(candidates) != 1:
        raise ValueError("Expected exactly one candidate left")

    return bit_array_to_decimal(candidates[0])


def bit_array_to_decimal(bit_array: list[int]) -> int:
    return int("".join([str(x) for x in bit_array]), 2)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input3.txt")) as f:
        binary_numbers = [[int(c) for c in line.strip()] for line in f]

    oxygen_generator_rating = find_oxygen_generator_rating(binary_numbers)
    co2_scrubber_rating = find_co2_scrubber_rating(binary_numbers)
    life_support_rating = oxygen_generator_rating * co2_scrubber_rating

    print(life_support_rating)
