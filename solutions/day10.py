import math
from collections import defaultdict
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
        _, station_pos, max_detection = self.parse_asteroids(data)
        print(station_pos)
        return max_detection

    def part2(self, data):
        asteroids, station_pos, _ = self.parse_asteroids(data)

        asteroids_relative = [(a[0] - station_pos[0], a[1] - station_pos[1]) for a in asteroids if a != station_pos]
        aster_angles = defaultdict(list)
        for a in asteroids_relative:
            ang = (math.degrees(math.atan2(a[1], a[0]) + math.atan2(1, 0)) + 360) % 360
            aster_angles[ang] += [a]

        angles = sorted(aster_angles.keys())
        destroyed = []
        for k in angles:
            asters = aster_angles[k]
            if len(asters) > 0:
                asters.sort(key=lambda x: x[0] ** 2 + x[1] ** 2)
                destroyed += [asters[0]]
                aster_angles[k] = asters[1:]
                if len(destroyed) == 200:
                    break

        return (destroyed[-1][0] + station_pos[0]) * 100 + destroyed[-1][1] + station_pos[1]

    def parse_asteroids(self, data):
        asteroids = []
        for y, row in enumerate(data):
            for x, c in enumerate(row):
                if c == "#":
                    asteroids += [(x, y)]

        detection = {}
        for idx1, a in enumerate(asteroids):
            count = 0
            for idx2, b in enumerate(asteroids):
                if idx1 == idx2:
                    continue
                x = b[0] - a[0]
                y = b[1] - a[1]
                gcd = math.gcd(abs(x), abs(y))
                xx = x // gcd
                yy = y // gcd
                block = 0
                for i in range(1, gcd):
                    if (a[0] + i * xx, a[1] + i * yy) in asteroids:
                        block += 1
                if block == 0:
                    count += 1
            detection[a] = count

        max_detect = max(list(detection.values()))
        coord = [k for k, val in detection.items() if val == max_detect][0]

        return asteroids, coord, max_detect
