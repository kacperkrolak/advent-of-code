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
        cost = 0

        # How many bananas each sequence will give.
        sequence_score: dict[tuple[int, int, int, int], int] = {}

        # @TODO: Only add the val if the tuple appeared in given buyer the first time.
        for secret in self.secrets:
            lastFour = []
            seen: set[tuple[int, int, int, int]] = set()

            prev_val = secret % 10
            prev = secret
            for _ in range(2000):
                next = self.evolve_secret(prev)
                next_val = next % 10
                
                diff = next_val - prev_val
                
                prev = next
                prev_val = next_val

                lastFour.append(diff)
                if len(lastFour) < 4:
                    continue

                if len(lastFour) > 4:
                    lastFour.pop(0)
                
                if tuple(lastFour) in seen:
                    continue
                seen.add(tuple(lastFour))
                
                if not tuple(lastFour) in sequence_score:
                    sequence_score[tuple(lastFour)] = 0
                sequence_score[tuple(lastFour)] += next_val


            cost += prev

        return max(sequence_score.values())