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
        insts = [int(i) for i in data[0].split(",")]

        insts[1] = 12
        insts[2] = 2

        insts = self.run(insts)
        return insts[0]

    def part2(self, data):
        for noun in range(100):
            for verb in range(100):
                insts = [int(i) for i in data[0].split(",")]

                insts[1] = noun
                insts[2] = verb

                insts = self.run(insts)
                if insts[0] == 19690720:
                    return 100 * noun + verb

    def run(self, insts):
        pntr = 0
        opcode = insts[pntr]

        RUNNING = 1
        HALT = 0
        status = RUNNING

        while status == RUNNING:
            if opcode == 1:
                insts[insts[pntr + 3]] = insts[insts[pntr + 1]] + insts[insts[pntr + 2]]
                pntr += 4
            elif opcode == 2:
                insts[insts[pntr + 3]] = insts[insts[pntr + 1]] * insts[insts[pntr + 2]]
                pntr += 4
            elif opcode == 99:
                status = HALT
                pntr += 1
            else:
                raise Exception(f"unknown opcode: {opcode}")

            opcode = insts[pntr]
        return insts
