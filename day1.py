from collections import Counter
from solution_base import SolutionBase

class Solution(SolutionBase):
    def read_input(self, input_file):
        self.listOne = []
        self.listTwo = []

        with open(input_file, "r") as file:
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
