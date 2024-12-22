from solution_base import SolutionBase
from typing import TextIO

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.secrets = []

        for line in file:
            self.secrets.append(int(line))
    
    def evolve_secret(self, secret: int):
        mult = secret << 6 # Multiply by 64
        mixed = mult ^ secret
        pruned = mixed % 16777216

        divided = pruned >> 5 # Divide by 32
        mixed2 = divided ^ mixed
        pruned2 = mixed2 % 16777216 # Prune to 24 bits
        
        mult2 = pruned2 << 11 # Multiply by 2048
        mixed3 = mult2 ^ pruned2
        pruned3 = mixed3 % 16777216
        
        return pruned3
    
        
    def part_one(self):
        cost = 0

        for secret in self.secrets:
            evolved = secret
            for _ in range(2000):
                evolved = self.evolve_secret(evolved)

            cost += evolved
        
        return cost

    def part_two(self):
        return 0