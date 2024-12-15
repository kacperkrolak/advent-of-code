from solution_base import SolutionBase
from typing import TextIO
from vector import Vector
from enum import Enum

class Type(Enum):
    WALL = 0
    EMPTY = 1
    # PART 1
    BOX = 2
    # PART 2
    BOX_LEFT = 3
    BOX_RIGHT = 4
    
    def __str__(self) -> str:
        match self:
            case Type.WALL:
                return '#'
            case Type.EMPTY:
                return '.'
            case Type.BOX:
                return 'O'
            case Type.BOX_LEFT:
                return '['
            case Type.BOX_RIGHT:
                return ']'
            case _:
                raise ValueError(f'Invalid type: {self}')

UP = Vector(0, -1)
DOWN = Vector(0, 1)
LEFT = Vector(-1, 0)
RIGHT = Vector(1, 0)

class Map:
    def __init__(self):
        self.map: list[str] = []
    
    def get_char(self, position: Vector) -> Type:
        if position.y < 0 or position.y >= len(self.map) or position.x < 0 or position.x >= len(self.map[position.y]):
            return Type.WALL

        match self.map[position.y][position.x]:
            case '#':
                return Type.WALL
            case '.':
                return Type.EMPTY
            case 'O':
                return Type.BOX
            case '[':
                return Type.BOX_LEFT
            case ']':
                return Type.BOX_RIGHT
            case _:
                raise ValueError(f'Invalid character: {self.map[position.y][position.x]}')
            
    def set_char(self, position: Vector, type: Type) -> None:
        self.map[position.y] = self.map[position.y][:position.x] + str(type) + self.map[position.y][position.x + 1:]
        
    def __repr__(self) -> str:
        result = ""
        for row in self.map:
            result += row + "\n"
        return result

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.map: Map = Map()
        self.map_input: list[str] = []
        self.robot_position: Vector = Vector(0, 0)
        self.instructions: str = ""
        
        line = file.readline().strip()
        while line:
            self.map_input.append(line)
            line = file.readline().strip()
            
        line = file.readline().strip()
        while line:
            self.instructions += line
            line = file.readline().strip()
    
    def build_part_one_map(self) -> None:
        for line in self.map_input:
            robot_index = line.find('@')
            if robot_index != -1:
                self.robot_position = Vector(robot_index, len(self.map.map))
                line = line[:robot_index] + '.' + line[robot_index + 1:]
                
            self.map.map.append(line)
            
    def build_part_two_map(self) -> None:
        for i, line in enumerate(self.map_input):
            self.map.map.append("")
            for j, char in enumerate(line):
                match char:
                    case '#':
                        self.map.map[i] += '##'
                    case '.':
                        self.map.map[i] += '..'
                    case '@':
                        self.robot_position = Vector(len(self.map.map[i]), i)
                        self.map.map[i] += '..'
                    case 'O':
                        self.map.map[i] += '[]'
                    case _:
                        raise ValueError(f'Invalid character: {char}')


    def apply_changes(self, changes: list[tuple[Vector, Type]]) -> None:
        for position, type in changes:
            self.map.set_char(position, type)

    def move(self, direction: Vector) -> None:
        changes: list[tuple[Vector, Type]] = []

        position = self.robot_position.copy()
        previous_type = self.map.get_char(position)
        while True:
            position.add(direction)
            next_type = self.map.get_char(position)
            
            # Walls are immovable, don't move.
            if next_type == Type.WALL:
                return
            
            changes.append((position.copy(), previous_type))
            
            # We have space to push the blocks, apply the changes.
            if next_type == Type.EMPTY:
                break
            
            previous_type = next_type

        self.apply_changes(changes)
        self.robot_position.add(direction)
    
    def move_part_two(self, direction: Vector) -> None:
        changes: list[tuple[Vector, Type]] = []
        queue: list[Vector] = [self.robot_position.copy()]
        q_len: int = 1
        
        pushed_boxes: set[tuple[int, int]] = set()
        
        while q_len > 0:
            for i in range(q_len):
                cur_position = queue[i]
                cur_type = self.map.get_char(cur_position)

                pushed_boxes.add(cur_position.tuple())

                previous_position = cur_position.copy().add(direction.copy().scale(-1))
                if previous_position.tuple() in pushed_boxes:
                    changes.append((cur_position, self.map.get_char(previous_position)))
                else:
                    changes.append((cur_position, Type.EMPTY))

                next_position = cur_position.copy().add(direction)
                next_type = self.map.get_char(next_position)

                match next_type:
                    case Type.WALL:
                        # Walls are immovable, don't move.
                        return
                    case Type.EMPTY:
                        changes.append((next_position, cur_type))
                    case Type.BOX_LEFT:                                      
                        queue.append(next_position.copy())
                        queue.append(next_position.copy().add(RIGHT))
                    case Type.BOX_RIGHT:
                        queue.append(next_position.copy())
                        queue.append(next_position.copy().add(LEFT))


            queue = queue[q_len:]
            q_len = len(queue)
            
        self.apply_changes(changes)
        self.robot_position.add(direction)

    def part_one(self):
        self.build_part_one_map()

        for instruction in self.instructions:
            match instruction:
                case '^':
                    direction = UP
                case 'v':
                    direction = DOWN
                case '<':
                    direction = LEFT
                case '>':
                    direction = RIGHT
                case _:
                    raise ValueError(f'Invalid instruction: {instruction}')

            self.move(direction)
        
        coordinate_sum = 0
        for i, row in enumerate(self.map.map):
            for j, char in enumerate(row):
                if char == 'O':
                    coordinate_sum += i * 100 + j

        print(self.map)
        return coordinate_sum

    def part_two(self):
        self.build_part_two_map()
        
        for instruction in self.instructions:
            # Part 1 moving will work for horizontal movement.
            match instruction:
                case '^':
                    self.move_part_two(UP)
                case 'v':
                    self.move_part_two(DOWN)
                case '<':
                    self.move(LEFT)
                case '>':
                    self.move(RIGHT)
                case _:
                    raise ValueError(f'Invalid instruction: {instruction}')

        coordinate_sum = 0
        for i, row in enumerate(self.map.map):
            for j, char in enumerate(row):
                if char == '[':
                    coordinate_sum += i * 100 + j

        print(self.map)
        return coordinate_sum