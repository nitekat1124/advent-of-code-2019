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

    def part1(self, data):
        NICs = []
        outputs = []
        for i in range(50):
            NIC = Amp(data[0])
            NIC.inputs += [i]
            NICs += [NIC]
            outputs += [[]]

        while 1:
            for i, NIC in enumerate(NICs):
                # check if has something to send
                wait_to_send = outputs[i]
                if len(wait_to_send) > 2:
                    addr, x, y = wait_to_send[:3]
                    if addr == 255:
                        return y
                    NICs[addr].inputs += [x, y]
                    outputs[i] = wait_to_send[3:]

                # check incoming queue
                if len(NIC.inputs) == 0:
                    NIC.inputs = [-1]

                NIC.set_status_running()
                out = [*NIC.run()]
                outputs[i] += out

    def part2(self, data):
        NAT = None
        send_y = set()

        NICs = []
        outputs = []
        for i in range(50):
            NIC = Amp(data[0])
            NIC.inputs += [i]
            NICs += [NIC]
            outputs += [[]]

        while 1:
            for i, NIC in enumerate(NICs):
                # check if has something to send
                wait_to_send = outputs[i]
                if len(wait_to_send) > 2:
                    addr, x, y = wait_to_send[:3]
                    if addr == 255:
                        NAT = (x, y)
                    else:
                        NICs[addr].inputs += [x, y]
                    outputs[i] = wait_to_send[3:]

                # check incoming queue
                if len(NIC.inputs) == 0:
                    NIC.inputs = [-1]

                NIC.set_status_running()
                out = [*NIC.run()]
                outputs[i] += out

            if sum(len(n.inputs) for n in NICs) == 0 and sum(len(o) for o in outputs) == 0 and NAT is not None:
                x, y = NAT
                NAT = None
                NICs[0].inputs = [x, y]
                if y in send_y:
                    return y
                send_y.add(y)
