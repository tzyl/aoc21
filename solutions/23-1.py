#!/usr/bin/env python3
import heapq
import math
import os
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Generator, Generic, Literal, TypeVar

Amphipod = Literal["A", "B", "C", "D"]
Room = tuple[Amphipod | None, Amphipod | None]
Hallway = tuple[
    Amphipod | None,
    Amphipod | None,
    Amphipod | None,
    Amphipod | None,
    Amphipod | None,
    Amphipod | None,
    Amphipod | None,
    Amphipod | None,
    Amphipod | None,
    Amphipod | None,
    Amphipod | None,
]
AMPHIPODS: list[Amphipod] = ["A", "B", "C", "D"]
ENERGY_COST: dict[Amphipod, int] = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

T = TypeVar("T")


@dataclass(order=True)
class PrioritizedItem(Generic[T]):
    priority: int
    item: T = field(compare=False)


@dataclass(frozen=True)
class AmphipodBurrow:
    room_a: Room
    room_b: Room
    room_c: Room
    room_d: Room
    hallway: Hallway

    _hallway_position_index = {
        "A": 2,
        "B": 4,
        "C": 6,
        "D": 8,
    }
    _invalid_hallway_positions = set([2, 4, 6, 8])

    def __repr__(self) -> str:
        lines = []
        lines.append("".join(self.print_amphipod(space) for space in self.hallway))
        lines.append(self.print_amphipod_room_line(1))
        lines.append(self.print_amphipod_room_line(0))
        return "\n".join(lines)

    def print_amphipod_room_line(self, index: int) -> str:
        return (
            f"  {self.print_amphipod(self.room_a[index])}"
            f" {self.print_amphipod(self.room_b[index])}"
            f" {self.print_amphipod(self.room_c[index])}"
            f" {self.print_amphipod(self.room_d[index])}  "
        )

    def print_amphipod(self, amphipod: Amphipod | None) -> str:
        return amphipod if amphipod is not None else "."

    def get_room(self, room_type: Amphipod) -> Room:
        if room_type == "A":
            return self.room_a
        elif room_type == "B":
            return self.room_b
        elif room_type == "C":
            return self.room_c
        elif room_type == "D":
            return self.room_d

    def get_possible_moves(self) -> Generator[tuple["AmphipodBurrow", int], None, None]:
        # Leaving room to hallway
        for room_type in AMPHIPODS:
            for move in self.get_possible_leave_room_moves(room_type):
                yield move

        # Entering room from hallway
        for i in range(len(self.hallway)):
            for move in self.get_possible_enter_room_moves(i):
                yield move

    def get_possible_leave_room_moves(
        self, room_type: Amphipod
    ) -> Generator[tuple["AmphipodBurrow", int], None, None]:
        room = self.get_room(room_type)
        amphipod: Amphipod
        steps_to_leave_room: int
        next_room: Room

        a0, a1 = room[0], room[1]
        if a0 is not None and a1 is not None:
            if all(a == room_type for a in (a0, a1)):
                return
            amphipod = a1
            steps_to_leave_room = 1
            next_room = (a0, None)
        elif a0 is not None and a1 is None:
            if all(a == room_type for a in (a0,)):
                return
            amphipod = a0
            steps_to_leave_room = 2
            next_room = (None, None)
        else:
            return

        outside_room_index = self._hallway_position_index[room_type]
        to_left_index = outside_room_index - 1
        while to_left_index >= 0 and self.hallway[to_left_index] is None:
            if to_left_index not in self._invalid_hallway_positions:
                next_hallway = get_next_hallway(self.hallway, to_left_index, amphipod)
                next_amphipod_burrow = AmphipodBurrow(
                    room_a=next_room if room_type == "A" else self.room_a,
                    room_b=next_room if room_type == "B" else self.room_b,
                    room_c=next_room if room_type == "C" else self.room_c,
                    room_d=next_room if room_type == "D" else self.room_d,
                    hallway=next_hallway,
                )
                energy_cost = ENERGY_COST[amphipod] * (
                    steps_to_leave_room + abs(to_left_index - outside_room_index)
                )
                yield next_amphipod_burrow, energy_cost
            to_left_index -= 1

        to_right_index = outside_room_index + 1
        while (
            to_right_index < len(self.hallway) and self.hallway[to_right_index] is None
        ):
            if to_right_index not in self._invalid_hallway_positions:
                next_hallway = get_next_hallway(self.hallway, to_right_index, amphipod)
                next_amphipod_burrow = AmphipodBurrow(
                    room_a=next_room if room_type == "A" else self.room_a,
                    room_b=next_room if room_type == "B" else self.room_b,
                    room_c=next_room if room_type == "C" else self.room_c,
                    room_d=next_room if room_type == "D" else self.room_d,
                    hallway=next_hallway,
                )
                energy_cost = ENERGY_COST[amphipod] * (
                    steps_to_leave_room + abs(to_right_index - outside_room_index)
                )
                yield next_amphipod_burrow, energy_cost
            to_right_index += 1

    def get_possible_enter_room_moves(
        self, hallway_index: int
    ) -> Generator[tuple["AmphipodBurrow", int], None, None]:
        amphipod = self.hallway[hallway_index]
        if amphipod is None:
            return

        room = self.get_room(amphipod)
        steps_to_enter_room: int
        next_room: Room

        a0, a1 = room[0], room[1]
        if a0 is None and a1 is None:
            steps_to_enter_room = 2
            next_room = (amphipod, None)
        elif a0 is not None and a1 is None:
            if any(a != amphipod for a in (a0,)):
                return
            steps_to_enter_room = 1
            next_room = (a0, amphipod)
        else:
            return

        outside_room_index = self._hallway_position_index[amphipod]
        a, b = (
            (hallway_index + 1, outside_room_index)
            if hallway_index <= outside_room_index
            else (outside_room_index, hallway_index - 1)
        )
        if any(space is not None for space in self.hallway[a : b + 1]):
            return

        next_hallway = get_next_hallway(self.hallway, hallway_index, None)
        next_amphipod_burrow = AmphipodBurrow(
            room_a=next_room if amphipod == "A" else self.room_a,
            room_b=next_room if amphipod == "B" else self.room_b,
            room_c=next_room if amphipod == "C" else self.room_c,
            room_d=next_room if amphipod == "D" else self.room_d,
            hallway=next_hallway,
        )
        energy_cost = ENERGY_COST[amphipod] * (
            abs(hallway_index - outside_room_index) + steps_to_enter_room
        )
        yield next_amphipod_burrow, energy_cost


def get_next_hallway(hallway: Hallway, index: int, value: Amphipod | None) -> Hallway:
    next_hallway_list = list(hallway)
    next_hallway_list[index] = value
    next_hallway: Hallway = (
        next_hallway_list[0],
        next_hallway_list[1],
        next_hallway_list[2],
        next_hallway_list[3],
        next_hallway_list[4],
        next_hallway_list[5],
        next_hallway_list[6],
        next_hallway_list[7],
        next_hallway_list[8],
        next_hallway_list[9],
        next_hallway_list[10],
    )
    return next_hallway


def parse_input(
    f,
) -> AmphipodBurrow:
    lines = [line for line in f]
    return AmphipodBurrow(
        room_a=(lines[3][3], lines[2][3]),
        room_b=(lines[3][5], lines[2][5]),
        room_c=(lines[3][7], lines[2][7]),
        room_d=(lines[3][9], lines[2][9]),
        hallway=(None,) * 11,
    )


def find_least_energy_to_organize(initial_amphipod_burrow: AmphipodBurrow) -> int:
    visited: set[AmphipodBurrow] = set()
    distances: dict[AmphipodBurrow, float] = defaultdict(lambda: math.inf)
    priority_queue: list[PrioritizedItem[AmphipodBurrow]] = []

    distances[initial_amphipod_burrow] = 0
    heapq.heappush(priority_queue, PrioritizedItem(0, initial_amphipod_burrow))

    while priority_queue:
        item = heapq.heappop(priority_queue)
        current_energy_cost, current_amphipod_burrow = item.priority, item.item
        visited.add(current_amphipod_burrow)

        for (
            next_amphipod_burrow,
            energy_cost,
        ) in current_amphipod_burrow.get_possible_moves():
            if next_amphipod_burrow not in visited:
                candidate_energy_cost = current_energy_cost + energy_cost
                if candidate_energy_cost < distances[next_amphipod_burrow]:
                    distances[next_amphipod_burrow] = candidate_energy_cost
                    heapq.heappush(
                        priority_queue,
                        PrioritizedItem(candidate_energy_cost, next_amphipod_burrow),
                    )

    completed_amphipod_burrow = AmphipodBurrow(
        room_a=("A", "A"),
        room_b=("B", "B"),
        room_c=("C", "C"),
        room_d=("D", "D"),
        hallway=(None,) * 11,
    )

    return int(distances[completed_amphipod_burrow])


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input23.txt")) as f:
        initial_amphipod_burrow = parse_input(f)

    print(find_least_energy_to_organize(initial_amphipod_burrow))
