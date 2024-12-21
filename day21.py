from solution_base import SolutionBase
from typing import TextIO
from vector import Vector
from enum import Enum

def get_horizontal_target(cur_pos: Vector, target_pos: Vector) -> None | str:
    if cur_pos.x == target_pos.x:
        return None
    return ">" if cur_pos.x < target_pos.x else "<"

def get_vertical_target(cur_pos: Vector, target_pos: Vector) -> None | str:
    if cur_pos.y == target_pos.y:
        return None
    return "v" if cur_pos.y < target_pos.y else "^"

def shortest_path_directional(start: str, end: str) -> str | list[str]:
        """
            +---+---+ We need to find the shortest sequence of moves,
            | ^ | A | (v, >, <, ^, A again).
        +---+---+---+
        | < | v | > | We prefer TOP and RIGHT over DOWN over LEFT.
        +---+---+---+
        """
                
        positions: dict[str, Vector] = {
            "^": Vector(1, 0), "A": Vector(2, 0),
            "<": Vector(0, 1), "v": Vector(1, 1), ">": Vector(2, 1)
        }
        
        cur_pos = positions[start].copy()
        target_pos = positions[end].copy()
        
        result = ""

        horizontal_target = get_horizontal_target(cur_pos, target_pos)
        vertical_target = get_vertical_target(cur_pos, target_pos)
        
        if horizontal_target and vertical_target:
            if target_pos.x == 0 and target_pos.y == 1:
                # Vertical first
                result += vertical_target
                result += horizontal_target * (abs(cur_pos.x - target_pos.x))
                return result + "A"
            if cur_pos.x == 0 and cur_pos.y == 1:
                # Horizontal first
                result += horizontal_target * (abs(cur_pos.x - target_pos.x))
                result += vertical_target
                return result + "A"
            
            
            result1 = result + vertical_target + horizontal_target * (abs(cur_pos.x - target_pos.x)) + "A"
            result2 = result + horizontal_target * (abs(cur_pos.x - target_pos.x)) + vertical_target + "A"
    
            return [result1, result2]
    
        if horizontal_target:
            result += horizontal_target * (abs(cur_pos.x - target_pos.x))
        if vertical_target:
            result += vertical_target

        return result + "A"
    
class Counter:
    def __init__(self, start: str, end: str, counters: dict[str, "Counter"]):
        self.start: str = start
        self.end: str = end
        self.next: list[list["Counter"]] = []
        self.counters = counters
        self.count_per_iteration: dict[int, int] = {
            0: 1
        }
    
    # Get the stones this counter's stone will transform into.
    def set_next_references(self):
        path = shortest_path_directional(self.start, self.end)
        if not isinstance(path, list):
            path = [path]

        for p in path:
            p = "A" + p
            self.next.append([])
            for i in range(len(p) - 1):
                if p[i] + p[i + 1] not in self.counters:
                    self.counters[p[i] + p[i + 1]] = Counter(p[i], p[i + 1], self.counters)

                self.next[-1].append(self.counters[p[i] + p[i + 1]])

    def get_count(self, iteration: int) -> int:
        if iteration in self.count_per_iteration:
            return self.count_per_iteration[iteration]
        
        if self.next == []:
            self.set_next_references()
        
        min_count = float('inf')
        for next_reference in self.next:
            s = 0
            for i in range(len(next_reference)):
                s += next_reference[i].get_count(iteration - 1)
            if s < min_count:
                min_count = s

        self.count_per_iteration[iteration] = min_count

        return self.count_per_iteration[iteration]

def append_all(sequences: list[str], move: str, count: int = 1) -> None:
    for i in range(len(sequences)):
        sequences[i] += move * count

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.codes = []
        self.counters: dict[str, Counter] = {}

        for line in file:
            self.codes.append(line.strip())
    
    def shortest_sequence_numerical(self, code: str) -> list[str]:
        """
        +---+---+---+ This is the keypad,
        | 7 | 8 | 9 | we need a sequence of
        +---+---+---+ >, <, ^, v, A codes,
        | 4 | 5 | 6 | which we represent as
        +---+---+---+ Move enum.
        | 1 | 2 | 3 |
        +---+---+---+ We need to find the shortest sequence,
            | 0 | A | but also prefer TOP and RIGHT over DOWN over LEFT.
            +---+---+
        """
        positions: dict[str, Vector] = {
            "7": Vector(0, 0), "8": Vector(1, 0), "9": Vector(2, 0),
            "4": Vector(0, 1), "5": Vector(1, 1), "6": Vector(2, 1),
            "1": Vector(0, 2), "2": Vector(1, 2), "3": Vector(2, 2),
            "0": Vector(1, 3), "A": Vector(2, 3)
        }
        
        sequences: list[str] = [""]
        
        target_pos = positions['A'].copy()
        
        for i in range(len(code)):
            cur_pos = target_pos.copy() # Set current position to previous target position
            target_pos = positions[code[i]]
            
            horizontal_target = get_horizontal_target(cur_pos, target_pos)
            vertical_target = get_vertical_target(cur_pos, target_pos)
            
            if horizontal_target and vertical_target:
                new_sequences: list[str] = []
            
                horizontal_sequence = horizontal_target * abs(cur_pos.x - target_pos.x)
                vertical_sequence = vertical_target * (abs(cur_pos.y - target_pos.y))
                
                for sequence in sequences:
                    # Make sure not to hover over empty space.
                    if cur_pos.y != 3 or target_pos.x != 0:
                        new_sequences.append(sequence + horizontal_sequence + vertical_sequence + "A")
                    if cur_pos.x != 0 or target_pos.y != 3:
                        new_sequences.append(sequence + vertical_sequence + horizontal_sequence + "A")

                sequences = new_sequences
                continue

            if horizontal_target:
                append_all(sequences, horizontal_target, abs(cur_pos.x - target_pos.x))

            if vertical_target:
                append_all(sequences, vertical_target, abs(cur_pos.y - target_pos.y))

            append_all(sequences, "A")


        return sequences
    
    # def shortest_sequence_directional(self, sequence: list[Move]) -> list[Move]:
    #     """
    #         +---+---+ We need to find the shortest sequence of moves,
    #         | ^ | A | (v, >, <, ^, A again).
    #     +---+---+---+
    #     | < | v | > | We prefer TOP and RIGHT over DOWN over LEFT.
    #     +---+---+---+
    #     """
        
    #     result_sequence: list[Move] = []
        
    #     positions: dict[Move, Vector] = {
    #         Move.UP: Vector(1, 0), Move.PUSH: Vector(2, 0),
    #         Move.LEFT: Vector(0, 1), Move.DOWN: Vector(1, 1), Move.RIGHT: Vector(2, 1)
    #     }
        
    #     target_pos = positions[Move.PUSH].copy()
        
    #     for i in range(len(sequence)):
    #         cur_pos = target_pos.copy()
    #         target_pos = positions[sequence[i]]
            
    #         horizontal_target = get_horizontal_direction(cur_pos, target_pos)
    #         vertical_target = get_vertical_direction(cur_pos, target_pos)
            
    #         if horizontal_target and vertical_target:
    #             if cur_pos.x != 0 and cur_pos.y != 1:
    #                 # Vertical first
    #                 result_sequence.append(vertical_target)
    #                 result_sequence += [horizontal_target for _ in range(abs(cur_pos.x - target_pos.x))]
    #             else:
    #                 # Horizontal first
    #                 result_sequence += [horizontal_target for _ in range(abs(cur_pos.x - target_pos.x))]
    #                 result_sequence.append(vertical_target)                    
                
    #             result_sequence.append(Move.PUSH)
    #             continue
                
    #         if horizontal_target:
    #             result_sequence += [horizontal_target for _ in range(abs(cur_pos.x - target_pos.x))]
    #         if vertical_target:
    #             result_sequence.append(vertical_target)
                
    #         result_sequence.append(Move.PUSH)

    #     return result_sequence

    def get_complexity(self, robots: int) -> int:
        complexity: int = 0

        for code in self.codes:
            withoutLeadingZero = code.strip("0")
            onlyDigits = withoutLeadingZero.strip("A")
            
            first_sequences = self.shortest_sequence_numerical(code)
            min_length = float('inf')

            for j, first_sequence in enumerate(first_sequences):
                first_sequence = 'A' + first_sequence
                # print(code, first_sequence)
                count = 0
                for i in range(len(first_sequence) - 1):
                    cur_char = first_sequence[i]
                    next_char = first_sequence[i + 1]
                    
                    if cur_char + next_char not in self.counters:
                        self.counters[cur_char + next_char] = Counter(cur_char, next_char, self.counters)

                    c = self.counters[cur_char + next_char].get_count(robots)
                    # print(c)
                    count += c

                if count < min_length:
                    min_length = count

            complexity += min_length * int(onlyDigits)

        return complexity

    def part_one(self):
        return self.get_complexity(2)

    def part_two(self):
        return self.get_complexity(25)

