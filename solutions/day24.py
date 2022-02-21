import binascii
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
        _map = defaultdict(lambda: ".")
        for y, line in enumerate(data):
            for x, c in enumerate(line):
                _map[(x, y)] = c

        c = self.make_crc(_map)
        layout = {c}

        while 1:
            _map = self.run_process(_map)
            c = self.make_crc(_map)
            if c in layout:
                return self.calc_rating(_map)
            layout.add(c)

    def part2(self, data):
        times = 200 if data[0] == "#####" else 10

        _map = defaultdict(lambda: ".")
        for y, line in enumerate(data):
            for x, c in enumerate(line):
                _map[(x, y)] = c

        _maps = {}
        _maps[0] = _map
        for i in range(1, times + 1):
            _maps[i] = defaultdict(lambda: ".")
            _maps[-i] = defaultdict(lambda: ".")

        for _ in range(times):
            _maps = self.run_process_recursive(_maps)

        c = 0
        for i in range(-times, times + 1):
            v = sum(1 for v in _maps[i].values() if v == "#")
            c += v
        return c

    def make_crc(self, _map):
        c = "".join([_map[(i, j)] for i in range(5) for j in range(5)])
        return binascii.crc32(c.encode())

    def run_process(self, _map):
        next_map = defaultdict(lambda: ".")
        dp = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for y in range(5):
            for x in range(5):
                adjs = [tuple(i + j for i, j in zip((x, y), d)) for d in dp]
                if _map[(x, y)] == "#":
                    next_map[(x, y)] = ".#"[sum(1 for i in adjs if _map[i] == "#") == 1]
                else:
                    next_map[(x, y)] = ".#"[sum(1 for i in adjs if _map[i] == "#") in (1, 2)]
        return next_map

    def calc_rating(self, _map):
        return sum(2 ** (k[1] * 5 + k[0]) for k, v in _map.items() if v == "#")

    def run_process_recursive(self, _maps):
        next_maps = {}
        dp = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        max_level = max(_maps.keys())

        for lvl in range(0, max_level):
            levels = [lvl, -lvl]
            for level in levels:
                next_map = defaultdict(lambda: ".")
                for y in range(5):
                    for x in range(5):
                        if x == 2 and y == 2:
                            next_map[(x, y)] = "?"
                            continue
                        adjs = [tuple(i + j for i, j in zip((x, y), d)) for d in dp]
                        tiles = []
                        for idx, p in enumerate(adjs):
                            x1, y1 = p
                            if x1 < 0:
                                tiles += [_maps[level - 1][(1, 2)]]
                            elif x1 > 4:
                                tiles += [_maps[level - 1][(3, 2)]]
                            elif y1 < 0:
                                tiles += [_maps[level - 1][(2, 1)]]
                            elif y1 > 4:
                                tiles += [_maps[level - 1][(2, 3)]]
                            elif x1 == 2 and y1 == 2:
                                if idx == 0:
                                    tiles += [_maps[level + 1][(0, 4)], _maps[level + 1][(1, 4)], _maps[level + 1][(2, 4)], _maps[level + 1][(3, 4)], _maps[level + 1][(4, 4)]]
                                elif idx == 1:
                                    tiles += [_maps[level + 1][(0, 0)], _maps[level + 1][(1, 0)], _maps[level + 1][(2, 0)], _maps[level + 1][(3, 0)], _maps[level + 1][(4, 0)]]
                                elif idx == 2:
                                    tiles += [_maps[level + 1][(4, 0)], _maps[level + 1][(4, 1)], _maps[level + 1][(4, 2)], _maps[level + 1][(4, 3)], _maps[level + 1][(4, 4)]]
                                elif idx == 3:
                                    tiles += [_maps[level + 1][(0, 0)], _maps[level + 1][(0, 1)], _maps[level + 1][(0, 2)], _maps[level + 1][(0, 3)], _maps[level + 1][(0, 4)]]
                            else:
                                tiles += [_maps[level][(x1, y1)]]
                        count = tiles.count("#")

                        if _maps[level][(x, y)] == "#":
                            next_map[(x, y)] = ".#"[count == 1]
                        else:
                            next_map[(x, y)] = ".#"[count in (1, 2)]
                next_maps[level] = next_map

                if level == 0:
                    break

            next_maps[max_level] = defaultdict(lambda: ".")
            next_maps[-max_level] = defaultdict(lambda: ".")
        return next_maps
