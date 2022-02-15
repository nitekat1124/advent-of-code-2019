from collections import defaultdict
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
        panels = defaultdict(int)
        pos = (0, 0)
        facing = 0
        turn = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        dirs = [-1, 1]

        amp = Amp(data[0], 0)
        while 1:
            amp.inputs = [panels[pos]]
            amp.set_status_running()
            outputs = [*amp.run()]
            if amp.is_halt():
                break
            panels[pos] = outputs[-1]  # paint

            amp.inputs += [outputs[-1]]
            amp.set_status_running()
            outputs = [*amp.run()]
            if amp.is_halt():
                break
            facing = (facing + dirs[outputs[-1]] + 4) % 4
            pos = (pos[0] + turn[facing][0], pos[1] + turn[facing][1])

        return len(panels.keys())

    def part2(self, data):
        panels = defaultdict(int)
        pos = (0, 0)
        panels[pos] = 1

        facing = 0
        turn = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        dirs = [-1, 1]

        amp = Amp(data[0], 0)

        while 1:
            amp.inputs = [panels[pos]]
            amp.set_status_running()
            outputs = [*amp.run()]
            if amp.is_halt():
                break
            panels[pos] = outputs[-1]  # paint

            amp.inputs += [outputs[-1]]
            amp.set_status_running()
            outputs = [*amp.run()]
            if amp.is_halt():
                break
            facing = (facing + dirs[outputs[-1]] + 4) % 4
            pos = (pos[0] + turn[facing][0], pos[1] + turn[facing][1])

        keys = list(panels.keys())
        min_x = min(k[0] for k in keys)
        max_x = max(k[0] for k in keys)
        min_y = min(k[1] for k in keys)
        max_y = max(k[1] for k in keys)
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if panels[(x, y)] == 1:
                    print("#", end="")
                else:
                    print(" ", end="")
            print()
