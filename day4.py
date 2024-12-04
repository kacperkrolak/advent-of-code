from solution_base import SolutionBase
from typing import TextIO

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.lines = []
        for line in file:
            self.lines.append(line.strip())
            
    # Returns "" if the coordinates are out of bounds
    def get_char(self, x: int, y: int) -> str:
        if x < 0 or x >= len(self.lines[0]) or y < 0 or y >= len(self.lines):
            return ""
        
        return self.lines[y][x]
    
    def count_xmas_around(self, x: int, y: int) -> int:
        count = 0
        
        search = "MAS"
        coords = [
            # Horizontal
            [(x+1,y), (x+2,y), (x+3,y)],
            [(x-1,y), (x-2,y), (x-3,y)],
            # Vertical
            [(x,y+1), (x,y+2), (x,y+3)],
            [(x,y-1), (x,y-2), (x,y-3)],
            # Diagonal
            [(x+1,y+1), (x+2,y+2), (x+3,y+3)],
            [(x-1,y-1), (x-2,y-2), (x-3,y-3)],
            # Anti-diagonal
            [(x+1,y-1), (x+2,y-2), (x+3,y-3)],
            [(x-1,y+1), (x-2,y+2), (x-3,y+3)],
        ]
        
        for coord in coords:
            found = True
            for i, (x, y) in enumerate(coord):
                if self.get_char(x, y) != search[i]:
                    found = False
                    break
                
            if found:
                count += 1
                
        return count
    
    def is_cross_mass(self, x: int, y: int) -> bool:
        # Check that each diagonal has "S" and "M" in the corners.
        if not self.get_char(x-1, y-1) == "M" and not self.get_char(x+1, y+1) == "M":
            return False
        if not self.get_char(x-1, y-1) == "S" and not self.get_char(x+1, y+1) == "S":
            return False
        if not self.get_char(x+1, y-1) == "M" and not self.get_char(x-1, y+1) == "M":
            return False
        if not self.get_char(x+1, y-1) == "S" and not self.get_char(x-1, y+1) == "S":
            return False

        return True

    def part_one(self):
        total = 0

        # Iterate over all characters in the grid,
        # if it's X, then look for XMAS around it.
        for y in range(len(self.lines)):
            for x in range(len(self.lines[y])):
                if self.get_char(x, y) == "X":
                    total += self.count_xmas_around(x, y)
                    
        return total

    def part_two(self):
        total = 0

        # Iterate over all characters in the grid,
        # if it's A, then check if it's part of a cross MAS.
        for y in range(len(self.lines)):
            for x in range(len(self.lines[y])):
                if self.get_char(x, y) == "A" and self.is_cross_mass(x, y):
                    total += 1
                    
        return total
