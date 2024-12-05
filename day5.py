from solution_base import SolutionBase
from typing import TextIO

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.rules: dict[int, set[int]] = {}
        self.instructions: list[list[int]] = []
        self.last_err_indexes = (0,0)

        line = file.readline()
        while line.strip() != "":                
            x, y = map(int, line.split("|"))
            if x not in self.rules:
                self.rules[x] = set()
            self.rules[x].add(y)
            
            line = file.readline()
        
        line = file.readline()
        while line:
            self.instructions.append(list(map(int, line.split(","))))
            line = file.readline()

    def is_instruction_valid(self, instruction: list[int]) -> bool:
        previous: set[int] = set()

        for i in range(len(instruction)):
            if instruction[i] not in self.rules:
                previous.add(instruction[i])
                continue
            
            intersection = previous & self.rules[instruction[i]]
            if len(intersection) > 0:
                self.last_err_indexes = (instruction.index(intersection.pop()), i)
                return False
            
            previous.add(instruction[i])

        return True

    def part_one(self):
        total = 0
        
        for instruction in self.instructions:
            if self.is_instruction_valid(instruction):
                total += instruction[len(instruction) // 2]
                
        return total

    def part_two(self):
        total = 0
        
        for instruction in self.instructions:
            # We only need to count invalid instructions.
            if self.is_instruction_valid(instruction):
                continue
            
            while True:
                buffer = instruction[self.last_err_indexes[0]]
                instruction[self.last_err_indexes[0]] = instruction[self.last_err_indexes[1]]
                instruction[self.last_err_indexes[1]] = buffer
                
                # To do this loop until the instruction is valid.
                if self.is_instruction_valid(instruction):
                    break

            total += instruction[len(instruction) // 2]
                
        return total
