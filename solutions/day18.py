import heapq
from collections import defaultdict, deque
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
        _map = self.parse_map(data)
        nears = self.find_nearests_keys_for_key(_map)

        keys_count = sum(1 for i in _map if _map[i].isalpha() and _map[i].islower())

        seen = set()
        queue = [(0, "@", tuple())]  # total_distances, curr_bot_location, collected_keys

        while queue:
            # queue = deque(sorted(queue))
            # dist, curr, keys = queue.popleft()
            dist, curr, keys = heapq.heappop(queue)

            if (curr, keys) in seen:
                continue
            if len(keys) == keys_count:
                return dist

            seen.add((curr, keys))

            keys = set(keys)

            for next_key, next_vals in nears[curr].items():
                if len(next_vals["req_keys"] - keys) == 0:
                    # queue.append((dist + next_vals["dist"], next_key, tuple(sorted(list(keys | {next_key})))))
                    heapq.heappush(queue, (dist + next_vals["dist"], next_key, tuple(sorted(list(keys | {next_key})))))

    def part2(self, data):
        ep = [k for k, v in self.parse_map(data).items() if v == "@"][0]
        data[ep[1] - 1] = data[ep[1] - 1][: ep[0] - 1] + "@#@" + data[ep[1] - 1][ep[0] + 2 :]
        data[ep[1]] = data[ep[1]][: ep[0] - 1] + "###" + data[ep[1]][ep[0] + 2 :]
        data[ep[1] + 1] = data[ep[1] + 1][: ep[0] - 1] + "@#@" + data[ep[1] + 1][ep[0] + 2 :]
        _map = self.parse_map(data)

        _map[(ep[0] - 1, ep[1] - 1)] = "@1"
        _map[(ep[0] + 1, ep[1] - 1)] = "@2"
        _map[(ep[0] - 1, ep[1] + 1)] = "@3"
        _map[(ep[0] + 1, ep[1] + 1)] = "@4"

        nears = self.find_nearests_keys_for_key(_map)

        keys_count = sum(1 for i in _map if _map[i].isalpha() and _map[i].islower())

        seen = set()
        queue = [(0, tuple(["@1", "@2", "@3", "@4"]), tuple())]  # total_distances, curr_bot_location, collected_keys

        while queue:
            dist, curr_bots_locs, keys = heapq.heappop(queue)

            if (curr_bots_locs, keys) in seen:
                continue
            if len(keys) == keys_count:
                return dist

            seen.add((curr_bots_locs, keys))

            keys = set(keys)

            for i, bot in enumerate(curr_bots_locs):
                for next_key, next_vals in nears[bot].items():
                    if len(next_vals["req_keys"] - keys) == 0:
                        robots = list(curr_bots_locs)
                        robots[i] = next_key
                        heapq.heappush(queue, (dist + next_vals["dist"], tuple(robots), tuple(sorted(list(keys | {next_key})))))

    def parse_map(self, data):
        _map = defaultdict(lambda: ".")
        for y, line in enumerate(data):
            for x, c in enumerate(line):
                _map[(x, y)] = c
        return _map

    def find_nearests_keys_for_key(self, _map):
        nearests = {}
        dp = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for pos, c in _map.items():
            if c in ".#" or (c.isalpha() and c.isupper()):
                continue
            pos_near = {}
            seen = set()
            queue = deque([(pos, 0, [])])
            while queue:
                target, dist, doors = queue.popleft()
                if target in seen:
                    continue
                seen.add(target)

                if _map[target].isalpha():
                    if _map[target].isupper():
                        doors = doors + [_map[target]]
                    elif _map[target].islower() and _map[target] != c:
                        pos_near[_map[target]] = {"dist": dist, "req_keys": set(d.lower() for d in doors)}
                        continue

                for next_target in [tuple(i + j for i, j in zip(target, d)) for d in dp]:
                    if next_target not in seen and _map[next_target] != "#":
                        queue.append((next_target, dist + 1, doors))

            nearests[c] = pos_near
        return nearests
