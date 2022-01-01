#!/usr/bin/env python3
import os


def parse_input(f) -> list[tuple[list[set[str]], list[set[str]]]]:
    return [parse_line(line) for line in f]


def parse_line(line) -> tuple[list[set[str]], list[set[str]]]:
    left, right = line.strip().split(" | ")
    signal_patterns = [make_segment_set(pattern) for pattern in left.split(" ")]
    output_patterns = [make_segment_set(pattern) for pattern in right.split(" ")]
    return signal_patterns, output_patterns


def make_segment_set(pattern: str) -> set[str]:
    return set(c for c in pattern)


def is_unique_segment_set(segment_set: set[str]) -> bool:
    return (
        len(segment_set) == 2  # Unique segment count for 1
        or len(segment_set) == 4  # Unique segment count for 4
        or len(segment_set) == 3  # Unique segment count for 7
        or len(segment_set) == 7  # Unique segment count for 8
    )


def decode_patterns(signal_patterns: list[set[str]]) -> dict[str, str]:
    """Decode which segment corresponds to which wire based on the ten unique
    digit patterns.

         u
      ul   ur
         m
      dl   dr
         d

    Returns a mapping between the segment character and the wire position
    according to the labelling in the diagram above.
    """
    one_pattern = next(p for p in signal_patterns if len(p) == 2)
    four_pattern = next(p for p in signal_patterns if len(p) == 4)
    seven_pattern = next(p for p in signal_patterns if len(p) == 3)
    eight_pattern = next(p for p in signal_patterns if len(p) == 7)

    u = next(c for c in seven_pattern if c not in one_pattern)

    ur_or_dr = list(one_pattern)
    ul_or_m = list(four_pattern.difference(one_pattern))
    dl_or_d = list(eight_pattern.difference(seven_pattern).difference(four_pattern))

    two_three_five_patterns = [p for p in signal_patterns if len(p) == 5]
    two_pattern = next(
        p for p in two_three_five_patterns if all(c in p for c in dl_or_d)
    )
    three_pattern = next(
        p for p in two_three_five_patterns if all(c in p for c in ur_or_dr)
    )
    five_pattern = next(
        p for p in two_three_five_patterns if all(c in p for c in ul_or_m)
    )

    if ur_or_dr[0] in two_pattern:
        ur, dr = ur_or_dr[0], ur_or_dr[1]
    else:
        ur, dr = ur_or_dr[1], ur_or_dr[0]

    if ul_or_m[0] in five_pattern and ul_or_m[0] not in three_pattern:
        ul, m = ul_or_m[0], ul_or_m[1]
    else:
        ul, m = ul_or_m[1], ul_or_m[0]

    if dl_or_d[0] in two_pattern and dl_or_d[0] not in three_pattern:
        dl, d = dl_or_d[0], dl_or_d[1]
    else:
        dl, d = dl_or_d[1], dl_or_d[0]

    return {
        u: "u",
        ul: "ul",
        ur: "ur",
        m: "m",
        dl: "dl",
        dr: "dr",
        d: "d",
    }


def get_digit(decoded_pattern: frozenset[str]) -> int:
    """Gets the digit corresponding to the decoded pattern following the
    labelling in the diagram below.

         u
      ul   ur
         m
      dl   dr
         d

    Returns the digit between 0 and 9.
    """
    wire_mapping = {
        frozenset(["u", "ul", "ur", "dl", "dr", "d"]): 0,
        frozenset(["ur", "dr"]): 1,
        frozenset(["u", "ur", "m", "dl", "d"]): 2,
        frozenset(["u", "ur", "m", "dr", "d"]): 3,
        frozenset(["ul", "ur", "m", "dr"]): 4,
        frozenset(["u", "ul", "m", "dr", "d"]): 5,
        frozenset(["u", "ul", "m", "dl", "dr", "d"]): 6,
        frozenset(["u", "ur", "dr"]): 7,
        frozenset(["u", "ul", "ur", "m", "dl", "dr", "d"]): 8,
        frozenset(["u", "ul", "ur", "m", "dr", "d"]): 9,
    }
    return wire_mapping[decoded_pattern]


def decode_output_value(
    signal_patterns: list[set[str]], output_patterns: list[set[str]]
) -> int:
    segment_mapping = decode_patterns(signal_patterns)
    decoded_digits = [
        get_digit(frozenset(segment_mapping[c] for c in p)) for p in output_patterns
    ]
    return int("".join([str(digit) for digit in decoded_digits]))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input8.txt")) as f:
        entries = parse_input(f)

    print("Part One:")
    print(
        sum(
            is_unique_segment_set(pattern)
            for _, output_patterns in entries
            for pattern in output_patterns
        )
    )

    print("Part Two:")
    print(
        sum(
            decode_output_value(signal_patterns, output_patterns)
            for signal_patterns, output_patterns in entries
        )
    )
