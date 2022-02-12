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
        self.inputs = [1]
        insts = [int(x) for x in data[0].split(",")]
        output = [*self.run(insts)]
        return output[-1]

    def part2(self, data):
        self.inputs = [5]
        insts = [int(x) for x in data[0].split(",")]
        output = [*self.run(insts)]
        return output[-1]

    def run(self, insts):
        pntr = 0
        opcode = f"{insts[pntr]:05}"
        modes = list(opcode[:-2][::-1])
        opcode = int(opcode[-2:])

        RUNNING = 1
        HALT = 0
        status = RUNNING

        while status == RUNNING:
            if opcode == 1:
                val1 = insts[insts[pntr + 1]] if modes[0] == "0" else insts[pntr + 1]
                val2 = insts[insts[pntr + 2]] if modes[1] == "0" else insts[pntr + 2]
                insts[insts[pntr + 3]] = val1 + val2
                pntr += 4
            elif opcode == 2:
                val1 = insts[insts[pntr + 1]] if modes[0] == "0" else insts[pntr + 1]
                val2 = insts[insts[pntr + 2]] if modes[1] == "0" else insts[pntr + 2]
                insts[insts[pntr + 3]] = val1 * val2
                pntr += 4
            elif opcode == 3:
                val = self.inputs.pop(0)
                insts[insts[pntr + 1]] = val
                pntr += 2
            elif opcode == 4:
                yield insts[insts[pntr + 1]]
                pntr += 2
            elif opcode == 5:
                val1 = insts[insts[pntr + 1]] if modes[0] == "0" else insts[pntr + 1]
                val2 = insts[insts[pntr + 2]] if modes[1] == "0" else insts[pntr + 2]
                if val1 != 0:
                    pntr = val2
                else:
                    pntr += 3
            elif opcode == 6:
                val1 = insts[insts[pntr + 1]] if modes[0] == "0" else insts[pntr + 1]
                val2 = insts[insts[pntr + 2]] if modes[1] == "0" else insts[pntr + 2]
                if val1 == 0:
                    pntr = val2
                else:
                    pntr += 3
            elif opcode == 7:
                val1 = insts[insts[pntr + 1]] if modes[0] == "0" else insts[pntr + 1]
                val2 = insts[insts[pntr + 2]] if modes[1] == "0" else insts[pntr + 2]
                insts[insts[pntr + 3]] = 1 if val1 < val2 else 0
                pntr += 4
            elif opcode == 8:
                val1 = insts[insts[pntr + 1]] if modes[0] == "0" else insts[pntr + 1]
                val2 = insts[insts[pntr + 2]] if modes[1] == "0" else insts[pntr + 2]
                insts[insts[pntr + 3]] = 1 if val1 == val2 else 0
                pntr += 4
            elif opcode == 99:
                status = HALT
                pntr += 1
            else:
                raise Exception(f"unknown opcode: {opcode}")

            opcode = f"{insts[pntr]:05}"
            modes = list(opcode[:-2][::-1])
            opcode = int(opcode[-2:])
