import math
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
        nums = [*map(int, data[0])]
        pattern = [0, 1, 0, -1]
        len_nums = len(nums)

        for _ in range(100):
            nums_new = []
            for i in range(len_nums):
                pattern_new = []
                for p in pattern:
                    pattern_new.extend([p] * (i + 1))
                times = math.ceil(len_nums / len(pattern_new)) + 1
                pattern_new = pattern_new * times
                pattern_new = pattern_new[1 : len_nums + 1]

                # nums_new += [abs(sum(a * b for a, b in zip(nums, pattern_new))) % 10]
                nums_new += [abs(sum(nums[x] * pattern_new[x] for x in range(len_nums))) % 10]
            nums = nums_new

        return "".join(map(str, nums[:8]))

    def part2(self, data):
        """
        looking at the input signals and the offset
        we can find the pattern that start from the offset will be
        [1, 1, 1, 1, 1, 1, 1 ......]
        [0, 1, 1, 1, 1, 1, 1 ......]
        [0, 0, 1, 1, 1, 1, 1 ......]
        [0, 0, 0, 1, 1, 1, 1 ......]
        [0, 0, 0, 0, 1, 1, 1 ......]
        and so on
        so the solution is trivial
        """
        offset = int(data[0][:7])
        org_length = len(data[0]) * 10000
        offset2 = org_length - offset
        times = math.ceil(offset2 / 10000) * 10000

        nums = ([*map(int, data[0])] * times)[-offset2:]
        len_nums = len(nums)

        for _ in range(100):
            nums_new = []
            offset_sum = sum(nums)
            for x in range(len_nums):
                if x > 0:
                    offset_sum -= nums[x - 1]
                nums_new += [abs(offset_sum) % 10]
            nums = nums_new

        return "".join(map(str, nums[:8]))
