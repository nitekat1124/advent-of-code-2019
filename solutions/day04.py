from collections import Counter
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
        n1, n2 = map(int, data[0].split("-"))
        return sum(1 for i in range(n1, n2 + 1) if self.is_valid(i))

    def part2(self, data):
        n1, n2 = map(int, data[0].split("-"))
        return sum(1 for i in range(n1, n2 + 1) if self.is_valid(i, True))

    def is_valid(self, n, additional_rule=False):
        n = str(n)
        counter = Counter(n)
        not_decrease = "".join(sorted(n)) == n

        if additional_rule:
            valid = not_decrease and any(v == 2 for v in counter.values())
        else:
            valid = not_decrease and any(v >= 2 for v in counter.values())

        return valid
