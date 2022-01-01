#!/usr/bin/env python3
import os
from functools import cache
from typing import Callable

THREE_ROLLS_OUTCOMES = {
    3: 1,  # 1-1-1
    4: 3,  # 1-1-2
    5: 6,  # 1-1-3, 1-2-2
    6: 7,  # 1-2-3, 2-2-2
    7: 6,  # 1-3-3, 2-2-3
    8: 3,  # 2-3-3
    9: 1,  # 3-3-3
}


def parse_input(f) -> tuple[int, int]:
    player1_start = int(f.readline().strip()[-1])
    player2_start = int(f.readline().strip()[-1])
    return player1_start, player2_start


def play_dirac_dice(
    player1_start: int, player2_start: int, roll: Callable[[], int]
) -> tuple[int, int, int]:
    player1_position = player1_start
    player2_position = player2_start
    player1_score = 0
    player2_score = 0
    round = 0

    while player1_score < 1000 and player2_score < 1000:
        amount = roll() + roll() + roll()
        if round % 2 == 0:
            player1_position = move_player_position(player1_position, amount)
            player1_score += player1_position
        else:
            player2_position = move_player_position(player2_position, amount)
            player2_score += player2_position
        round += 1

    return player1_score, player2_score, 3 * round


class DeterministicDice:
    def __init__(self) -> None:
        self.value = 0

    def roll(self) -> int:
        value = self.value + 1
        self.value = (self.value + 1) % 100
        return value


@cache
def calculate_number_of_wins(
    player1_start: int,
    player1_score: int,
    player2_start: int,
    player2_score: int,
) -> tuple[int, int]:
    if player1_score >= 21:
        return (1, 0)
    if player2_score >= 21:
        return (0, 1)

    wins = [0, 0]
    for amount, copies in THREE_ROLLS_OUTCOMES.items():
        # Swap roles of player 1 and player 2 so that player 1 is
        # always playing the round.
        new_player1_start = player2_start
        new_player1_score = player2_score
        new_player2_start = move_player_position(player1_start, amount)
        new_player2_score = player1_score + new_player2_start

        next_step_wins = calculate_number_of_wins(
            new_player1_start,
            new_player1_score,
            new_player2_start,
            new_player2_score,
        )
        wins[0] += copies * next_step_wins[1]
        wins[1] += copies * next_step_wins[0]

    return (wins[0], wins[1])


def move_player_position(player_position: int, amount: int) -> int:
    return ((player_position - 1 + amount) % 10) + 1


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input21.txt")) as f:
        player1_start, player2_start = parse_input(f)

    deterministic_dice = DeterministicDice()
    player1_score, player2_score, number_of_rolls = play_dirac_dice(
        player1_start, player2_start, deterministic_dice.roll
    )

    print("Part One:")
    print(min(player1_score, player2_score) * number_of_rolls)

    player1_wins, player2_wins = calculate_number_of_wins(
        player1_start, 0, player2_start, 0
    )

    print("Part Two:")
    print(max(player1_wins, player2_wins))
