from solution_base import SolutionBase
from typing import TextIO
from vector import Vector

class Map:
    def __init__(self):
        self.map: list[list[str]] = []
    
    def get_char(self, position: Vector) -> str:
        if position.y < 0 or position.y >= len(self.map) or position.x < 0 or position.x >= len(self.map[position.y]):
            return "#"

        return self.map[position.y][position.x]
    
    def set_char(self, position: Vector, char: str):
        self.map[position.y][position.x] = char
        
    @staticmethod
    def create(x: int, y: int, default: str) -> "Map":
        map = Map()
        map.map = [[default for _ in range(x)] for _ in range(y)]
        return map

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.map_size = int(file.readline())
        self.map = Map.create(self.map_size, self.map_size, ".")
        
        self.bytes_limit = int(file.readline())
        
        self.bytes: list[Vector] = []
        
        line = file.readline()
        while line != "":
            numbs = line.strip().split(",")
            self.bytes.append(Vector(int(numbs[0]), int(numbs[1])))
            line = file.readline()
    
    # Returns shortest distance to end, or -1 if no path is found
    def bfs(self, end: Vector) -> tuple[int, set[Vector]]:
        queue: list[Vector] = []
        visited: dict[Vector, None | Vector] = {}  # Maps position to its parent
        
        start = Vector(0, 0)
        queue.append(start)
        visited[start] = None
        
        q_len = 1
        distance = 0
        
        while queue:
            for i in range(q_len):
                cur = queue[i]
                if cur.equals(end):
                    # Reconstruct path
                    path_set: set[Vector] = set()
                    cur_node: None | Vector = cur
                    while cur_node is not None:
                        path_set.add(cur_node)
                        cur_node = visited[cur_node]
                    return distance, path_set
                
                for neighbor in cur.get_neighbors():
                    if self.map.get_char(neighbor) == "." and neighbor not in visited:
                        queue.append(neighbor)
                        visited[neighbor] = cur

            queue = queue[q_len:]
            q_len = len(queue)
            distance += 1
            
        return -1, set()

    def part_one(self):
        for i in range(self.bytes_limit):
            self.map.set_char(self.bytes[i], "#")

        distance, _ = self.bfs(Vector(self.map_size - 1, self.map_size - 1))

        return distance

    def part_two(self):
        # First find the path to the end
        distance, path_set = self.bfs(Vector(self.map_size - 1, self.map_size - 1))
        if distance == -1:
            return "No path found"

        # Only check bytes that intersect with our path
        for byte in self.bytes:
            self.map.set_char(byte, "#")
            if byte in path_set:
                distance, path_set = self.bfs(Vector(self.map_size - 1, self.map_size - 1))
                if distance == -1:
                    return f"{byte.x},{byte.y}"
        
        raise Exception("Unreachable")
