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
        """
        @................
        ###.#############

        @................
        ###..############

        @................
        ###...###########

        @................
        ###.##.##########

        @................
        #####.##.########

        @................
        ###..##.#########

        @................
        ###...#.#########

        any, check if one of A, B, C is hole and D must be a ground
        """
        amp = Amp(data[0])
        amp.inputs = [ord(c) for c in "NOT A T\nNOT B J\nOR J T\nNOT C J\nOR T J\nAND D J\nWALK\n"]

        collect_ouputs = []
        while not amp.is_halt():
            amp.set_status_running()
            outputs = [*amp.run()]
            if outputs:
                collect_ouputs += outputs

        # for c in collect_ouputs:
        #     print(chr(c), end="")

        return collect_ouputs[-1]

    def part2(self, data):
        amp = Amp(data[0])
        amp.inputs = [ord(c) for c in "NOT A T\nNOT B J\nOR T J\nAND D J\nNOT C T\nAND D T\nAND H T\nOR T J\nRUN\n"]

        collect_ouputs = []
        while not amp.is_halt():
            amp.set_status_running()
            outputs = [*amp.run()]
            if outputs:
                collect_ouputs += outputs

        # for c in collect_ouputs:
        #     print(chr(c), end="")

        return collect_ouputs[-1]
