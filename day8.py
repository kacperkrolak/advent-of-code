from solution_base import SolutionBase
from typing import TextIO
from vector import Vector
from itertools import combinations

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.antennas: dict[str, list[Vector]] = {}
        self.len_y = 0
        self.len_x = 0
        
        # The result will be stored there as hashes of vectors
        self.antinodes = set()
        
        for row, line in enumerate(file):
            self.len_y = row + 1
            self.len_x = len(line.strip())

            chars = line.strip()
            for col, char in enumerate(chars):
                if char != ".":
                    if char not in self.antennas:
                        self.antennas[char] = []
                    self.antennas[char].append(Vector(x=col, y=row))
    
    def vector_in_grid(self, vector: Vector) -> bool:
        return 0 <= vector.x < self.len_x and 0 <= vector.y < self.len_y
    
    def get_antinodes_part1(self, antenna_a: Vector, antenna_b: Vector) -> list[Vector]:
        diff = antenna_b.copy().subtract(antenna_a)

        result = []
        result.append(antenna_a.copy().subtract(diff))
        result.append(antenna_b.copy().add(diff))
        
        return [vector for vector in result if self.vector_in_grid(vector)]
    
    def get_antinodes_part2(self, antenna_a: Vector, antenna_b: Vector) -> list[Vector]:
        diff = antenna_b.copy().subtract(antenna_a)

        result = []

        # Direction one - from A to B
        cur = antenna_b.copy()
        while True:
            if not self.vector_in_grid(cur):
                break
            
            result.append(cur.copy())
            cur.add(diff)
            
        # Direction two - from B to A
        cur = antenna_a.copy()
        while True:
            if not self.vector_in_grid(cur):
                break
            
            result.append(cur.copy())
            cur.subtract(diff)
            
        return result
    
    def print_antinodes(self):
        for i in range(self.len_y):
            for j in range(self.len_x):
                if hash(Vector(j, i)) in self.antinodes:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def part_one(self):
        for type, antennas in self.antennas.items():
            for antenna_a, antenna_b in combinations(antennas, 2):
                self.antinodes.update([hash(antinode) for antinode in self.get_antinodes_part1(antenna_a, antenna_b)])

        self.print_antinodes()

        return len(self.antinodes)
                
    def part_two(self):
        for type, antennas in self.antennas.items():
            if len(antennas) == 1:
                self.antinodes.add(hash(antennas[0]))

            for antenna_a, antenna_b in combinations(antennas, 2):
                self.antinodes.update([hash(antinode) for antinode in self.get_antinodes_part2(antenna_a, antenna_b)])
                
        self.print_antinodes()

        return len(self.antinodes)
