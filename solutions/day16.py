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

        for _ in range(100):
            nn = []
            for i in range(len(nums)):
                np = []
                for k in pattern:
                    np.extend([k] * (i + 1))
                t = math.ceil(len(nums) / len(np)) + 1
                np = np * t
                np = np[1 : len(nums) + 1]

                nn += [int(str(sum(a * b for a, b in zip(nums, np)))[-1])]

            nums = nn
        return "".join(str(i) for i in nums)[:8]

    def part2(self, data):
        offset = int(data[0][:7])
        nums = ([*map(int, data[0])] * 10000)[offset:]
        for i in range(100):
            nums_new = []
            nums_sum = sum(nums)
            for x in range(len(nums)):
                if x > 0:
                    nums_sum -= nums[x - 1]
                nums_new += [int(str(nums_sum)[-1])]
            nums = nums_new
        return "".join(str(i) for i in nums[:8])
