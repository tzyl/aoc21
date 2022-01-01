#!/usr/bin/env python3
import os
from dataclasses import dataclass, field
from math import prod


@dataclass(frozen=True)
class Packet:
    version: int
    type_id: int
    value: int | None = None
    subpackets: list["Packet"] = field(default_factory=list)


def parse_input(f) -> str:
    return hex_to_binary(f.readline().strip())


def hex_to_binary(hex: str) -> str:
    return bin(int(hex, 16))[2:].zfill(len(hex * 4))


def parse_packet(bit_string: str, start: int) -> tuple[Packet, int]:
    version = int(bit_string[start : start + 3], 2)
    type_id = int(bit_string[start + 3 : start + 6], 2)

    if type_id == 4:
        return parse_literal_packet(bit_string, start, version, type_id)
    else:
        return parse_operator_packet(bit_string, start, version, type_id)


def parse_literal_packet(
    bit_string: str, start: int, version: int, type_id: int
) -> tuple[Packet, int]:
    bits_consumed = 6  # Header already consumed
    value_start = start + 6
    value_bits = []
    i = 0
    while True:
        group_start = value_start + 5 * i
        is_last_group = bit_string[group_start] == "0"
        value_bits.append(bit_string[group_start + 1 : group_start + 5])
        bits_consumed += 5
        i += 1
        if is_last_group:
            break

    value = int("".join(value_bits), 2)
    literal_packet = Packet(version=version, type_id=type_id, value=value)

    return literal_packet, bits_consumed


def parse_operator_packet(
    bit_string: str, start: int, version: int, type_id: int
) -> tuple[Packet, int]:
    bits_consumed = 6  # Header already consumed

    subpackets = []
    length_type_id = int(bit_string[start + 6], 2)
    bits_consumed += 1

    if not length_type_id:
        subpackets_bits_length = int(bit_string[start + 7 : start + 22], 2)
        bits_consumed += 15
        subpackets_bits_consumed = 0
        while subpackets_bits_consumed < subpackets_bits_length:
            subpacket_start = start + 22 + subpackets_bits_consumed
            subpacket, subpacket_bits_consumed = parse_packet(
                bit_string, subpacket_start
            )
            subpackets.append(subpacket)
            subpackets_bits_consumed += subpacket_bits_consumed
    else:
        subpackets_length = int(bit_string[start + 7 : start + 18], 2)
        bits_consumed += 11
        subpackets_bits_consumed = 0
        for i in range(subpackets_length):
            subpacket_start = start + 18 + subpackets_bits_consumed
            subpacket, subpacket_bits_consumed = parse_packet(
                bit_string, subpacket_start
            )
            subpackets.append(subpacket)
            subpackets_bits_consumed += subpacket_bits_consumed

    bits_consumed += subpackets_bits_consumed

    operator_packet = Packet(version=version, type_id=type_id, subpackets=subpackets)

    return operator_packet, bits_consumed


def evaluate_packet_value(packet: Packet) -> int:
    type_id, value, subpackets = packet.type_id, packet.value, packet.subpackets
    if type_id == 4:
        if value is None:
            raise ValueError("Literal packet should have value")
        return value
    elif type_id == 0:
        return sum(evaluate_packet_value(p) for p in subpackets)
    elif type_id == 1:
        return prod(evaluate_packet_value(p) for p in subpackets)
    elif type_id == 2:
        return min(evaluate_packet_value(p) for p in subpackets)
    elif type_id == 3:
        return max(evaluate_packet_value(p) for p in subpackets)
    elif type_id == 5:
        value1, value2 = [evaluate_packet_value(p) for p in subpackets]
        return 1 if value1 > value2 else 0
    elif type_id == 6:
        value1, value2 = [evaluate_packet_value(p) for p in subpackets]
        return 1 if value1 < value2 else 0
    elif type_id == 7:
        value1, value2 = [evaluate_packet_value(p) for p in subpackets]
        return 1 if value1 == value2 else 0
    raise ValueError("Unrecognized type_id")


def sum_packet_version(packet: Packet) -> int:
    packet_version_sum = packet.version
    for subpacket in packet.subpackets:
        packet_version_sum += sum_packet_version(subpacket)
    return packet_version_sum


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input16.txt")) as f:
        bit_string = parse_input(f)

    packet, _ = parse_packet(bit_string, 0)
    print("Part One:")
    print(sum_packet_version(packet))

    print("Part Two:")
    print(evaluate_packet_value(packet))
