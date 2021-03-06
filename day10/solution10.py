#!/usr/bin/env python3
import os

OPEN_CHUNK_CHARACTERS = set(["(", "[", "{", "<"])
CLOSE_CHUNK_CHARACTERS = set([")", "]", "}", ">"])
OPEN_CHUNK_TO_CLOSE_CHUNK = {
    # comment to force black to format multiline
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
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
AUTOCOMPLETE_CHARACTER_SCORES = {
    # comment to force black to format multiline
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
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


def find_completion_string(line: str) -> str | None:
    open_chunks: list[str] = []
    for c in line:
        if c in OPEN_CHUNK_CHARACTERS:
            open_chunks.append(c)
        elif c in CLOSE_CHUNK_CHARACTERS:
            open_chunk = open_chunks.pop() if open_chunks else None
            if CLOSE_CHUNK_TO_OPEN_CHUNK[c] != open_chunk:
                # Corrupt line cannot be completed
                return None
    return "".join(OPEN_CHUNK_TO_CLOSE_CHUNK[c] for c in open_chunks[::-1])


def score_completion_string(completion_string: str) -> int:
    score = 0
    for c in completion_string:
        score = 5 * score + AUTOCOMPLETE_CHARACTER_SCORES[c]
    return score


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input10.txt")) as f:
        lines = [line.strip() for line in f]

    print("Part One:")
    print(
        sum(
            ILLEGAL_CHARACTER_SCORES[c]
            for c in (find_first_illegal_character(line) for line in lines)
            if c is not None
        )
    )

    completion_string_scores = [
        score_completion_string(completion_string)
        for completion_string in (find_completion_string(line) for line in lines)
        if completion_string is not None
    ]
    print("Part Two:")
    print(sorted(completion_string_scores)[len(completion_string_scores) // 2])
