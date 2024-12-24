from solution_base import SolutionBase
from typing import TextIO

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.values: dict[str, int] = {}
        self.gate_definitions: dict[str, tuple[str, str, str]] = {}
        
        line = file.readline()
        while line.strip() != "":
            gate, val = line.strip().split(":")
            self.values[gate] = int(val)
            line = file.readline()

        line = file.readline()
        while line.strip() != "":
            operation, output_gate = line.strip().split(" -> ")
            input1, operation, input2 = operation.split()
            self.gate_definitions[output_gate] = (input1, input2, operation)
            line = file.readline()

    def evaluate_gate(self, gate: str) -> int:
        if gate in self.values:
            return self.values[gate]
        
        input1, input2, operation = self.gate_definitions[gate]
        input1_val = self.evaluate_gate(input1)
        input2_val = self.evaluate_gate(input2)
        
        match operation:
            case "AND":
                self.values[gate] = input1_val & input2_val
            case "OR":
                self.values[gate] = input1_val | input2_val
            case "XOR":
                self.values[gate] = input1_val ^ input2_val
            case _:
                raise ValueError(f"Invalid operation: {operation}")
        
        return self.values[gate]

    def part_one(self):
        z_values: dict[str, int] = {}
        for gate in self.gate_definitions:
            if gate.startswith("z"):
                z_values[gate] = self.evaluate_gate(gate)
        
        bin_val = "".join(str(z_values[gate]) for gate in sorted(z_values.keys(), reverse=True))
        return int(bin_val, 2)

    def part_two(self):
        return 0
