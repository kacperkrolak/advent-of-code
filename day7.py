from solution_base import SolutionBase
from typing import TextIO

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.operations = []
        self.operation_incrementer = self.increment_operators
        
        for line in file:
            parts = line.split(":")
            result = int(parts[0])
            ingredients = [int(x) for x in parts[1].split()]
            self.operations.append((result, ingredients))
    
    # Multiplication has higher precedence, so we do it first,
    # then only addition is left.
    def calculate(self, ingredients: list[int], operators: list[str]):
        numbers = ingredients.copy()
        operations = operators.copy()

        result = numbers[0]
        i = 0
        while i < len(operations):
            match operations[i]:
                case "*":
                    result *= numbers[i + 1]
                case "+":
                    result += numbers[i + 1]
                case "||":
                    result = int(str(result) + str(numbers[i + 1]))
                
            i += 1
            
        return result
    
    # Returns True if the operators were incremented, False if we've reached the maximum.
    def increment_operators(self, operators: list[str]) -> bool:
        for i in range(len(operators) -1, -1, -1):
            if operators[i] == "+":
                operators[i] = "*"
                
                for j in range(i + 1, len(operators)):
                    operators[j] = "+"
                return True

        return False
    
    def increment_operators_part_two(self, operators: list[str]) -> bool:
        for i in range(len(operators) -1, -1, -1):
            if operators[i] == "+":
                operators[i] = "*"
                
                for j in range(i + 1, len(operators)):
                    operators[j] = "+"
                return True
                    
            if operators[i] == "*":
                operators[i] = "||"
                
                for j in range(i + 1, len(operators)):
                    operators[j] = "+"
                return True
            
        return False
            
    def check_if_operation_is_possible(self, ingredients: list[int], result: int) -> bool:
        operators = ["+"] * (len(ingredients) - 1)
        
        while True:
            if self.calculate(ingredients, operators) == result:
                return True
            
            if not self.operation_incrementer(operators):
                break
            
        return False
        
        
    def part_one(self):
        self.operation_incrementer = self.increment_operators

        total = 0

        for result, ingredients in self.operations:
            if self.check_if_operation_is_possible(ingredients, result):
                total += result

        return total

    # May take a while to run.
    def part_two(self):
        self.operation_incrementer = self.increment_operators_part_two
        
        total = 0

        for result, ingredients in self.operations:
            if self.check_if_operation_is_possible(ingredients, result):
                total += result

        return total