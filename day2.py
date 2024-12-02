from collections import Counter
from solution_base import SolutionBase
from typing import TextIO

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.levels = []
        for line in file:
            self.levels.append(list(map(int, line.split())))
        
    def is_level_safe(self, level: list[int]) -> bool:
        if len(level) == 1:
            return True
        
        increasing = level[0] < level[1]
            
        for i in range(1, len(level)):
            diff = abs(level[i] - level[i - 1])
            if diff < 1 or diff > 3:
                return False
            
            if increasing and level[i] < level[i - 1]:
                return False
            elif not increasing and level[i] > level[i - 1]:
                return False
            
        return True

    def part_one(self):
        safe_count = 0

        for level in self.levels:            
            if self.is_level_safe(level):
                safe_count += 1

        return safe_count

    def part_two(self):
        safe_count = 0

        for level in self.levels:            
            for i in range(len(level)):
                level_copy = level.copy()
                level_copy.pop(i)
                if self.is_level_safe(level_copy):
                    safe_count += 1
                    break

        return safe_count
