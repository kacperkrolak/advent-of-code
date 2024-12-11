from solution_base import SolutionBase
from typing import TextIO

# 1. If stone is 0, it transforms into 1
# 2. If stone's digit count is even, it splits into two stones
# 3. Else it transforms into 2024 times the stone
def transform_stone(stone: int) -> list[int]:
        if stone == 0:
            return [1]
        
        str_stone = str(stone)
        length = len(str_stone)
        if length % 2 == 0:
            return [int(str_stone[:length // 2]), int(str_stone[length // 2:])]

        return [stone * 2024]

# Counter is a class which caches the count of the stone for each iteration
# It (kind of) recursively runs other counters, so that each counter is responsible only for:
# 1. Calculating next iteration
# 2. Caching the result for each iteration it's been asked for
class Counter:
    def __init__(self, value: int, counters: dict[int, "Counter"]):
        self.value: int = value
        self.next: list["Counter"] = []
        self.counters = counters
        self.count_per_iteration: dict[int, int] = {
            0: 1
        }
    
    # Get the stones this counter's stone will transform into.
    def set_next_references(self):
        next_values = transform_stone(self.value)
        for next_value in next_values:
            if next_value not in self.counters:
                self.counters[next_value] = Counter(next_value, self.counters)

            self.next.append(self.counters[next_value])

    # Get cached count for this iteration.
    # If not cached, ask child counters for their count.
    def get_count(self, iteration: int) -> int:
        if iteration in self.count_per_iteration:
            return self.count_per_iteration[iteration]
        
        if self.next == []:
            self.set_next_references()
        
        self.count_per_iteration[iteration] = sum([next_reference.get_count(iteration - 1) for next_reference in self.next])

        return self.count_per_iteration[iteration]

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.stones = list(map(int, file.readline().split()))
        self.counters: dict[int, Counter] = {}

    # Sum the number of stones each stone will split into.
    def get_count(self, iteration: int) -> int:
        count = 0
        for stone in self.stones:
            if stone not in self.counters:
                self.counters[stone] = Counter(stone, self.counters)
                
            count += self.counters[stone].get_count(iteration)
        return count

    def part_one(self):
        blinks = 6 if self.is_test else 25

        return f"Result for {blinks} blinks: {self.get_count(blinks)}"

    def part_two(self):
        blinks = 75
        
        return f"Result for {blinks} blinks: {self.get_count(blinks)}"