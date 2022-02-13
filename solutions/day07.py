from itertools import permutations
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
        phases_perms = list(permutations([0, 1, 2, 3, 4], 5))
        signals = []

        for phases in phases_perms:
            output = 0
            for phase in phases:
                amp = Amp(data[0], phase)
                amp.inputs += [output]
                outputs = [*amp.run()]
                output = outputs[-1]
            signals += [output]
        return max(signals)

    def part2(self, data):
        phases_perms = list(permutations([5, 6, 7, 8, 9], 5))
        signals = []

        for phases in phases_perms:
            amps = [Amp(data[0], phase) for phase in phases]
            amp_idx = 0
            output = 0
            while 1:
                amps[amp_idx].inputs += [output]
                amps[amp_idx].status = Status.RUNNING
                outputs = [*amps[amp_idx].run()]
                if amps[amp_idx].status == Status.HALT:
                    break
                else:
                    output = outputs[-1]
                    amp_idx = (amp_idx + 1) % 5
            signals += [output]
        return max(signals)


class Status:
    RUNNING = 1
    WAIT = 2
    HALT = 0


class Amp:
    def __init__(self, insts_raw, phase):
        self.insts = [*map(int, insts_raw.split(","))]
        self.phase = phase
        self.status = Status.RUNNING
        self.pntr = 0
        self.inputs = [phase]

    def run(self):
        while self.status == Status.RUNNING:
            opcode = f"{self.insts[self.pntr]:05}"
            modes = list(opcode[:-2][::-1])
            opcode = int(opcode[-2:])

            if opcode == 1:
                val1 = self.insts[self.insts[self.pntr + 1]] if modes[0] == "0" else self.insts[self.pntr + 1]
                val2 = self.insts[self.insts[self.pntr + 2]] if modes[1] == "0" else self.insts[self.pntr + 2]
                self.insts[self.insts[self.pntr + 3]] = val1 + val2
                self.pntr += 4
            elif opcode == 2:
                val1 = self.insts[self.insts[self.pntr + 1]] if modes[0] == "0" else self.insts[self.pntr + 1]
                val2 = self.insts[self.insts[self.pntr + 2]] if modes[1] == "0" else self.insts[self.pntr + 2]
                self.insts[self.insts[self.pntr + 3]] = val1 * val2
                self.pntr += 4
            elif opcode == 3:
                if len(self.inputs):
                    val = self.inputs.pop(0)
                    self.insts[self.insts[self.pntr + 1]] = val
                    self.pntr += 2
                else:
                    self.status = Status.WAIT
            elif opcode == 4:
                yield self.insts[self.insts[self.pntr + 1]]
                self.pntr += 2
                self.status = Status.WAIT
            elif opcode == 5:
                val1 = self.insts[self.insts[self.pntr + 1]] if modes[0] == "0" else self.insts[self.pntr + 1]
                val2 = self.insts[self.insts[self.pntr + 2]] if modes[1] == "0" else self.insts[self.pntr + 2]
                if val1 != 0:
                    self.pntr = val2
                else:
                    self.pntr += 3
            elif opcode == 6:
                val1 = self.insts[self.insts[self.pntr + 1]] if modes[0] == "0" else self.insts[self.pntr + 1]
                val2 = self.insts[self.insts[self.pntr + 2]] if modes[1] == "0" else self.insts[self.pntr + 2]
                if val1 == 0:
                    self.pntr = val2
                else:
                    self.pntr += 3
            elif opcode == 7:
                val1 = self.insts[self.insts[self.pntr + 1]] if modes[0] == "0" else self.insts[self.pntr + 1]
                val2 = self.insts[self.insts[self.pntr + 2]] if modes[1] == "0" else self.insts[self.pntr + 2]
                self.insts[self.insts[self.pntr + 3]] = 1 if val1 < val2 else 0
                self.pntr += 4
            elif opcode == 8:
                val1 = self.insts[self.insts[self.pntr + 1]] if modes[0] == "0" else self.insts[self.pntr + 1]
                val2 = self.insts[self.insts[self.pntr + 2]] if modes[1] == "0" else self.insts[self.pntr + 2]
                self.insts[self.insts[self.pntr + 3]] = 1 if val1 == val2 else 0
                self.pntr += 4
            elif opcode == 99:
                self.status = Status.HALT
                self.pntr += 1
            else:
                raise Exception(f"unknown opcode: {opcode}")
