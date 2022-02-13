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
        amp.inputs = [1]
        signals = []
        while 1:
            amp.status = Status.RUNNING
            outputs = [*amp.run()]
            if amp.status == Status.HALT:
                break
            signals += [str(outputs[-1])]
        return ",".join(signals)

    def part2(self, data):
        amp = Amp(data[0], 0)
        amp.inputs = [2]
        signals = []
        while 1:
            amp.status = Status.RUNNING
            outputs = [*amp.run()]
            if amp.status == Status.HALT:
                break
            signals += [str(outputs[-1])]
        return ",".join(signals)


class Status:
    RUNNING = 1
    WAIT = 2
    HALT = 0


class Amp:
    def __init__(self, insts_raw, phase):
        self.insts = [*map(int, insts_raw.split(","))] + [0] * 1000
        self.phase = phase
        self.status = Status.RUNNING
        self.pntr = 0
        self.inputs = [phase]
        self.base = 0

    def run(self):
        while self.status == Status.RUNNING:
            opcode = f"{self.insts[self.pntr]:05}"
            modes = list(opcode[:-2][::-1])
            opcode = int(opcode[-2:])

            if opcode == 1:
                val1 = self.insts[self.insts[self.pntr + 1]] if modes[0] == "0" else self.insts[self.insts[self.pntr + 1] + self.base] if modes[0] == "2" else self.insts[self.pntr + 1]
                val2 = self.insts[self.insts[self.pntr + 2]] if modes[1] == "0" else self.insts[self.insts[self.pntr + 2] + self.base] if modes[1] == "2" else self.insts[self.pntr + 2]
                address = self.insts[self.pntr + 3] if modes[2] == "0" else self.insts[self.pntr + 3] + self.base if modes[2] == "2" else self.pntr + 3
                if address >= 0:
                    self.insts[address] = val1 + val2
                self.pntr += 4
            elif opcode == 2:
                val1 = self.insts[self.insts[self.pntr + 1]] if modes[0] == "0" else self.insts[self.insts[self.pntr + 1] + self.base] if modes[0] == "2" else self.insts[self.pntr + 1]
                val2 = self.insts[self.insts[self.pntr + 2]] if modes[1] == "0" else self.insts[self.insts[self.pntr + 2] + self.base] if modes[1] == "2" else self.insts[self.pntr + 2]
                address = self.insts[self.pntr + 3] if modes[2] == "0" else self.insts[self.pntr + 3] + self.base if modes[2] == "2" else self.pntr + 3
                if address >= 0:
                    self.insts[address] = val1 * val2
                self.pntr += 4
            elif opcode == 3:
                if len(self.inputs):
                    val = self.inputs.pop(0)
                    address = self.insts[self.pntr + 1] if modes[0] == "0" else self.insts[self.pntr + 1] + self.base if modes[0] == "2" else self.pntr + 1
                    if address >= 0:
                        self.insts[address] = val
                    self.pntr += 2
                else:
                    self.status = Status.WAIT
            elif opcode == 4:
                address = self.insts[self.pntr + 1] if modes[0] == "0" else self.insts[self.pntr + 1] + self.base if modes[0] == "2" else self.pntr + 1
                if address >= 0:
                    yield self.insts[address]
                self.pntr += 2
                self.status = Status.WAIT
            elif opcode == 5:
                val1 = self.insts[self.insts[self.pntr + 1]] if modes[0] == "0" else self.insts[self.insts[self.pntr + 1] + self.base] if modes[0] == "2" else self.insts[self.pntr + 1]
                val2 = self.insts[self.insts[self.pntr + 2]] if modes[1] == "0" else self.insts[self.insts[self.pntr + 2] + self.base] if modes[1] == "2" else self.insts[self.pntr + 2]
                if val1 != 0:
                    self.pntr = val2
                else:
                    self.pntr += 3
            elif opcode == 6:
                val1 = self.insts[self.insts[self.pntr + 1]] if modes[0] == "0" else self.insts[self.insts[self.pntr + 1] + self.base] if modes[0] == "2" else self.insts[self.pntr + 1]
                val2 = self.insts[self.insts[self.pntr + 2]] if modes[1] == "0" else self.insts[self.insts[self.pntr + 2] + self.base] if modes[1] == "2" else self.insts[self.pntr + 2]
                if val1 == 0:
                    self.pntr = val2
                else:
                    self.pntr += 3
            elif opcode == 7:
                val1 = self.insts[self.insts[self.pntr + 1]] if modes[0] == "0" else self.insts[self.insts[self.pntr + 1] + self.base] if modes[0] == "2" else self.insts[self.pntr + 1]
                val2 = self.insts[self.insts[self.pntr + 2]] if modes[1] == "0" else self.insts[self.insts[self.pntr + 2] + self.base] if modes[1] == "2" else self.insts[self.pntr + 2]
                address = self.insts[self.pntr + 3] if modes[2] == "0" else self.insts[self.pntr + 3] + self.base if modes[2] == "2" else self.pntr + 3
                if address >= 0:
                    self.insts[address] = 1 if val1 < val2 else 0
                self.pntr += 4
            elif opcode == 8:
                val1 = self.insts[self.insts[self.pntr + 1]] if modes[0] == "0" else self.insts[self.insts[self.pntr + 1] + self.base] if modes[0] == "2" else self.insts[self.pntr + 1]
                val2 = self.insts[self.insts[self.pntr + 2]] if modes[1] == "0" else self.insts[self.insts[self.pntr + 2] + self.base] if modes[1] == "2" else self.insts[self.pntr + 2]
                address = self.insts[self.pntr + 3] if modes[2] == "0" else self.insts[self.pntr + 3] + self.base if modes[2] == "2" else self.pntr + 3
                if address >= 0:
                    self.insts[address] = 1 if val1 == val2 else 0
                self.pntr += 4
            elif opcode == 9:
                val = self.insts[self.insts[self.pntr + 1]] if modes[0] == "0" else self.insts[self.insts[self.pntr + 1] + self.base] if modes[0] == "2" else self.insts[self.pntr + 1]
                self.base += val
                self.pntr += 2
            elif opcode == 99:
                self.status = Status.HALT
                self.pntr += 1
            else:
                raise Exception(f"unknown opcode: {opcode}")
