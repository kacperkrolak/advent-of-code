from solution_base import SolutionBase
from typing import TextIO
import json

class Solution(SolutionBase):
    def parse_register_value(self, line: str) -> int:
        return int(line.split(":")[1])

    def read_input(self, file: TextIO):
        self.pointer: int = 0

        self.a_start: int = self.parse_register_value(file.readline())
        self.b_start: int = self.parse_register_value(file.readline())
        self.c_start: int = self.parse_register_value(file.readline())
        
        file.readline() # empty line
        
        self.instructions: list[int] = list(map(int, file.readline().split(':')[1].split(",")))
        self.output: list[int] = []
        
    def reset(self):
        self.a = self.a_start
        self.b = self.b_start
        self.c = self.c_start
        self.pointer = 0
        self.output = []
    
    def resolve_combo(self, combo: int) -> int:
        match combo:
            case combo if combo <= 3:
                return combo
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                raise ValueError(f"Invalid combo value: {combo}")
            
    def adv(self, combo: int):
        denominator = 2 ** self.resolve_combo(combo)
        self.a = self.a // denominator
        
    def bxl(self, literal: int):
        self.b = self.b ^ literal
        
    def bst(self, combo: int):
        self.b = self.resolve_combo(combo) % 8
        
    def jnz(self, combo: int):
        if self.a == 0:
            return
        
        self.pointer = self.resolve_combo(combo) - 2
        
    def bxc(self, _: int):
        self.b = self.b ^ self.c
        
    def out(self, combo: int):
        self.output.append(self.resolve_combo(combo) % 8)
    
    def bdv(self, combo: int):
        denominator = 2 ** self.resolve_combo(combo)
        self.b = self.a // denominator
        
    def cdv(self, combo: int):
        denominator = 2 ** self.resolve_combo(combo)
        self.c = self.a // denominator

    # Returns:
    # 0: continue
    # 1: halt
    # 2: error - out is not correct
    def handle_instruction(self) -> int:
        if self.pointer >= len(self.instructions):
            return 1
        
        opcode = self.instructions[self.pointer]
        operand = self.instructions[self.pointer + 1]
        
        match opcode:
            case 0:
                self.adv(operand)
            case 1:
                self.bxl(operand)
            case 2:
                self.bst(operand)
            case 3:
                self.jnz(operand)
            case 4:
                self.bxc(operand)
            case 5:
                self.out(operand)
                instruction = self.instructions[len(self.output) - 1] if len(self.instructions) >= len(self.output) else None
                if self.output[-1] != instruction:
                    self.pointer += 2
                    return 2
            case 6:
                self.bdv(operand)
            case 7:
                self.cdv(operand)
            case _:
                raise ValueError(f"Invalid opcode: {opcode}")
        
        self.pointer += 2
        return 0

    def part_one(self):
        self.reset()
        while True:
            status = self.handle_instruction()
            if status == 1:
                break
        
        return ",".join(map(str, self.output))

    def possible_bin_values(self, bin_prefix: str) -> tuple[int, int]:
        min = bin_prefix + "000"
        max = bin_prefix + "111"
        return int(min, 2), int(max, 2)
    
    def create_lookup_table(self) -> dict[int, dict[int, str]]:
        # Key is number 0-7, value is dictionary of 11-bit numbers and their string representation.
        results: dict[int, dict[int, str]] = {}
        for i in range(2**11):
            self.a_start = i
            self.reset()

            while True:
                status = self.handle_instruction()
                if status != 0:
                    break

            result = self.output[0]
            if result not in results:
                results[result] = {}

            results[result][i] = bin(i)[2:].zfill(11)
        return results

    # The program from part two always does instructions one by one, and at the end,
    # it jumps to the very beginning. It only halts when A register reaches 0.
    # When we analyze the operations (see input/17.txt for details), we can see that:
    # 1. Register A is divided by 8 in every iteration,
    # 2. The length of the program is 16, so the output will be in range from 8^15 to 8^16-1.
    # 3. The iterations don't share any state - each iteration uses A with 3 last bits removed.
    # 4. One iteration uses at most 11 bits of A, so there are 2^11 different cases.
    #
    # Therefore, we can solve this problem using this method:
    # 1. Create a map of 11-bit binary numbers and their corresponding 3-bit binary numbers.
    # 2. Reverse the program (the beginning of register A creates the last instruction)
    # 3. Find all possible register A values that will create the program.
    # 4. Choose the smallest register A.
    def part_two(self):
        # For testing, input is small and brute force is fast enough.
        if self.is_test:
            while True:
                self.reset()

                while True:
                    status = self.handle_instruction()
                    if status == 1 and len(self.output) == len(self.instructions):
                        return self.a_start
                    if status > 0:
                        break

                self.a_start += 1
        
        
        lookup_table = self.create_lookup_table()
        self.instructions.reverse()

        # We need smallest number, that's why we start with 0.
        a = "00000000"

        paths = [a]

        for i in self.instructions:
            allowed_values = lookup_table[i]
            
            new_paths = []
            for path in paths:
                last_8_bits = path[-8:]
                min_val, max_val = self.possible_bin_values(last_8_bits)

                for num, bin_str in allowed_values.items():
                    if int(num) >= min_val and int(num) <= max_val:
                        new_paths.append(path + bin_str[-3:])
                
            paths = new_paths

        nums = []
        for path in paths:
            nums.append(int(path, 2))

        return min(nums)

        
