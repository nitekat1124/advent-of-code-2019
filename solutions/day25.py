from utils.intcode import Amp
from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def solve(self, part_num: int):
        self.test_runner(part_num)

        func = getattr(self, f"part{part_num}")
        result = func(self.data)
        return result

    def test_runner(self, part_num):
        test_inputs = self.get_test_input()
        test_results = self.get_test_result(part_num)
        test_counter = 1

        func = getattr(self, f"part{part_num}")
        for i, r in zip(test_inputs, test_results):
            if len(r):
                if (tr := str(func(i))) == r[0]:
                    print(f"test {test_counter} passed")
                else:
                    print(f"your result: {tr}")
                    print(f"test answer: {r[0]}")
                    print(f"test {test_counter} NOT passed")
            test_counter += 1
        print()

    def part1(self, data):
        buffer = ""
        printed = ""
        commands = ["west", "south", "take polygon", "north", "east", "north", "west", "take boulder", "east", "north", "take manifold", "west", "south", "east", "south", "take fixed point", "north", "west", "north", "north", "east", "east", "north"]

        _input = input("1) Automatically\n2) Manually\n> ")
        auto = True if _input.strip() == "1" else False

        amp = Amp(data[0])

        while not amp.is_halt():
            if printed == "Command?":
                if auto:
                    if len(commands) == 0:
                        command = input()
                    else:
                        command = commands.pop(0)
                        print(command)
                else:
                    command = input()
                amp.inputs = [ord(c) for c in command + "\n"]
            amp.set_status_running()
            out = [*amp.run()]
            for c in out:
                if c == 10:
                    printed = buffer
                    buffer = ""
                else:
                    buffer += chr(c)
                print(chr(c), end="")

        if printed.find("typing") > -1:
            temp = printed.split()
            print()
            return temp[temp.index("typing") + 1]

    def part2(self, data):
        return "Merry Christmas!"
