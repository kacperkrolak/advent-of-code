from solution_base import SolutionBase
from typing import TextIO

class BiDict(dict):
    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __len__(self):
        """Returns the number of connections"""
        return dict.__len__(self) // 2

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.values: dict[str, int] = {}
        self.gate_definitions: dict[str, tuple[str, str, str]] = {}
        self.aliases: dict[str, str] = {}
        self.lines = file.readlines()
            
    def read_operations(self, swaps: BiDict) -> None:
        last_index = 0
        for i, line in enumerate(self.lines):
            if line.strip() == "":
                last_index = i
                break

            gate, val = line.strip().split(":")
            self.values[gate] = int(val)
            
        for line in self.lines[last_index+1:]:
            operation, output_gate = line.strip().split(" -> ")
            if output_gate in swaps:
                output_gate = swaps[output_gate]

            input1, operation, input2 = operation.split()
            input1, input2 = sorted([input1, input2])
            # If the gate = xNUM AND yNUM, then rename it to aNUM to make it more readable.
            if operation == "AND" and input1.startswith("x") and input2.startswith("y") and not output_gate.startswith("z"):
                self.aliases[output_gate] = "a" + input2[1:]
            elif operation == "XOR" and input1.startswith("x") and input2.startswith("y") and not output_gate.startswith("z"):
                self.aliases[output_gate] = "b" + input2[1:]
                
            self.gate_definitions[output_gate] = (input1, input2, operation)


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

    def get_calculated_sum(self) -> int:
        z_values: dict[str, int] = {}
        for gate in self.gate_definitions:
            if gate.startswith("z"):
                z_values[gate] = self.evaluate_gate(gate)
        
        bin_val = "".join(str(z_values[gate]) for gate in sorted(z_values.keys(), reverse=True))
        return int(bin_val, 2)

    def part_one(self):
        swaps = BiDict()
        self.read_operations(swaps)
        return self.get_calculated_sum()

    def print_levels(self, levels: list[set[str]], start_index: int = 1) -> None:
        l_index = start_index
        for level in levels[l_index:]:
            print(str(l_index).zfill(3), self.level_to_str(level))
            l_index += 1

    def level_to_str(self, level: set[str]) -> str:
        l = []
        for gate in sorted(level):
            i1, i2, op = self.gate_definitions[gate]
            if gate in self.aliases:
                gate = self.aliases[gate]
            if i1 in self.aliases:
                i1 = self.aliases[i1]
            if i2 in self.aliases:
                i2 = self.aliases[i2]
            l.append(f"{gate} = {i1} {op} {i2}")
        return str(l)

    def find_gate_used_as_input(self, gate_name: str) -> list[str]:
        found: list[str] = []
        for gate, values in self.gate_definitions.items():
            if gate_name in values:
                found.append(gate)
        
        return found

    def get_expected_sum(self) -> int:
        x_values: dict[str, int] = {}
        y_values: dict[str, int] = {}
        for gate in self.values:
            if gate.startswith("x"):
                x_values[gate] = self.values[gate]
            if gate.startswith("y"):
                y_values[gate] = self.values[gate]
        
        x_bin = "".join(str(x_values[gate]) for gate in sorted(x_values.keys(), reverse=True))
        y_bin = "".join(str(y_values[gate]) for gate in sorted(y_values.keys(), reverse=True))
        
        return int(x_bin, 2) + int(y_bin, 2)
    
    def print_issue(self, l_index: int, level: set[str], expected: str) -> None:
        print(f"Level {l_index:02}, got: {self.level_to_str(level)}, expected: {expected}")
        index = (l_index) // 2
        a_gate, b_gate = f"a{index:02}", f"b{index:02}"
        aliases = {}
        values = list(self.aliases.values())
        try:
            key = list(self.aliases.keys())[values.index(a_gate)]
            aliases[key] = a_gate
        except ValueError:
            pass
        try:
            key = list(self.aliases.keys())[values.index(b_gate)]
            aliases[key] = b_gate
        except ValueError:
            pass
        print("Aliases:", aliases)
        
    def alias(self, gate: str) -> str:
        if gate in self.aliases:
            return self.aliases[gate]
        return gate
    
    def find_first_issue(self, levels: list[set[str]]) -> None:
        # Find all the issues
        prev_important_gate = next((k for k in levels[2] if not str(k).startswith('z')), None)
        print(prev_important_gate)
        prev_was_and_xor = True
        l_index = 3
        for level in levels[l_index:]:
            if prev_was_and_xor:
                if len(level) != 1:
                    print(l_index, level, f"Expected one or using {prev_important_gate}")
                    return
                gate_name = level.copy().pop()
                i1, i2, op = self.gate_definitions[gate_name]
                input_aliases = [self.alias(i1), self.alias(i2)]
                expected_gate_alias = "a" + str(l_index // 2).zfill(2)
                
                if (op != "OR") or prev_important_gate not in input_aliases or expected_gate_alias not in input_aliases:
                    self.print_issue(l_index, level, f"'{gate_name} = {prev_important_gate} OR {expected_gate_alias}'")
                    return
                prev_important_gate = gate_name
                prev_was_and_xor = False
            else:
                num = (l_index + 1) // 2
                expected_b_gate = "b" + str(num).zfill(2)
                expected_z_gate = "z" + str(num).zfill(2)
                expected = f"['{expected_z_gate} = {prev_important_gate} XOR {expected_b_gate}', '<some gate> = {prev_important_gate} AND {expected_b_gate}']"
                if len(level) != 2:
                    self.print_issue(l_index, level, expected)
                    return
                z_gate_name, other_gate_name = None, None
                z_in_1, z_in_2, z_op = None, None, None
                other_in_1, other_in_2, other_op = None, None, None
                
                for gate in level:
                    i1, i2, op = self.gate_definitions[gate]
                    if gate.startswith("z"):
                        z_gate_name = gate
                        z_in_1, z_in_2, z_op = i1, i2, op
                    else:
                        other_gate_name = gate
                        other_in_1, other_in_2, other_op = i1, i2, op
                expected = f"['{expected_z_gate} = {prev_important_gate} XOR {expected_b_gate}', '{other_gate_name} = {prev_important_gate} AND {expected_b_gate}']"
                
                additional_error_msg = ""
                match True:
                    case True if len(level) != 2:
                        additional_error_msg = "Expected 2 gates"
                    case True if z_op != "XOR" or other_op != "AND":
                        additional_error_msg = "Z should be XOR and other gate should be AND"
                    case True if z_in_1 != prev_important_gate and z_in_2 != prev_important_gate:
                        additional_error_msg = "Expected z gate to have prev_important_gate as input"
                    case True if other_in_1 != prev_important_gate and other_in_2 != prev_important_gate:
                        additional_error_msg = "Expected other gate to have prev_important_gate as input"
                    case True if z_in_1 != other_in_1 and z_in_2 != other_in_2:
                        additional_error_msg = "Expected z gate and other gate to have the same inputs"
                    case True if expected_b_gate not in [self.alias(other_in_1), self.alias(other_in_2)]:
                        additional_error_msg = f"Expected other gate to have {expected_b_gate} as input"
                if additional_error_msg:
                    self.print_issue(l_index, level, f"{expected} ({additional_error_msg})")
                    return

                prev_was_and_xor = True
                prev_important_gate = other_gate_name
            l_index += 1
 
    
    # After manual checking, the pattern is
    # Level 0: x00, ..., xNUM, y00, ..., yNUM
    # Level 1: a00 = x00 AND y00, ..., aNUM = xNUM AND yNUM
    # Even levels:
    #   zNum = gate1 XOR gate2, gate3 = gate1 AND gate2 - where zNum starts at 01 and increases by 1
    # Odd levels: 
    #   gate4 = gate3 OR aNum - where aNum is the same as zNum in the previous level
    def part_two(self):
        swaps = BiDict()
        swaps["qdg"] = "z12"
        swaps["vvf"] = "z19"
        swaps["fgn"] = "dck" # a23 and b23
        swaps["nvh"] = "z37"
        self.read_operations(swaps)

        levels: list[set[str]] = []
        
        levels.append(set(self.values.keys()))
        unvisited: set[str] = set(self.gate_definitions.keys())
        
        # For each level find the gates that are not in the previous levels
        # but can be evaluated from the previous levels
        while unvisited:
            next_level = set()
            for gate in unvisited:
                i1, i2, _ = self.gate_definitions[gate]
                if not i1 in unvisited and not i2 in unvisited:
                    next_level.add(gate)

            levels.append(next_level)
            unvisited -= next_level
    
        self.print_levels(levels)
        self.find_first_issue(levels)

        exp = self.get_expected_sum()
        calc = self.get_calculated_sum()
        bin_exp = bin(exp)
        print("Expected sum:  ", bin_exp)
        print("Calculated sum:", bin(calc))
        print("Difference:    ", bin(exp ^ calc).zfill(len(bin_exp)))
        wrong_bits = bin(exp ^ calc)
        zNum = 0
        for i in range(len(wrong_bits)-1, 0, -1):
            if wrong_bits[i] == "1":
                print(f"Z{zNum} is wrong")
            zNum += 1
            
        if exp == calc:
            print("Found the right answer")
            swapped_gates = []
            for k, v in swaps.items():
                swapped_gates.append(k)
                swapped_gates.append(v)
            return ",".join(sorted(set(swapped_gates)))
