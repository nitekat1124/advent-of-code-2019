from collections import deque
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
        _map, oxygen = self.get_map(data)
        # self.draw_map(_map)

        start = (0, 0)
        end = oxygen
        d = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        seen = set()
        queue = deque([(start, 0)])

        while queue:
            pos, steps = queue.popleft()
            seen.add(pos)
            nexts = [(pos[0] + i[0], pos[1] + i[1]) for i in d]
            for next_pos in nexts:
                if next_pos == end:
                    return steps + 1
                if next_pos not in seen and _map[next_pos] == 1:
                    queue.append((next_pos, steps + 1))

    def part2(self, data):
        _map, _ = self.get_map(data)
        d = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        t = 0

        while 1:
            Os = [k for k, v in _map.items() if v == 2]
            for o in Os:
                neighbors = [(o[0] + i[0], o[1] + i[1]) for i in d]
                for p in neighbors:
                    if p in _map and _map[p] == 1:
                        _map[p] = 2
            t += 1
            if len([k for k, v in _map.items() if v == 1]) == 0:
                break

        return t

    def get_map(self, data):
        start = (0, 0)
        pos = (0, 0)
        _map = {pos: (1, 0)}
        facing = 0

        directions = {
            # north
            1: (0, -1),
            # south
            2: (0, 1),
            # west
            3: (-1, 0),
            # east
            4: (1, 0),
        }
        rel_dir = [
            # when facing north
            {"left": 3, "front": 1, "right": 4},
            # when facing east
            {"left": 1, "front": 4, "right": 2},
            # when facing south
            {"left": 4, "front": 2, "right": 3},
            # when facing west
            {"left": 2, "front": 3, "right": 1},
        ]

        amp = Amp(data[0], 0)
        amp.inputs = []
        oxygen_found = False

        while 1:

            # check left
            amp.inputs += [rel_dir[facing]["left"]]
            amp.set_status_running()
            lft = [*amp.run()][-1]

            next_pos = tuple(i + j for i, j in zip(pos, directions[rel_dir[facing]["left"]]))
            _map[next_pos] = lft
            if lft == 0:
                # print("left is wall, looking front")
                # check front
                amp.inputs += [rel_dir[facing]["front"]]
                amp.set_status_running()
                frnt = [*amp.run()][-1]

                next_pos = tuple(i + j for i, j in zip(pos, directions[rel_dir[facing]["front"]]))
                _map[next_pos] = frnt
                if frnt == 0:
                    # print("front is wall, looking right")
                    # check right
                    amp.inputs += [rel_dir[facing]["right"]]
                    amp.set_status_running()
                    rght = [*amp.run()][-1]

                    next_pos = tuple(i + j for i, j in zip(pos, directions[rel_dir[facing]["right"]]))
                    _map[next_pos] = rght
                    if rght == 0:
                        # print("right is wall, turn back")
                        # turn back
                        facing = (facing + 2) % 4
                    else:
                        if rght == 2:
                            # print("meet oxygen at right")
                            oxygen_found = next_pos
                        # else:
                        #     print("right have room, turn right and go")
                        facing = (facing + 1) % 4
                        pos = next_pos
                else:
                    if frnt == 2:
                        # print("meet oxygen at front")
                        oxygen_found = next_pos
                    # else:
                    #     print("front have room, still front and go")
                    # facing not change
                    pos = next_pos
            else:
                if lft == 2:
                    # print("meet oxygen at left")
                    oxygen_found = next_pos
                # else:
                #     print("left have room, turn left and go")
                facing = (facing + 3) % 4
                pos = next_pos

            if pos == start and oxygen_found:
                # print("after found oxygen, return to start position")
                break

        return _map, oxygen_found

    def draw_map(self, _map):
        coords = [*_map.keys()]
        min_x = min(coords, key=lambda x: x[0])[0]
        max_x = max(coords, key=lambda x: x[0])[0]
        min_y = min(coords, key=lambda x: x[1])[1]
        max_y = max(coords, key=lambda x: x[1])[1]

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, y) == (0, 0):
                    print("S", end="")
                elif (x, y) in _map:
                    print("#.O"[_map[(x, y)]], end="")
                else:
                    print("?", end="")
            print()
