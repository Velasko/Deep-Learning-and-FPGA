from nmigen import *
from nmigen.cli import main

# python3 test.py simulate -c 10 -v test.vcd

class Mod1(Elaboratable):
    def __init__(self):
        self.s1 = Signal()

    def elaborate(self, platform):
        m = Module() #all operation on signals must be done in a module

        #s1 = Signal()
        s2 = Signal()
        s3 = Signal()
        #r1 = Record([("r", 1), ("g", 1), ("b", 1)])

        m.d.comb += s2.eq(s3) #s2 change when s3 change
        m.d.sync += s3.eq(~s3)  #s3 change on every clock tick

        # equaivalent to m.d.comb += s1.eq(s3)
        #with m.If(s3):
        #    m.d.comb += s1.eq(1)
        #with m.Else():
        #    m.d.comb += s1.eq(0)

        return m

if __name__ == "__main__":
    top = Mod1()
    main(top, ports=(top.s1))
