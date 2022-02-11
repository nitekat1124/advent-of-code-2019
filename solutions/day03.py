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
        directions = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}

        line1 = set()
        line2 = set()

        p1 = (0, 0)
        for inst in data[0].split(","):
            d = inst[0]
            n = int(inst[1:])
            for _ in range(n):
                p1 = (p1[0] + directions[d][0], p1[1] + directions[d][1])
                line1.add(p1)

        p2 = (0, 0)
        for inst in data[1].split(","):
            d = inst[0]
            n = int(inst[1:])
            for _ in range(n):
                p2 = (p2[0] + directions[d][0], p2[1] + directions[d][1])
                line2.add(p2)

        return min(abs(i[0]) + abs(i[1]) for i in (line1 & line2))

    def part2(self, data):
        directions = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}

        line1 = {}
        line2 = {}

        p1 = (0, 0)
        l1 = 0
        for inst in data[0].split(","):
            d = inst[0]
            n = int(inst[1:])
            for _ in range(n):
                p1 = (p1[0] + directions[d][0], p1[1] + directions[d][1])
                l1 += 1
                line1[p1] = min(l1, line1.get(p1, l1))

        p2 = (0, 0)
        l2 = 0
        for inst in data[1].split(","):
            d = inst[0]
            n = int(inst[1:])
            for _ in range(n):
                p2 = (p2[0] + directions[d][0], p2[1] + directions[d][1])
                l2 += 1
                line2[p2] = min(l2, line2.get(p2, l2))

        return min(line1[i] + line2[i] for i in (set(line1.keys()) & set(line2.keys())))
