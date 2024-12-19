from solution_base import SolutionBase
from typing import TextIO

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        # Patterns grouped by the first character
        self.available_patterns: dict[str, list[str]] = {}
        self.target_patterns: list[str] = []
        self.memo: dict[str, int] = {}
        
        for pattern in file.readline().split(','):
            pattern = pattern.strip()
            
            if pattern[0] not in self.available_patterns:
                self.available_patterns[pattern[0]] = []

            self.available_patterns[pattern[0]].append(pattern)
        
        file.readline() # Skip empty line

        line = file.readline().strip()
        while line:
            self.target_patterns.append(line)
            line = file.readline().strip()
    
    def is_pattern_possible(self, pattern: str) -> bool:
        if pattern == "":
            return True
        
        if pattern[0] not in self.available_patterns:
            return False
        
        for p in self.available_patterns[pattern[0]]:
            if not pattern.startswith(p):
                continue
            
            if self.is_pattern_possible(pattern[len(p):]):
                return True
        return False
    
    def possible_ways_to_build_pattern(self, pattern: str) -> int:
        if pattern == "":
            return 1
        
        if pattern in self.memo:
            return self.memo[pattern]
        
        if pattern[0] not in self.available_patterns:
            return 0
        
        ways = 0
        for p in self.available_patterns[pattern[0]]:
            if not pattern.startswith(p):
                continue
            
            ways += self.possible_ways_to_build_pattern(pattern[len(p):])

        self.memo[pattern] = ways
        return ways
    
    def part_one(self):
        possible_count = 0

        for pattern in self.target_patterns:
            if self.is_pattern_possible(pattern):
                possible_count += 1

        return possible_count

    def part_two(self):
        count = 0

        for pattern in self.target_patterns:
            count += self.possible_ways_to_build_pattern(pattern)

        return count
