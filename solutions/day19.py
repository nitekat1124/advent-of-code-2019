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
        count = 0
        for y in range(50):
            for x in range(50):
                amp = Amp(data[0])
                amp.inputs = [x, y]
                outputs = [*amp.run()]
                if outputs[0] == 1:
                    count += 1
        return count

    def part2(self, data):
        y = 100

        while 1:
            x_top_max = None
            flag = 0
            for x in range(y):
                amp = Amp(data[0])
                amp.inputs = [x, y]
                outputs = [*amp.run()]
                if outputs[0] == 1:
                    flag = 1
                elif flag == 1:
                    x_top_max = x - 1
                    break

            x_btm_min = None
            for x in range(y + 99):
                amp = Amp(data[0])
                amp.inputs = [x, y + 99]
                outputs = [*amp.run()]
                if outputs[0] == 1:
                    x_btm_min = x
                    break

            if x_btm_min + 99 == x_top_max:
                return x_btm_min * 10000 + y
            else:
                diff = x_top_max - x_btm_min
                if diff > 100:
                    y = int(y / 1.02)
                elif diff < 95:
                    y = int(y * 1.1)
                else:
                    y += 1
