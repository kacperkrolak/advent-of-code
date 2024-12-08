from collections import Counter
from solution_base import SolutionBase
from typing import TextIO
from enum import Enum
from vector import Vector
        
UP = Vector(0, -1)
DOWN = Vector(0, 1)
LEFT = Vector(-1, 0)
RIGHT = Vector(1, 0)

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        # Map of the grid, consists of dots and hashes.
        self.grid: list[list[str]] = []
        
        # Part 2 only: Position of the wall we added, needed to remove it later
        self.wall_position: Vector | None = None
        
        self.start_position: Vector = Vector(0, 0) # Constant
        # Position visited in the default path (not used when detecting loops in part 2)
        self.visited: dict[int, Vector] = {}

        line_number = 0
        for line in file:
            row = list(line.strip())
            try:
                index = row.index('^')
                row[index] = "."
                self.start_position = Vector(index, line_number)
            except ValueError:
                pass

            self.grid.append(row)
            line_number += 1
            
        self.reset_position()
            
    def reset_position(self):
        self.position = self.start_position.copy()
        self.direction = UP
            
    def get_char(self, pos: Vector):
        if pos.x < 0 or pos.x >= len(self.grid[0]) or pos.y < 0 or pos.y >= len(self.grid):
            return None

        return self.grid[pos.y][pos.x]
            
    def rotate_right(self):
        dir = self.direction
        if dir.equals(UP):
            self.direction = RIGHT
        elif dir.equals(RIGHT):
            self.direction = DOWN
        elif dir.equals(DOWN):
            self.direction = LEFT
        else:
            self.direction = UP
    
    def step_back(self):
        self.position.subtract(self.direction)
        
    # Return True if character exited the grid
    # If track_visited is True, add the position to visited,
    # but we don't need to track visited when checking for loops
    def go_straight(self, direction: Vector, track_visited: bool = True) -> bool:
        while True:
            self.position.add(direction)
            char = self.get_char(self.position)
            match char:
                case None:
                    return True
                case ".":
                    if track_visited:
                        self.visited[hash(self.position)] = self.position.copy()
                case "#":
                    self.step_back()
                    return False
    
    def simulate_default_path(self):
        self.visited[hash(self.position)] = self.position

        while True:
            exited_grid = self.go_straight(self.direction, track_visited=True)
            if exited_grid:
                break
            
            self.rotate_right()
    
    # If we turn twice in the same direction on the same field, we have a loop.
    # If we exit the grid, there is no loop.
    def is_loop(self) -> bool:
        self.reset_position()

        # Data structure to track turning positions
        hash_turning_position = lambda pos, dir: f'{pos.x},{pos.y},{dir.x},{dir.y}'
        turning_positions: set[str] = set()
        
        while True:
            exited_grid = self.go_straight(self.direction, track_visited=False)
            if exited_grid:
                return False
            
            if hash_turning_position(self.position, self.direction) in turning_positions:
                return True
            
            turning_positions.add(hash_turning_position(self.position, self.direction))
            self.rotate_right()

    # Simulate going through the default path following these rules:
    # - Move straight if possible, otherwise turn right
    # - Finish when we exit the grid
    def part_one(self):
        self.simulate_default_path()
        return len(self.visited)

    # Try adding a wall in every visited position and count possible loops.
    def part_two(self):
        loops = 0

        self.simulate_default_path()

        self.visited.pop(hash(self.start_position))
        
        walls = []

        while self.visited:
            _, pos = self.visited.popitem()

            # Add temporary wall
            self.grid[pos.y][pos.x] = "#"
            self.wall_position = pos
            
            if self.is_loop():
                walls.append((pos.x, pos.y))
                loops += 1
                
            # Remove the wall
            self.grid[pos.y][pos.x] = "."            

        return loops
            
            
            
