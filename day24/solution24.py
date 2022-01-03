#!/usr/bin/env python3
import os
from typing import Literal, Union

Variable = Literal["w", "x", "y", "z"]
InpInstruction = tuple[Literal["inp"], Variable]
AddInstruction = tuple[Literal["add"], Variable, Variable | int]
MulInstruction = tuple[Literal["mul"], Variable, Variable | int]
DivInstruction = tuple[Literal["div"], Variable, Variable | int]
ModInstruction = tuple[Literal["mod"], Variable, Variable | int]
EqlInstruction = tuple[Literal["eql"], Variable, Variable | int]
Instruction = Union[
    InpInstruction,
    AddInstruction,
    MulInstruction,
    DivInstruction,
    ModInstruction,
    EqlInstruction,
]


class ALU:
    w: int
    x: int
    y: int
    z: int

    def __init__(self, program: list[Instruction], input_stack: list[int]) -> None:
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.program = program
        self.input_stack = input_stack

    def run(self) -> tuple[int, int, int, int]:
        for instruction in self.program:
            self.run_instruction(instruction)
        return self.w, self.x, self.y, self.z

    def run_instruction(self, instruction: Instruction) -> None:
        if instruction[0] == "inp":
            self.run_inp_instruction(instruction)
        elif instruction[0] == "add":
            self.run_add_instruction(instruction)
        elif instruction[0] == "mul":
            self.run_mul_instruction(instruction)
        elif instruction[0] == "div":
            self.run_div_instruction(instruction)
        elif instruction[0] == "mod":
            self.run_mod_instruction(instruction)
        elif instruction[0] == "eql":
            self.run_eq_instruction(instruction)

    def run_inp_instruction(self, instruction: InpInstruction) -> None:
        variable = instruction[1]
        value = self.input_stack.pop()
        self.set_variable(variable, value)

    def run_add_instruction(self, instruction: AddInstruction) -> None:
        left = self.get_variable(instruction[1])
        right = self.get_variable_or_int(instruction[2])
        self.set_variable(instruction[1], left + right)

    def run_mul_instruction(self, instruction: MulInstruction) -> None:
        left = self.get_variable(instruction[1])
        right = self.get_variable_or_int(instruction[2])
        self.set_variable(instruction[1], left * right)

    def run_div_instruction(self, instruction: DivInstruction) -> None:
        left = self.get_variable(instruction[1])
        right = self.get_variable_or_int(instruction[2])
        if right == 0:
            raise ValueError("Invalid state for div")
        self.set_variable(instruction[1], int(left / right))

    def run_mod_instruction(self, instruction: ModInstruction) -> None:
        left = self.get_variable(instruction[1])
        right = self.get_variable_or_int(instruction[2])
        if left < 0 or right <= 0:
            raise ValueError("Invalid state for mod")
        self.set_variable(instruction[1], left % right)

    def run_eq_instruction(self, instruction: EqlInstruction) -> None:
        left = self.get_variable(instruction[1])
        right = self.get_variable_or_int(instruction[2])
        self.set_variable(instruction[1], 1 if left == right else 0)

    def get_variable_or_int(self, variable_or_int: Variable | int) -> int:
        if isinstance(variable_or_int, int):
            return variable_or_int
        return self.get_variable(variable_or_int)

    def get_variable(self, variable: Variable) -> int:
        if variable == "w":
            return self.w
        elif variable == "x":
            return self.x
        elif variable == "y":
            return self.y
        elif variable == "z":
            return self.z

    def set_variable(self, variable: Variable, value: int) -> None:
        if variable == "w":
            self.w = value
        elif variable == "x":
            self.x = value
        elif variable == "y":
            self.y = value
        elif variable == "z":
            self.z = value


def parse_instruction(line: str) -> Instruction:
    tokens = line.strip().split(" ")
    left = parse_variable(tokens[1])
    if tokens[0] == "inp":
        inp_instruction: InpInstruction = ("inp", left)
        return inp_instruction

    right = parse_variable_or_int(tokens[2])
    if tokens[0] == "add":
        add_instruction: AddInstruction = ("add", left, right)
        return add_instruction
    elif tokens[0] == "mul":
        mul_instruction: MulInstruction = ("mul", left, right)
        return mul_instruction
    elif tokens[0] == "div":
        div_instruction: DivInstruction = ("div", left, right)
        return div_instruction
    elif tokens[0] == "mod":
        mod_instruction: ModInstruction = ("mod", left, right)
        return mod_instruction
    elif tokens[0] == "eql":
        eql_instruction: EqlInstruction = ("eql", left, right)
        return eql_instruction
    raise ValueError(f"Unexpected token {tokens[0]} when parsing operation")


def parse_variable(token: str) -> Variable:
    if token == "w":
        return "w"
    elif token == "x":
        return "x"
    elif token == "y":
        return "y"
    elif token == "z":
        return "z"
    raise ValueError(f"Unexpected token {token} when parsing variable")


def parse_variable_or_int(token: str) -> Variable | int:
    try:
        return parse_variable(token)
    except ValueError:
        return int(token)


def is_model_number_valid(program: list[Instruction], model_number: int) -> bool:
    model_number_str = str(model_number)
    if len(model_number_str) != 14:
        raise ValueError("Model number must be 14 digits long")
    alu = ALU(program, [int(c) for c in model_number_str[::-1]])
    _, _, _, z = alu.run()
    return z == 0


def is_model_number_valid_formula(model_number: int) -> bool:
    """Formula version of calculating whether a model number is valid
    by inspecting the program."""
    w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 = [
        int(c) for c in str(model_number)
    ]
    # L1 w1
    z = w1 + 6
    # L19 w2
    z *= 26
    z += w2 + 12
    # L37 w3
    z *= 26
    z += w3 + 5
    # L55 w4
    z *= 26
    z += w4 + 10
    # L73 w5
    z = int(z / 26)
    if w5 != (w4 + 10) - 16:
        z *= 26
        z += w5 + 7
    # L91 w6
    z *= 26
    z += w6
    # L109 w7
    z *= 26
    z += w7 + 4
    # L127 w8
    z = int(z / 26)
    if w8 != (w7 + 4) - 4:
        z *= 26
        z += w8 + 12
    # L145 w9
    z *= 26
    z += w9 + 14
    # L163 w10
    z = int(z / 26)
    if w10 != (w9 + 14) - 7:
        z *= 26
        z += w10 + 13
    # L181 w11
    x = z % 26
    z = int(z / 26)
    if w11 != x - 8:
        z *= 26
        z += w11 + 10
    # L199 w12
    x = z % 26
    z = int(z / 26)
    if w12 != x - 4:
        z *= 26
        z += w12 + 11
    # L217 w13
    x = z % 26
    z = int(z / 26)
    if w13 != x - 15:
        z *= 26
        z += w13 + 9
    # L235 w14
    x = z % 26
    z = int(z / 26)
    if w14 != x - 8:
        z *= 26
        z += w14 + 9
    # In each input iteration we work in base 26 and either shift up
    # and add a new term or shift down.
    #
    # For z to be zero at the end:
    # - We cannot add a term in last iteration
    # - Must have shifted out all previous terms
    #
    # There are at least seven shifts up and at most seven shifts down
    # depending on the conditions between the digits. Therefore, to
    # shift out the very first term we must pass every condition so
    # that there are seven shifts up and seven shifts down in total.
    #
    # Therefore, the conditions must apply against the following pairs
    # of terms:
    # - w4/w5
    # - w7/w8
    # - w9/w10
    # - w6/w11
    # - w3/w12
    # - w2/w13
    # - w1/w14
    return z == 0


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input24.txt")) as f:
        program = [parse_instruction(line) for line in f]

    # Highest possible number:
    #
    # w5 = w4 - 6
    #  -> w4 = 9, w5 = 3
    w4 = 9
    w5 = 3
    # w8 = w7
    #  -> w7 = 9, w8 = 9
    w7 = 9
    w8 = 9
    # w10 = w9 + 7
    #  -> w9 = 2, w10 = 9
    w9 = 2
    w10 = 9
    # w11 = w6 - 8
    #  -> w6 = 9, w11 = 1
    w6 = 9
    w11 = 1
    # w12 = w3 + 1
    #  -> w3 = 8, w12 = 9
    w3 = 8
    w12 = 9
    # w13 = w2 - 3
    #  -> w2 = 9, w13 = 6
    w2 = 9
    w13 = 6
    # w14 = w1 - 2
    #  -> w1 = 9, w14 = 7
    w1 = 9
    w14 = 7

    highest_valid_number = int(
        "".join(
            str(c)
            for c in (w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14)
        )
    )
    if not is_model_number_valid(program, highest_valid_number):
        raise ValueError("Expected model number to be valid")
    elif not is_model_number_valid_formula(highest_valid_number):
        raise ValueError("Expected model number to be valid")

    print("Part One:")
    print(highest_valid_number)

    # Lowest possible number:
    #
    # w5 = w4 - 6
    #  -> w4 = 7, w5 = 1
    w4 = 7
    w5 = 1
    # w8 = w7
    #  -> w7 = 1, w8 = 1
    w7 = 1
    w8 = 1
    # w10 = w9 + 7
    #  -> w9 = 1, w10 = 8
    w9 = 1
    w10 = 8
    # w11 = w6 - 8
    #  -> w6 = 9, w11 = 1
    w6 = 9
    w11 = 1
    # w12 = w3 + 1
    #  -> w3 = 1, w12 = 2
    w3 = 1
    w12 = 2
    # w13 = w2 - 3
    #  -> w2 = 4, w13 = 1
    w2 = 4
    w13 = 1
    # w14 = w1 - 2
    #  -> w1 = 3, w14 = 1
    w1 = 3
    w14 = 1

    lowest_valid_number = int(
        "".join(
            str(c)
            for c in (w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14)
        )
    )
    if not is_model_number_valid(program, lowest_valid_number):
        raise ValueError("Expected model number to be valid")
    elif not is_model_number_valid_formula(lowest_valid_number):
        raise ValueError("Expected model number to be valid")

    print("Part Two:")
    print(lowest_valid_number)
