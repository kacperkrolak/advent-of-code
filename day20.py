from solution_base import SolutionBase
from typing import TextIO
from vector import Vector

class Map:
    def __init__(self):
        self.map: list[list[str]] = []
    
    def get_char(self, position: Vector) -> str | None:
        if position.y < 0 or position.y >= len(self.map) or position.x < 0 or position.x >= len(self.map[position.y]):
            return None

        return self.map[position.y][position.x]

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.map = Map()
        self.end = Vector(0, 0)
        self.start = Vector(0, 0)
        
        row = 0
        for line in file:
            l = line.strip()
            end_index = l.find("E")
            if end_index != -1:
                self.end = Vector(end_index, row)
                l = l[:end_index] + '.' + l[end_index + 1:]
            
            start_index = l.find("S")
            if start_index != -1:
                self.start = Vector(start_index, row)
                l = l[:start_index] + '.' + l[start_index + 1:]
            
            self.map.map.append(list(l))
            row += 1

    # Check the distance from the end to each tile.
    # Return the set with path and the distance to each tile.
    def bfs(self, start: Vector, end: Vector) -> tuple[set[Vector], dict[Vector, int]]:
        queue: list[Vector] = [end]
        previous: dict[Vector, None | Vector] = {
            end: None
        }
        distance: dict[Vector, int] = {}
        visited: set[Vector] = set([end])
        
        q_len = len(queue)
        
        dist = 0
        while q_len > 0:
            for i in range(q_len):
                vec = queue[i]
                distance[vec] = dist
                
                for neighbor in vec.get_neighbors():
                    if self.map.get_char(neighbor) == "." and neighbor not in visited:
                        queue.append(neighbor)
                        if neighbor in previous:
                            raise Exception("Neighbor already in previous")
                        previous[neighbor] = vec
                        visited.add(neighbor)
            queue = queue[q_len:]
            q_len = len(queue)
            dist += 1

        path: set[Vector] = set()
        cur: Vector | None = start

        while cur is not None:
            path.add(cur)
            cur = previous[cur]
                
        return path, distance

    # If tile next to us is a wall, and the tile behind the wall is empty,
    # then it's a cheat path.
    #
    # Return positions we land on after using the cheat paths.
    def get_cheat_paths(self, position: Vector) -> list[Vector]:
        tiles: list[Vector] = []

        UP = Vector(0, -1)
        DOWN = Vector(0, 1)
        LEFT = Vector(-1, 0)
        RIGHT = Vector(1, 0)

        for direction in [UP, DOWN, LEFT, RIGHT]:
            neighbor = position.copy().add(direction)
            neighbor_behind = neighbor.copy().add(direction)
            
            if self.map.get_char(neighbor) == "#" and self.map.get_char(neighbor_behind) == ".":
                tiles.append(neighbor_behind)

        return tiles
    
    def get_cheats_paths_part_two(self, position: Vector) -> list[tuple[Vector, int]]:
        tiles: list[tuple[Vector, int]] = []
        
        for y in range(-20, 21):
            distance_left = 20 - abs(y)
            for x in range(-distance_left, distance_left + 1):
                tile = Vector(position.x + x, position.y + y)
                if self.map.get_char(tile) == ".":
                    distance = abs(x) + abs(y)
                    tiles.append((tile, distance))
        
        return tiles

    def part_one(self) -> str:
        path, distance = self.bfs(self.start, self.end)
        
        # Seconds saved -> Occurences
        cheats: dict[int, int] = {}
        
        for vec in path:
            tiles = self.get_cheat_paths(vec)
            distance_to_end = distance[vec] - 2 # Cheat path needs to have distance lower than that.
            for tile in tiles:
                cheat_distance = distance[tile]
                saved_seconds = distance_to_end - cheat_distance
                if saved_seconds > 0:
                    cheats[saved_seconds] = cheats.get(saved_seconds, 0) + 1

        if self.is_test:
            return str(sorted(cheats.items()))
        
        count = 0
        for seconds, occurences in sorted(cheats.items()):
            if seconds >= 100:
                count += occurences

        return str(count)

    def part_two(self):
        path, distance = self.bfs(self.start, self.end)
        
        # Seconds saved -> Occurences
        cheats: dict[int, int] = {}

        for vec in path:
            tiles = self.get_cheats_paths_part_two(vec)
            default_distance = distance[vec]

            for tile, dist in tiles:
                cheat_distance = distance[tile] + dist

                saved_seconds = default_distance - cheat_distance
                if saved_seconds > 0:
                    cheats[saved_seconds] = cheats.get(saved_seconds, 0) + 1

        if self.is_test:
            return str(sorted(cheats.items()))
        
        count = 0
        for seconds, occurences in sorted(cheats.items()):
            if seconds >= 100:
                count += occurences

        return str(count)
