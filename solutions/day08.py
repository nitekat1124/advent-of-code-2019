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
        w = 25
        h = 6
        layers = [data[0][i : i + w * h] for i in range(0, len(data[0]), w * h)]
        zeros = [i.count("0") for i in layers]
        idx = zeros.index(min(zeros))
        return layers[idx].count("1") * layers[idx].count("2")

    def part2(self, data):
        w = 25
        h = 6
        layers = [data[0][i : i + w * h] for i in range(0, len(data[0]), w * h)]
        for y in range(h):
            for x in range(w):
                p = [layer[y * 25 + x] for layer in layers]
                p = " #"[int([i for i in p if i != "2"][0])]
                print(p, end="")
            print()
