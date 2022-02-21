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
        # cards = [*range(deck_size)]
        # for inst in data:
        #     if "increment" in inst:
        #         inc = int(inst.split()[-1])
        #         cards = self.increment(cards, inc)
        #     elif "cut" in inst:
        #         cut = int(inst.split()[-1])
        #         cards = cards[cut:] + cards[:cut]
        #     else:
        #         cards = cards[::-1]
        # return cards.index(target)

        target = 2019
        deck_size = 10007
        for inst in data:
            if "increment" in inst:
                inc = int(inst.split()[-1])
                target = (target * inc) % deck_size
            elif "cut" in inst:
                cut = int(inst.split()[-1])
                # if cut < 0:
                #     cut = leng + cut
                # if cut > target:
                #     target = leng - (cut - target)
                # else:
                #     target = target - cut
                target = (target - cut) % deck_size
            else:
                target = deck_size - 1 - target
        return target

    def part2(self, data):
        """
        I failed on this one :'(
        implement the code after look at this ref:
        https://www.reddit.com/r/adventofcode/comments/ee0rqi/comment/fbnkaju/
        """

        target = 2020
        deck_size = 119315717514047
        iterations = 101741582076661

        offset, increment = 0, 1

        for inst in data:
            if inst.startswith("deal with increment"):
                n = int(inst.split()[-1])
                increment *= pow(n, deck_size - 2, deck_size)
            elif inst.startswith("cut"):
                n = int(inst.split()[-1])
                offset += n * increment
            else:  # deal into new stack
                increment *= -1
                offset += increment

        increments = pow(increment, iterations, deck_size)
        offsets = offset * (1 - pow(increment, iterations, deck_size)) * pow(1 - increment, deck_size - 2, deck_size)

        return (target * increments + offsets) % deck_size

    def increment(self, cards, inc):
        deck = {}
        _max = len(cards)
        idx = 0
        while cards:
            card = cards.pop(0)
            deck[idx] = card
            idx = (idx + inc) % _max
        return [deck[i] for i in range(_max)]
