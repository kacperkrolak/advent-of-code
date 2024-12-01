from abc import ABCMeta, abstractmethod

class SolutionBase(metaclass=ABCMeta):
    @abstractmethod
    def read_input(self, input_file):
        pass

    @abstractmethod
    def part_one(self):
        pass

    @abstractmethod
    def part_two(self):
        pass
