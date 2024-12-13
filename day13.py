import sympy as sp
from sympy.solvers import solve
from sympy.abc import x, y

from solution_base import SolutionBase
from typing import TextIO
from vector import Vector

class Machine:
    def __init__(self, button_a: Vector, button_b: Vector, prize: Vector):
        self.button_a = button_a
        self.button_b = button_b
        self.prize = prize

class Solution(SolutionBase):
    # Example line: Button A: X+94, Y+34
    def parse_button_line(self, line: str) -> Vector:
        # Extract the x and y coordinates from the line
        x, y = line.split("X+")[1].split(", Y+")
        return Vector(int(x), int(y))
    
    # Example line: Prize: X=8400, Y=5400
    def parse_prize_line(self, line: str) -> Vector:
        x, y = line.split("X=")[1].split(", Y=")
        return Vector(int(x), int(y))
    
    def read_input(self, file: TextIO):
        self.machines = []

        while True:
            button_a_line = file.readline()
            if button_a_line == "":
                break
            
            button_a = self.parse_button_line(button_a_line)
            button_b = self.parse_button_line(file.readline())
            prize = self.parse_prize_line(file.readline())
            self.machines.append(Machine(button_a, button_b, prize))
            
            # Empty line
            file.readline()
            
    def part_one(self):
        tokens = 0

        # X is the number of times the button A is pressed
        # Y is the number of times the button B is pressed
        for machine in self.machines:
            eq1 = sp.Eq(machine.prize.x, machine.button_a.x * x + machine.button_b.x * y)
            eq2 = sp.Eq(machine.prize.y, machine.button_a.y * x + machine.button_b.y * y)
            output = solve([eq1, eq2], dict=True)
            # if x or y type is not sympy.core.numbers.Integer, continue
            if not isinstance(output[0][x], sp.core.numbers.Integer) or not isinstance(output[0][y], sp.core.numbers.Integer):
                continue

            tokens += output[0][x] * 3 + output[0][y] * 1

        return tokens

    def part_two(self):
        tokens = 0

        # X is the number of times the button A is pressed
        # Y is the number of times the button B is pressed
        for machine in self.machines:
            # Correct prize position.
            prize = machine.prize.add(Vector(10000000000000, 10000000000000))

            # Do the equation.
            eq1 = sp.Eq(machine.prize.x, machine.button_a.x * x + machine.button_b.x * y)
            eq2 = sp.Eq(machine.prize.y, machine.button_a.y * x + machine.button_b.y * y)
            output = solve([eq1, eq2], dict=True)
            # if x or y type is not sympy.core.numbers.Integer, continue
            if not isinstance(output[0][x], sp.core.numbers.Integer) or not isinstance(output[0][y], sp.core.numbers.Integer):
                continue

            tokens += output[0][x] * 3 + output[0][y] * 1

        return tokens
