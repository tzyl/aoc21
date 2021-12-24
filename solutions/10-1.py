#!/usr/bin/env python3
import os

OPEN_CHUNK_CHARACTERS = set(["(", "[", "{", "<"])
CLOSE_CHUNK_CHARACTERS = set([")", "]", "}", ">"])
CLOSE_CHUNK_TO_OPEN_CHUNK = {
    # comment to force black to format multiline
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}
ILLEGAL_CHARACTER_SCORES = {
    # comment to force black to format multiline
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def find_first_illegal_character(line: str) -> str | None:
    open_chunks: list[str] = []
    for c in line:
        if c in OPEN_CHUNK_CHARACTERS:
            open_chunks.append(c)
        elif c in CLOSE_CHUNK_CHARACTERS:
            open_chunk = open_chunks.pop() if open_chunks else None
            if CLOSE_CHUNK_TO_OPEN_CHUNK[c] != open_chunk:
                return c
    return None


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input10.txt")) as f:
        lines = [line.strip() for line in f]

    print(
        sum(
            ILLEGAL_CHARACTER_SCORES[c]
            for c in (find_first_illegal_character(line) for line in lines)
            if c is not None
        )
    )
