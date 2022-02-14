from collections import defaultdict
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
        basic, reactions = self.parse_reacions(data)

        ore, wasted = self.calc(basic, reactions, "FUEL", 1)
        return ore

    def part2(self, data):
        basic, reactions = self.parse_reacions(data)

        ore1, wasted = self.calc(basic, reactions, "FUEL", 1)
        units = 1000000000000 // ore1 + 1
        while 1:
            ore, wasted = self.calc(basic, reactions, "FUEL", units)
            if ore > 1000000000000:
                return units - 1
            else:
                units += (1000000000000 - ore) // ore1 + 1

    def parse_reacions(self, data):
        basic = {}
        reactions = {}

        for line in data:
            a, b = line.split(" => ")
            ai, an = a.split(" ", 1)
            bi, bn = b.split(" ", 1)
            if an == "ORE":
                basic[bn] = (int(bi), int(ai))
            else:
                lists = a.split(", ")
                items = []
                for item in lists:
                    item = item.split(" ")
                    items += [(int(item[0]), item[1])]
                reactions[bn] = (int(bi), items)
        return basic, reactions

    def calc(self, basic, reactions, target, units):
        wasted = defaultdict(int)

        targets = [(t[0] * units, t[1]) for t in reactions[target][1]]

        while not all(f[1] in basic for f in targets):
            targets_new = []
            for t in targets:
                if t[1] in basic:
                    targets_new += [t]
                else:
                    requires = reactions[t[1]]
                    f0 = t[0]

                    if t[1] in wasted:
                        c = min(wasted[t[1]], f0)
                        f0 -= c
                        wasted[t[1]] -= c

                    count = math.ceil(f0 / requires[0])
                    for i in requires[1]:
                        i0 = i[0] * count
                        if i[1] in wasted:
                            c = min(wasted[i[1]], i0)
                            i0 -= c
                            wasted[i[1]] -= c
                        targets_new += [(i0, i[1])]
                    wasted[t[1]] += requires[0] * count - f0
            targets = targets_new

        basics = defaultdict(int)
        for item in targets:
            basics[item[1]] += item[0]

        ore = sum(math.ceil(v / basic[k][0]) * basic[k][1] for k, v in basics.items())

        return ore, wasted
