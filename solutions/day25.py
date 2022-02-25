from collections import deque
from itertools import combinations
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

    def part1_not_programmatically(self, data):
        buffer = ""
        printed = ""
        commands = ["west", "south", "take polygon", "north", "east", "north", "west", "take boulder", "east", "north", "take manifold", "west", "south", "east", "south", "take fixed point", "north", "west", "north", "north", "east", "east", "north"]

        _input = input("1) Automatically\n2) Manually\n> ")
        auto = True if _input.strip() == "1" else False

        amp = Amp(data[0])

        while not amp.is_halt():
            if printed == "Command?":
                if auto:
                    if len(commands) == 0:
                        command = input()
                    else:
                        command = commands.pop(0)
                        print(command)
                else:
                    command = input()
                amp.inputs = [ord(c) for c in command + "\n"]
            amp.set_status_running()
            out = [*amp.run()]
            for c in out:
                if c == 10:
                    printed = buffer
                    buffer = ""
                else:
                    buffer += chr(c)
                print(chr(c), end="")

        if printed.find("typing") > -1:
            temp = printed.split()
            print()
            return temp[temp.index("typing") + 1]

    def part1(self, data):
        opp_path = {"north": "south", "south": "north", "east": "west", "west": "east"}
        danger_items = set()

        while 1:
            print("restart game\n\n")

            buffer = ""
            printed = ""

            rooms = {}
            curr_room = None
            inv_items = []

            status_ready_to_collect_item = False
            status_ready_to_scan_doors = False
            status_ready_to_test_weight = False

            available_items = []
            wait_update = []
            path_history = []

            target_room = None
            path_commands = None
            item_combinations = None
            test_combination = None

            amp = Amp(data[0])

            while not amp.is_halt():
                if any(i in printed for i in ["You can't move!!", "You take the infinite loop."]):
                    break

                if printed.startswith("==") and printed.endswith("=="):
                    curr_room = " ".join(printed.split()[1:-1])
                    if curr_room not in rooms:
                        rooms[curr_room] = {"doors": {}}
                        if wait_update:
                            prev_room, prev_room_door = wait_update
                            rooms[prev_room]["doors"][prev_room_door] = curr_room
                            rooms[curr_room]["doors"][opp_path[prev_room_door]] = prev_room
                            wait_update = []

                elif printed == "Doors here lead:":
                    status_ready_to_scan_doors = True
                elif status_ready_to_scan_doors:
                    if printed == "":
                        status_ready_to_scan_doors = False
                    else:
                        direction = printed.split()[1]
                        if direction not in rooms[curr_room]["doors"]:
                            rooms[curr_room]["doors"][direction] = None

                elif printed == "Items here:":
                    status_ready_to_collect_item = True
                elif status_ready_to_collect_item:
                    if printed == "":
                        status_ready_to_collect_item = False
                    else:
                        item = printed.split(" ", 1)[1]
                        if item not in danger_items:
                            available_items += [item]

                elif printed == "Command?":

                    if status_ready_to_test_weight and curr_room == target_room[0]:
                        """
                        test every combination of items
                        """
                        if test_combination is None:
                            drops = set(inv_items) - set(item_combinations[0])
                            if drops:
                                item = list(drops)[0]
                                inv_items.remove(item)
                                command = f"drop {item}"
                            else:
                                test_combination = item_combinations.pop(0)
                                continue
                        else:
                            takes = set(test_combination) - set(inv_items)
                            if takes:
                                item = list(takes)[0]
                                inv_items += [item]
                                command = f"take {item}"
                            else:
                                test_combination = None
                                command = target_room[1]

                    elif status_ready_to_test_weight:
                        command = path_commands.pop(0)
                    else:
                        if available_items:
                            item = available_items.pop(0)
                            inv_items += [item]
                            command = f"take {item}"
                        else:
                            not_visited_rooms = sum(1 for r in rooms if None in rooms[r]["doors"].values())
                            if not_visited_rooms == 0:
                                """
                                1. set status to ready to test
                                2. find routes to go to the room before Pressure-Sensitive Floor
                                3. find cominations of items
                                4. test every combinations of items
                                """
                                status_ready_to_test_weight = True
                                target_room = self.find_target(rooms)
                                path_commands = self.find_path(rooms, curr_room, target_room[0])
                                item_combinations = self.get_items_combs(inv_items)

                                command = path_commands.pop(0)
                            else:
                                not_visit = [i for i, v in rooms[curr_room]["doors"].items() if v is None]
                                if not_visit:
                                    wait_update = [curr_room, not_visit[0]]
                                    path_history += [not_visit[0]]
                                    command = not_visit[0]
                                else:
                                    path = path_history[-1]
                                    path_history = path_history[:-1]
                                    command = opp_path[path]
                    amp.inputs = [ord(c) for c in command + "\n"]
                    print(command)
                amp.set_status_running()
                out = [*amp.run()]
                for c in out:
                    if c == 10:
                        printed = buffer
                        buffer = ""
                    else:
                        buffer += chr(c)
                    print(chr(c), end="")

            if printed.find("typing") > -1:
                temp = printed.split()
                print()
                return temp[temp.index("typing") + 1]
            else:
                danger_items.add(inv_items[-1])

    def part2(self, data):
        return "Merry Christmas!"

    def find_target(self, rooms):
        target = [r for r in rooms if "Pressure-Sensitive Floor" in rooms[r]["doors"].values()][0]
        direction = [k for k, v in rooms[target]["doors"].items() if v == "Pressure-Sensitive Floor"][0]
        return target, direction

    def find_path(self, rooms, curr_room, target):
        start = (curr_room, [])
        queue = deque([start])
        visited = set()
        while queue:
            curr_room, path = queue.popleft()
            if curr_room == target:
                return path
            visited.add(curr_room)
            for direction, next_room in rooms[curr_room]["doors"].items():
                if next_room not in visited:
                    queue.append((next_room, path + [direction]))

    def get_items_combs(self, picked_item):
        items_combs = []
        for i in range(1, len(picked_item) + 1):
            for comb in combinations(picked_item, i):
                items_combs += [list(comb)]
        return items_combs
