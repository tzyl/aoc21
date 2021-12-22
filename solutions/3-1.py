#!/usr/bin/env python3
import os


def find_gamma_and_epsilon_rate(binary_numbers: list[list[int]]) -> tuple[int, int]:
    one_counts = [0] * 12

    for binary_number in binary_numbers:
        for i in range(12):
            one_counts[i] += binary_number[i]

    gamma_rate_bits = [0] * 12
    epsilon_rate_bits = [0] * 12

    for i in range(12):
        count = one_counts[i]
        if count > len(binary_numbers) / 2:
            gamma_rate_bits[i] = 1
        else:
            epsilon_rate_bits[i] = 1

    gamma_rate = bit_array_to_decimal(gamma_rate_bits)
    epsilon_rate = bit_array_to_decimal(epsilon_rate_bits)
    return gamma_rate, epsilon_rate


def bit_array_to_decimal(bit_array: list[int]) -> int:
    return int("".join([str(x) for x in bit_array]), 2)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input3.txt")) as f:
        binary_numbers = [[int(c) for c in line.strip()] for line in f]
    gamma_rate, epsilon_rate = find_gamma_and_epsilon_rate(binary_numbers)
    print(gamma_rate * epsilon_rate)
