from copy import deepcopy
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
        moons = []
        vels = []
        for line in data:
            parts = line[1:-1].split(", ")
            moons += [[int(p.split("=")[1]) for p in parts]]
            vels += [[0, 0, 0]]

        times = 1000
        if moons[0] == [-1, 0, 2]:
            times = 10
        elif moons[0] == [-8, -10, 0]:
            times = 100

        for _ in range(times):
            for i in range(4):
                for j in range(4):
                    if i == j:
                        continue
                    for k in range(3):
                        if moons[i][k] > moons[j][k]:
                            vels[i][k] -= 1
                        elif moons[i][k] < moons[j][k]:
                            vels[i][k] += 1
            for i in range(4):
                for k in range(3):
                    moons[i][k] += vels[i][k]
        return sum(sum(abs(m) for m in moons[i]) * sum(abs(v) for v in vels[i]) for i in range(4))

    def part2(self, data):
        moons = []
        vels = []
        for line in data:
            parts = line[1:-1].split(", ")
            moons += [[int(p.split("=")[1]) for p in parts]]
            vels += [[0, 0, 0]]
        org_moons = deepcopy(moons)

        counts = [0, 0, 0]
        times = 0
        while 1:
            times += 1
            for i in range(4):
                for j in range(4):
                    if i == j:
                        continue
                    for k in range(3):
                        if moons[i][k] > moons[j][k]:
                            vels[i][k] -= 1
                        elif moons[i][k] < moons[j][k]:
                            vels[i][k] += 1
            for i in range(4):
                for k in range(3):
                    moons[i][k] += vels[i][k]

            for k in range(3):
                if counts[k] == 0:
                    if all(moons[i][k] == org_moons[i][k] and vels[i][k] == 0 for i in range(4)):
                        counts[k] = times

            if counts.count(0) == 0:
                break

        x, y, z = counts
        return (g := x * y // math.gcd(x, y)) * z // math.gcd(g, z)
