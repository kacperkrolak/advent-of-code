from solution_base import SolutionBase
from typing import TextIO

# We will use Position to make the code more readable,
# but tuples make it easier to use in a set
class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        
    def get_neighbors(self) -> list["Position"]:
        return [
            Position(self.x + 1, self.y),
            Position(self.x - 1, self.y),
            Position(self.x, self.y + 1),
            Position(self.x, self.y - 1)
        ]
    
    def get_tuple(self) -> tuple[int,int]:
        return (self.x, self.y)

class TopographicalMap:
    def __init__(self, file: TextIO):
        self.map: list[list[int]] = []

        for line in file:
            self.map.append(list(map(int, line.strip())))

        self.size_x = len(self.map[0])
        self.size_y = len(self.map)
        
    def get_height(self, pos: Position) -> int:
        if pos.x < 0 or pos.x >= self.size_x or pos.y < 0 or pos.y >= self.size_y:
            return -1

        return self.map[pos.y][pos.x]

class TrailheadData:
    # score is the number of disctinct peaks reached
    # rating is the numbers of paths leading to a peak
    def __init__(self, score: int, rating: int):
        self.score = score
        self.rating = rating

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.map = TopographicalMap(file)
        self.trailheads: list[Position] = []
        self.find_trailheads()
        
    # Find all 0s in the map
    def find_trailheads(self):
        for y in range(self.map.size_y):
            for x in range(self.map.size_x):
                pos = Position(x, y)
                if self.map.get_height(pos) == 0:
                    self.trailheads.append(pos)

    def trailhead_score(self, trailhead: Position) -> TrailheadData:
        reached_peaks: set[tuple[int, int]] = set()
        finished_paths: int = 0
        queue: list[Position] = [trailhead]
        q_len = len(queue)
        
        while q_len > 0:
            for i in range(q_len):
                cur = queue[i]
                cur_height = self.map.get_height(cur)

                for neighbor in cur.get_neighbors():
                    neighbor_height = self.map.get_height(neighbor)
                    if not cur_height + 1 == neighbor_height:
                        continue
                    
                    tuple_neighbor = neighbor.get_tuple()

                    if neighbor_height == 9:
                        finished_paths += 1
                        reached_peaks.add(tuple_neighbor)
                        continue

                    queue.append(neighbor)
                                    
            queue = queue[q_len:]
            q_len = len(queue)

        return TrailheadData(len(reached_peaks), finished_paths)

    def part_one(self):
        return sum(self.trailhead_score(trailhead).score for trailhead in self.trailheads)
            
        

    def part_two(self):
        return sum(self.trailhead_score(trailhead).rating for trailhead in self.trailheads)
