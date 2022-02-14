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
