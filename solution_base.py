from abc import ABCMeta, abstractmethod
from typing import TextIO

class SolutionBase(metaclass=ABCMeta):
    @abstractmethod
    def read_input(self, file: TextIO):
        pass

    @abstractmethod
    def part_one(self):
        pass

    @abstractmethod
    def part_two(self):
        pass
