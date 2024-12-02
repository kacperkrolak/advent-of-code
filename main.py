import sys
import importlib

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <day> [test]")
        sys.exit(1)

    day = sys.argv[1]
    is_test = len(sys.argv) > 2 and sys.argv[2] == "test"
    
    # Dynamically import the Solution class from the day's module
    day_module = importlib.import_module(f"day{day}")
    Solution = day_module.Solution
    
    input_file = f"input/{day}{'_test' if is_test else ''}.txt"

    solution = Solution()

    with open(input_file, "r") as file:
        solution.read_input(file)
    
    print(solution.part_one())
    print(solution.part_two())
