

class Component(object):
    def __init__(self):
        self.sprite = ' '


class CPUError(Exception):
    def __init__(self, args):
        self.args = args

    def __str__(self):
        return repr(self.args)


class CPU(Component):
    def __init__(self, ramsize):
        self.data = [0] * ramsize
        self.pc = 0

    def read(self, addr):
        if not isinstance(addr, int):
            raise CPUError("Address must be set to an integer.")

        return self.data[addr % len(self.data)]

    def write(self, addr, val):
        if not isinstance(addr, int) or not isinstance(val, int):
            raise CPUError("Arguments must be integers.")

        self.data[addr % len(self.data)] = val
