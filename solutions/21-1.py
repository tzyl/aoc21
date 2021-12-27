#!/usr/bin/env python3
import os
from typing import Callable


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


def move_player_position(player_position: int, amount: int) -> int:
    return ((player_position - 1 + amount) % 10) + 1


class DeterministicDice:
    def __init__(self) -> None:
        self.value = 0

    def roll(self) -> int:
        value = self.value + 1
        self.value = (self.value + 1) % 100
        return value


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input21.txt")) as f:
        player1_start, player2_start = parse_input(f)

    deterministic_dice = DeterministicDice()
    player1_score, player2_score, number_of_rolls = play_dirac_dice(
        player1_start, player2_start, deterministic_dice.roll
    )
    print(min(player1_score, player2_score) * number_of_rolls)
