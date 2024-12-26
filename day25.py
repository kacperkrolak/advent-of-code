from solution_base import SolutionBase
from typing import TextIO, List

# Used to represent both keys and locks.
PinHeights = List[int]

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.keys: list[PinHeights] = []
        self.locks: list[PinHeights] = []
        
        while self.read_schematic(file):
            pass
    
    # Returns False if the end of the file is reached.
    def read_schematic(self, file: TextIO) -> bool:
        is_key = True
        line = file.readline().strip()
        
        if line == "":
            return False
        
        if "#" in line:
            is_key = False # Lock
        
        pin_heights: PinHeights = [-1, -1, -1, -1, -1]
        while line.strip() != "":
            for i, c in enumerate(line):
                if c == "#":
                    pin_heights[i] += 1
            line = file.readline().strip()
        if is_key:
            self.keys.append(pin_heights)
        else:
            self.locks.append(pin_heights)
        
        return True
                    
    def key_fits(self, key: PinHeights, lock: PinHeights) -> bool:
        for i in range(5):
            if key[i] + lock[i] > 5:
                return False
        return True
    
    def part_one(self):
        count = 0
        for key in self.keys:
            for lock in self.locks:
                print(key, lock)
                if self.key_fits(key, lock):
                    count += 1
        return count

    def part_two(self):
        return 0