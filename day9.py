from solution_base import SolutionBase
from typing import TextIO

class File:
    def __init__(self, id: int, pos: int, size: int):
        self.id = id
        self.pos = pos
        self.size = size
        
    @staticmethod
    def calculate_checksum(files: list) -> int:
        checksum = 0
        for file in files:
            for i in range(file.pos, file.pos + file.size):
                checksum += i * file.id

        return checksum

class FreeSpace:
    def __init__(self, pos: int, size: int):
        self.pos = pos
        self.size = size

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        line = file.readline().strip()
        self.input = list(map(int, line))
    
    def calculate_checksum(self, memory_map):
        checksum = 0
        for i in range(len(memory_map)):
            if memory_map[i] != None:
                checksum += memory_map[i] * i
        return checksum
    
    # Move file blocks from the end to free spaces at the beginning, one by one.
    #
    # For this part I decided to use array to represent each block.
    def part_one(self) -> int:
        memory_map: list[int | None] = []
        
        is_file = True
        file_id = 0
        
        for i in range(len(self.input)):
            if is_file:
                memory_map.extend([file_id for _ in range(self.input[i])])
                file_id += 1
            else:
                memory_map.extend([None for _ in range(self.input[i])])
            is_file = not is_file

        first_free_index = memory_map.index(None)
        last_file_index = len(memory_map) -1

        while first_free_index != -1 and first_free_index < last_file_index:
            if memory_map[last_file_index] == None:
                last_file_index -= 1
                continue

            memory_map[first_free_index] = memory_map[last_file_index]
            first_free_index = memory_map.index(None, first_free_index)
            last_file_index -= 1
            
        
        memory_map = memory_map[:last_file_index+1]
        
        return self.calculate_checksum(memory_map)

    def first_space_long_enough(self, free_spaces: list[FreeSpace], size: int, max_pos: int) -> int:
        for i in range(len(free_spaces)):
            if free_spaces[i].pos > max_pos:
                return -1

            if free_spaces[i].size >= size:
                return i
        
        return -1
    
    # Move full file blocks to the free spaces at the beginning.
    #
    # For this part it makes more sense to represent free spaces and files
    # as their positions and sizes.
    def part_two(self) -> int:
        free_spaces: list[FreeSpace] = []
        files: list[File] = []
        
        pos = 0
        id = 0
        is_file = True
        for i in range(len(self.input)):
            if is_file:
                files.append(File(id, pos, self.input[i]))
                id += 1
            else:
                free_spaces.append(FreeSpace(pos, self.input[i]))
            
            pos += self.input[i]
            is_file = not is_file
        
        for i in range(len(files)-1, -1, -1):
            free_space_index = self.first_space_long_enough(free_spaces, files[i].size, files[i].pos)
            if free_space_index == -1:
                continue

            
            files[i].pos = free_spaces[free_space_index].pos

            free_spaces[free_space_index].size -= files[i].size
            free_spaces[free_space_index].pos += files[i].size
        
        return File.calculate_checksum(files)
