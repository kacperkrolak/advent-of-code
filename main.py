import sys
import os
import importlib
from signal import signal, SIGPIPE, SIG_DFL


def get_filename(day: str, part: int, is_test: bool):
    if not is_test:
        return f"input/{day}.txt"
    
    test_file = f"input/{day}_test.txt"
    if part == 2:
        test_file_two = f"input/{day}_test2.txt"
        if os.path.exists(test_file_two):
            return test_file_two
    
    return test_file
    
def run_part(day: str, part: int, is_test: bool):
    filename = get_filename(day, part, is_test)

    solution = Solution()

    with open(filename, "r") as file:
        solution.read_input(file)
    
    return solution.part_one() if part == 1 else solution.part_two()

if __name__ == "__main__":
    signal(SIGPIPE, SIG_DFL)

    if len(sys.argv) < 2:
        print("Usage: python main.py <day> [test]")
        sys.exit(1)

    day = sys.argv[1]
    is_test = len(sys.argv) > 2 and sys.argv[2] == "test"
    
    # Dynamically import the Solution class from the day's module
    day_module = importlib.import_module(f"day{day}")
    Solution = day_module.Solution

    print(run_part(day, 1, is_test))
    print(run_part(day, 2, is_test))
