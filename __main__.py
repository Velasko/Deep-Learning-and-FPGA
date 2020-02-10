from nmigen import *
from nmigen.cli import main

# python3 test.py simulate -c 10 -v test.vcd
from .perceptron import Perceptron

from .settings import *

class Main(Elaboratable):
    def __init__(self):
        self.s1 = Signal(WIDTH)
        self.s2 = Signal(WIDTH)
        self.ret = Signal(WIDTH)

    def elaborate(self, platform):
        m = Module()

        m.submodules.per = Perceptron(ONE, ONE, 0)
        # or anonymous submodules
        # m.submodules += Mod1(2)

        m.d.sync += self.s1.eq( self.s1 + ONE )
        m.d.sync += self.s2.eq( self.s2 + ONE )

        m.d.comb += [
            m.submodules.per[0].eq(self.s1),
            m.submodules.per[1].eq(self.s2),
            self.ret.eq(m.submodules.per.o),
        ]

        return m

if __name__ == "__main__":
    top = Main()
    main(top)
