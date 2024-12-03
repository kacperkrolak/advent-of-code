from collections import Counter
from solution_base import SolutionBase
from typing import TextIO

# Helper class to abstract the input stream
class CharStream:
    def __init__(self, text: str):
        self.text = text
        self.position = 0
        self.length = len(text)
    
    def current(self) -> str | None:
        """Returns current character or None if at end of stream"""
        if self.position >= self.length:
            return None
        return self.text[self.position]
    
    def next(self) -> str | None:
        """Advances position and returns next character or None if at end of stream"""
        self.position += 1
        return self.current()
    
    def peek(self) -> str | None:
        """Returns next character without advancing position, or None if at end of stream"""
        if self.position + 1 >= self.length:
            return None
        return self.text[self.position + 1]


class Solution(SolutionBase):
    def __init__(self):
        self.total = 0
        self.disabled = False
        self.handling_functions = {}

    def read_input(self, file: TextIO):
        self.stream = CharStream(file.read())

    # Return True if next characters match expected string
    def expect_string(self, expected: str) -> bool:
        if self.stream.current() != expected[0]:
            self.stream.next()
            return False
        
        for i in range(len(expected)):
            if self.stream.current() != expected[i]:
                return False
            
            self.stream.next()

        return True
    
    # Get next digit from the input stream or move to the next char.
    def parse_digit(self) -> None|str:
        digit = self.stream.current()

        if digit is None or not digit.isdigit():
            return None

        self.stream.next()

        return digit
    
    # The numbers in the puzzle are constrained to three digit positive integers.
    def parse_number(self) -> None|int:
        number_str = ""
        for i in range(3):
            digit = self.parse_digit()
            if digit is None:
                return None if number_str == "" else int(number_str)
            number_str += digit
        
        return int(number_str)
    
    # The string we care about are "do", "don't", "mul", so we only need
    # lower case letters and apostrophes
    def is_string_char(self, char: None|str) -> bool:
        if char is None:
            return False
        
        if char == "'":
            return True

        if ord(char) < ord("a") or ord(char) > ord("z"):
            return False
        
        return True
    
    # Get next string from the input stream (a-z or ')
    def parse_string(self) -> str:
        result = ""
        while self.is_string_char(self.stream.current()):
            result += str(self.stream.current())
            self.stream.next()
        
        return result
    
    # Try to get two numbers from the input stream.
    # Return None if we can't get two numbers or if the expression is invalid
    def parse_mul_expression(self) -> None|list[int]:
        numbers = []
        if not self.expect_string("("):
            return None
        
        num1 = self.parse_number()
        if num1 is None:
            return None

        numbers.append(num1)
        
        if not self.expect_string(","):
            return None
        
        
        num2 = self.parse_number()
        if num2 is None:
            return None
        
        numbers.append(num2)
        
        if not self.expect_string(")"):
            return None
        
        return numbers
    
    # If the mul() expression is valid, add the product to the total
    def handle_mul_expression(self) -> None:
        numbers = self.parse_mul_expression()
        if numbers is None:
            return
        
        if not self.disabled:
            self.total += numbers[0] * numbers[1]
        
    # If the do() expression is valid, enable further processing
    def handle_do_expression(self) -> None:
        if not self.expect_string("()"):
            return
        
        self.disabled = False
    
    # If the don't() expression is valid, disable further processing
    def handle_do_not_expression(self) -> None:
        if not self.expect_string("()"):
            return
        
        self.disabled = True
    
    # If the current string ends with a known expression, handle it
    # Otherwise, just move to the next character
    def handle_expression(self):
        name = self.parse_string()
        for key, func in self.handling_functions.items():
            if name.endswith(key):
                func()
                break
        else:
            self.stream.next()        
        
    # Parse the input stream
    def parse(self):
        while self.stream.current() is not None:
            self.handle_expression()

    # We only need to handle mul expressions for part one
    def part_one(self):
        self.handling_functions = {
            "mul": self.handle_mul_expression,
        }
        
        self.parse()
        
        return self.total

    # We need to handle all expressions for part two
    def part_two(self):
        self.handling_functions = {
            "mul": self.handle_mul_expression,
            "do": self.handle_do_expression,
            "don't": self.handle_do_not_expression
        }
                
        self.parse()

        return self.total
