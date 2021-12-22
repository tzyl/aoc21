#!/usr/bin/env python3
import os

Board = list[list[int]]
BoardMarks = list[list[int]]


def parse_boards(f) -> tuple[list[int], list[Board], list[BoardMarks]]:
    numbers = [int(x) for x in f.readline().strip().split(",")]

    boards = []
    boards_marks = []

    rest = f.readlines()
    for i in range(len(rest) // 6):
        board_lines = rest[(6 * i + 1) : (6 * i + 6)]
        board = [[int(x) for x in line.strip().split()] for line in board_lines]
        board_marks = [([0] * 5) for _ in range(5)]

        boards.append(board)
        boards_marks.append(board_marks)

    return numbers, boards, boards_marks


def find_last_winning_board_score(
    boards: list[Board],
    boards_marks: list[BoardMarks],
    numbers: list[int],
) -> int:
    winning_scores = []
    boards_won = [False] * len(boards)

    for number in numbers:
        for i in range(len(boards)):
            board = boards[i]
            board_marks = boards_marks[i]
            board_won = boards_won[i]

            if board_won:
                continue

            mark_board(board, board_marks, number)
            if has_board_won(board_marks):
                boards_won[i] = True
                winning_scores.append(
                    calculate_winning_score(board, board_marks, number)
                )

    return winning_scores[-1]


def mark_board(board: Board, board_marks: BoardMarks, number: int) -> None:
    for i in range(5):
        for j in range(5):
            if board[i][j] == number:
                board_marks[i][j] = 1


def has_board_won(board_marks: BoardMarks) -> bool:
    for i in range(5):
        row = board_marks[i]
        if all(row):
            return True
    for j in range(5):
        column = [board_marks[i][j] for i in range(5)]
        if all(column):
            return True
    return False


def calculate_winning_score(
    board: Board, board_marks: BoardMarks, winning_number: int
) -> int:
    score = 0
    for i in range(5):
        for j in range(5):
            if not board_marks[i][j]:
                score += board[i][j]
    return score * winning_number


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input4.txt")) as f:
        numbers, boards, boards_marks = parse_boards(f)

    print(find_last_winning_board_score(boards, boards_marks, numbers))
