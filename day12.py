from solution_base import SolutionBase
from typing import TextIO

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

# We will use a dictionary to represent a map, because we will use a lot of empty tiles,
# which will be represented as None.
class Map:
    def __init__(self):
        self.tiles: dict[tuple[int, int], str] = {}
    
    @staticmethod
    def from_matrix(map: list[str]):
        m = Map()
        for y in range(len(map)):
            for x in range(len(map[y])):
                if map[y][x] != " ":
                    m.tiles[(x, y)] = map[y][x]

        return m
    
    def add_between(self, x1: int, y1: int, x2: int, y2: int, char: str):
        self.tiles[((x1 + x2) // 2, (y1 + y2) // 2)] = char
    
    def get_char(self, x: int, y: int) -> None | str:
        return self.tiles.get((x, y), None)

class RegionData:
    def __init__(self, char: str, perimeter: int, area: int, sides: int):
        self.char = char
        self.perimeter = perimeter
        self.area = area
        self.sides = sides

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        map: list[str] = []
        
        for line in file:
            map.append(line.strip())
            
        self.map = Map.from_matrix(map)
        self.visited: set[tuple[int, int]] = set()
    
    def get_fence_pos(self, x: int, y: int, direction: tuple[int, int]) -> tuple[int, int, bool]:
        horizontal = direction == UP or direction == DOWN
        x_offset = 1 if direction == RIGHT else 0
        y_offset = 1 if direction == DOWN else 0
        
        return (x + x_offset, y + y_offset, horizontal)
    
    def discover_edge(self, map: Map, x: int, y: int, visited: set[tuple[int, int]]) -> None:
        char = map.get_char(x, y)
        if char is None:
            raise ValueError(f"Invalid position: {x}, {y}")
        
        is_vertical = x % 2 == 1
        
        queue = [(x, y)]
        q_len = len(queue)
        
        while q_len > 0:
            for i in range(q_len):
                x, y = queue[i]
                
                neighbors = [(x, y-2), (x, y+2)] if is_vertical else [(x-2, y), (x+2, y)]
                for nx, ny in neighbors:
                    if map.get_char(nx, ny) != char:
                        continue
                    
                    if (nx, ny) in visited:
                        continue

                    # If a tile has edges on all 4 sides, then the sides are not connected. For example map:
                    # .-----.
                    # |X.X.X|
                    # |. - .|
                    # |X|0|X|
                    # |. - -.
                    # |X.X|0|
                    # .--- -.
                    # has zeroes which edges are next to each other, but they are not the same edge.
                    # One is one the inside, and the other is on the outside.
                    center = (nx + x) // 2, (ny + y) // 2
                    center_neighbors = [(center[0] - 1, center[1]), (center[0] + 1, center[1])] if is_vertical else [(center[0], center[1] - 1), (center[0], center[1] + 1)]
                    if map.get_char(center_neighbors[0][0], center_neighbors[0][1]) is not None or map.get_char(center_neighbors[1][0], center_neighbors[1][1]) is not None:
                        continue
                    
                    visited.add((nx, ny))
                    queue.append((nx, ny))
            
            queue = queue[q_len:]
            q_len = len(queue)
            
    def discover_region(self, x: int, y: int) -> RegionData:
        char = self.map.get_char(x, y)
        if char is None:
            raise ValueError(f"Invalid position: {x}, {y}")
        
        queue = [(x, y)]
        q_len = len(queue)

        perimeter = 0
        area = 0
        sides = 0
        edge_map = Map()
        
        while q_len > 0:
            for i in range(q_len):
                x, y = queue[i]
                
                for direction in [LEFT, RIGHT, UP, DOWN]:
                    dx, dy = direction
                    nx, ny = x + dx, y + dy
                    
                    if self.map.get_char(nx, ny) != char:
                        perimeter += 1
                        edge_map.add_between(x*2, y*2, nx*2, ny*2, char)

                        continue
                    
                    if (nx, ny) in self.visited:
                        continue
                    
                    self.visited.add((nx, ny))
                    queue.append((nx, ny))
                
                area += 1
            
            queue = queue[q_len:]
            q_len = len(queue)
            
        visited_edges: set[tuple[int, int]] = set()
        for pos, char in edge_map.tiles.items():
            if pos in visited_edges:
                continue

            visited_edges.add(pos)
            self.discover_edge(edge_map, pos[0], pos[1], visited_edges)
            sides += 1

        return RegionData(char, perimeter, area, sides)
            
    def part_one(self):
        cost = 0

        for pos in self.map.tiles:
            if pos in self.visited:
                continue
            
            self.visited.add(pos)
            region = self.discover_region(pos[0], pos[1])
            
            cost += region.perimeter * region.area
        
        return cost

    # We will represent the edges as tiles on the map, so map:
    # 12
    # 34
    # will be represented as:
    # 1e2
    # eee
    # 3e4
    # where e is the edge tile.
    # Then we can treat edges as regions and apply the same algorithm for finding them.
    def part_two(self):
        cost = 0

        for pos in self.map.tiles:
            if pos in self.visited:
                continue
            
            self.visited.add(pos)
            region = self.discover_region(pos[0], pos[1])
            cost += region.sides * region.area

        return cost
