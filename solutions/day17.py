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
        _map = self.get_map(data)

        w = max(x[0] for x in [*_map.keys()])
        h = max(x[1] for x in [*_map.keys()])

        check_points = [(0, -1), (1, 0), (0, 1), (-1, 0), (0, 0)]
        s = sum(x * y for y in range(1, h) for x in range(1, w) if all(_map[p] == "#" for p in [(x + cp[0], y + cp[1]) for cp in check_points]))
        return s

    def part2(self, data):
        _map = self.get_map(data)
        path = self.get_path(_map)
        _, main, functions = self.extract_path_pattern(path)

        movements = [",".join(main)] + [",".join(f) for f in functions] + ["n"]
        movement_insts = [ord(c) for movement in movements for c in movement + "\n"]

        amp = Amp(data[0])
        amp.insts[0] = 2
        amp.inputs = movement_insts

        outputs = []
        while not amp.is_halt():
            amp.set_status_running()
            output = [*amp.run()]
            outputs.extend(output)

        # for i in o[:-1]:
        #     print(chr(i), end="")

        return outputs[-1]

    def get_map(self, data):
        amp = Amp(data[0])

        _map = defaultdict(str)
        y = 0
        x = 0

        while not amp.is_halt():
            amp.set_status_running()
            outputs = [*amp.run()]
            if len(outputs):
                c = chr(int(outputs[0]))

                if outputs[0] == 10:
                    y += 1
                    x = 0
                else:
                    _map[(x, y)] = c
                    x += 1

        return _map

    def get_path(self, _map):
        pos = [k for k, v in _map.items() if v in "^v<>"][0]
        facing = "^>v<".index(_map[pos])

        adjs_rel_coords = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        path = []
        steps = 0

        while 1:
            adjs = [(pos[0] + d[0], pos[1] + d[1]) for d in adjs_rel_coords]
            left = (facing + 3) % 4
            right = (facing + 1) % 4

            if _map[adjs[facing]] == "#":
                steps += 1
                pos = adjs[facing]
            elif _map[adjs[left]] == "#":
                facing = left
                if steps > 0:
                    path += [str(steps)]
                path += ["L"]
                steps = 0
            elif _map[adjs[right]] == "#":
                facing = right
                if steps > 0:
                    path += [str(steps)]
                path += ["R"]
                steps = 0
            else:
                if steps > 0:
                    path += [str(steps)]
                break
        return path

    def extract_path_pattern(self, path, main=[], functions=[]):
        max_length = 20

        while 1:
            count = 0
            for idx, func in enumerate(functions):
                if path[: len(func)] == func:
                    main += [idx]
                    path = path[len(func) :]
                    count += 1
            if count == 0:
                break

        if len(functions) == 3:
            return (False, None, None) if len(path) else (True, ["ABC"[i] for i in main], functions)

        func = path[: max_length // 2]
        while len(",".join(func)) > max_length:
            func = func[:-2]

        while len(func):
            res, res_main, res_funcs = self.extract_path_pattern(path, [] + main, functions + [func])
            if res:
                return (res, res_main, res_funcs)
            else:
                func = func[:-2]
        return (False, None, None)
