from solution_base import SolutionBase
from typing import TextIO

def transform_stone(stone: int) -> list[int]:
        if stone == 0:
            return [1]
        
        str_stone = str(stone)
        length = len(str_stone)
        if length % 2 == 0:
            return [int(str_stone[:length // 2]), int(str_stone[length // 2:])]

        return [stone * 2024]

class Counter:
    def __init__(self, value: int, counters: dict[int, "Counter"]):
        self.value: int = value
        self.next: list["Reference"] = []
        self.counters = counters
        self.count_per_iteration: dict[int, int] = {
            0: 1
        }
        
    def set_next_references(self):
        next_values = transform_stone(self.value)
        for next_value in next_values:
            if next_value not in self.counters:
                self.counters[next_value] = Counter(next_value, self.counters)
            self.next.append(Reference(self.counters[next_value]))

    def get_count(self, iteration: int) -> int:
        if iteration in self.count_per_iteration:
            return self.count_per_iteration[iteration]
        
        if self.next == []:
            self.set_next_references()
        
        self.count_per_iteration[iteration] = sum([next_reference.counter.get_count(iteration - 1) for next_reference in self.next])

        return self.count_per_iteration[iteration]

class Reference:
    def __init__(self, counter: Counter):
        self.counter = counter

    def __repr__(self):
        return f"Reference({self.counter.count})"

# Cache implementation will work like this:
# 1. 
class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.stones = list(map(int, file.readline().split()))
        self.cache: dict[int, list[int]] = {}
        self.counters: dict[int, Counter] = {}
    
    def transform_all(self):
        new_stones = []
        
        for stone in self.stones:
            new_stones.extend(transform_stone(stone))

        self.stones = new_stones

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