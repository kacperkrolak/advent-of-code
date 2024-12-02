from collections import Counter
from solution_base import SolutionBase
from typing import TextIO

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.listOne = []
        self.listTwo = []

        for line in file:
            l, r = line.split()
            self.listOne.append(int(l))
            self.listTwo.append(int(r))

        self.listOne.sort()
        self.listTwo.sort()
        
    def part_one(self):
        distance = 0

        for i in range(len(self.listOne)):
            distance += abs(self.listOne[i] - self.listTwo[i])

        return distance

    def part_two(self):
        c = Counter(self.listTwo)
            
        similarity = 0
            
        for i in range(len(self.listOne)):
            similarity += c[self.listOne[i]] * self.listOne[i]

        return similarity
