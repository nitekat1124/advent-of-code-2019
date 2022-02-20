import networkx as nx
from collections import deque
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

    def check_is_raw(self):
        if self.is_raw is False:
            print("please use --raw flag in this puzzle")
            exit()

    def part1(self, data):
        self.check_is_raw()
        portals = self.parse_data(data)
        return self.find_shortest_path(("AA", "outer"), ("ZZ", "outer"), portals)

    def part2(self, data):
        self.check_is_raw()
        portals = self.parse_data(data)
        return self.find_shortest_path_recursive(("AA", "outer"), ("ZZ", "outer"), portals)

    def parse_data(self, data):
        portals = {}
        _map = {}

        dp = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        outer_side = {"x": [2, len(data[0]) - 3], "y": [2, len(data) - 3]}

        for y in range(2, len(data) - 2):
            for x in range(2, len(data[0]) - 2):
                if data[y][x] in ".#":
                    _map[(x, y)] = data[y][x]

                    adjs = [tuple(i + j for i, j in zip((x, y), d)) for d in dp]
                    for idx, adj in enumerate(adjs):
                        if data[adj[1]][adj[0]].isalpha():
                            n0 = data[adj[1]][adj[0]]
                            di = dp[idx]
                            adj2 = tuple(i + j for i, j in zip(adj, di))
                            n1 = data[adj2[1]][adj2[0]]
                            if sum(di) < 0:
                                _name = n1 + n0
                            else:
                                _name = n0 + n1
                            side = "outer" if x in outer_side["x"] or y in outer_side["y"] else "inner"
                            portals[(_name, side)] = {"pos": (x, y), "connect": []}
        return self.find_connects(portals, _map)

    def find_connects(self, portals, _map):
        dp = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        new_portals = {}
        reverse_portals = {v["pos"]: k for k, v in portals.items()}

        for pid, portal in portals.items():
            start = portal["pos"]
            connects = []
            seen = set()
            queue = deque([(start, 0)])
            while queue:
                pos, dist = queue.popleft()
                if pos in seen:
                    continue
                seen.add(pos)
                if pos in reverse_portals and pos != portal["pos"]:
                    connects += [(reverse_portals[pos], dist)]
                else:
                    adjs = [tuple(i + j for i, j in zip(pos, d)) for d in dp]
                    for adj in adjs:
                        if adj in seen or adj not in _map or _map[adj] in " #" or _map[adj].isalpha():
                            continue
                        queue.append((adj, dist + 1))
            new_portals[pid] = {"pos": portal["pos"], "connects": connects}
        return new_portals

    def find_shortest_path(self, start, end, portals):
        g = nx.Graph()
        for pid, portal in portals.items():
            other = ["inner", "outer"][pid[1] == "inner"]
            g.add_edge(pid, (pid[0], other), weight=1)
            for connect in portal["connects"]:
                g.add_edge(pid, connect[0], weight=connect[1])
        return nx.shortest_path_length(g, start, end, weight="weight")

    def find_shortest_path_recursive(self, start, end, portals):
        # guess max levels, may different with others' puzzle input
        levels = 25
        g = nx.Graph()
        for pid, portal in portals.items():
            other, level_direction = [("inner", -1), ("outer", 1)][pid[1] == "inner"]
            for level in range(levels):
                g.add_edge((*pid, level), (pid[0], other, level + level_direction), weight=1)

            for connect in portal["connects"]:
                for level in range(levels + 1):
                    g.add_edge((*pid, level), (*connect[0], level), weight=connect[1])

        return nx.shortest_path_length(g, (*start, 0), (*end, 0), weight="weight")
