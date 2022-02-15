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
        amp = Amp(data[0], 0)
        tile_data = []
        output = None
        while 1:
            if output is not None:
                amp.inputs = [output]
            amp.set_status_running()
            outputs = [*amp.run()]
            if amp.is_halt():
                break
            output = outputs[-1]
            tile_data += [output]
        tile_ids = tile_data[2::3]
        return tile_ids.count(2)

    def part2(self, data):
        amp = Amp(data[0], 0)
        amp.insts[0] = 2
        tile_data = []

        score = 0
        ball = None
        paddle = None
        ball_dir = None

        output = None
        while 1:
            if output is not None:
                amp.inputs = [output]
            amp.set_status_running()
            outputs = [*amp.run()]
            if amp.is_halt():
                break
            output = outputs[-1]
            tile_data += [output]

            if len(tile_data) and len(tile_data) % 3 == 0:
                x, y, z = tile_data[-3:]

                if x == -1 and y == 0:
                    score = z

                if z == 3:
                    paddle = (x, y)
                elif z == 4:
                    old_ball = ball
                    ball = (x, y)
                    if old_ball is not None:
                        ball_dir = ball[0] - old_ball[0]
                    if paddle is not None:
                        if paddle[0] != ball[0]:
                            d = [-1, 1][ball[0] + ball_dir > paddle[0]]
                            output = d
                        else:
                            output = 0

        return score
