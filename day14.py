from solution_base import SolutionBase
from typing import TextIO
from vector import Vector

class Robot:
    def __init__(self, position: Vector, velocity: Vector):
        self.position = position
        self.velocity = velocity
        
    def __repr__(self):
        return f'Robot({self.position}, {self.velocity})'

class Solution(SolutionBase):
    # Example input P=10,-1
    def parse_vector(self, line: str) -> Vector:
        x, y = line.split("=")[1].split(",")
        return Vector(int(x), int(y))
    
    def read_input(self, file: TextIO):
        self.x = 11 if self.is_test else 101
        self.y = 7 if self.is_test else 103

        self.robots: list[Robot] = []

        for line in file:
            self.robots.append(Robot(self.parse_vector(line.split("v")[0]), self.parse_vector(line.split("v")[1])))
            
    def part_one(self) -> int:
        seconds = 100
        
        quadrants: list[int] = [0, 0, 0, 0]
        middle_x = self.x // 2
        middle_y = self.y // 2

        for robot in self.robots:
            x = (robot.position.x + robot.velocity.x * seconds) % self.x
            y = (robot.position.y + robot.velocity.y * seconds) % self.y

            if x > middle_x and y > middle_y:
                quadrants[0] += 1
            elif x < middle_x and y > middle_y:
                quadrants[1] += 1
            elif x < middle_x and y < middle_y:
                quadrants[2] += 1
            elif x > middle_x and y < middle_y:
                quadrants[3] += 1
        
        product = 1
        for quadrant_count in quadrants:
            product *= quadrant_count

        return product

    def save_image(self, positions: set[tuple[int, int]], seconds: int):
        # Create a PPM file for this frame (binary P6 format)
        with open(f'output/frame_{seconds:04d}.ppm', 'wb') as f:
            # PPM header
            f.write(f'P6\n{self.x} {self.y}\n255\n'.encode())
            
            # Write pixel data
            for y in range(self.y):
                for x in range(self.x):
                    if (x, y) in positions:
                        # White for robots (#)
                        f.write(bytes([255, 255, 255]))
                    else:
                        # Black for empty space (.)
                        f.write(bytes([0, 0, 0]))

    # Sum number of neighbors of each robot, the more robots next to each other,
    # the higher the probability they represent a picture.
    # Returns a non-negative integer.
    def is_image_probability(self, positions: set[tuple[int, int]]) -> int:
        probability_score = 0

        for robot in self.robots:
            for neighbor in robot.position.get_neighbors():
                if neighbor.tuple() in positions:
                    probability_score += 1

        return probability_score
    
    # Save all frames with many robots next to each other.
    # Then manually find the pattern.
    def part_two(self) -> str:
        for seconds in range(1, 50000):
            if seconds % 100 == 0:
                print(f'Processing frame {seconds}')
            positions: set[tuple[int, int]] = set()
            for robot in self.robots:
                robot.position.x = (robot.position.x + robot.velocity.x) % self.x
                robot.position.y = (robot.position.y + robot.velocity.y) % self.y
                positions.add((robot.position.x, robot.position.y))


            if self.is_image_probability(positions) > 250:
                self.save_image(positions, seconds)

        return "Check output folder and find the Christmas tree!"
