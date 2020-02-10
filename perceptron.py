from nmigen import *
from nmigen.cli import main

#python3 perceptron.py simulate -c 10 -v test.vcd

offset = 3
one = 2**offset

class Perceptron(Elaboratable):
    def __init__(self, n_bits, *b):
        self.b = b
        self.ports = [Signal(n_bits) for _ in range(len(b) - 1)]
        self.o = Signal(n_bits)

    def elaborate(self, platform):
        m = Module()

        m.d.sync += self.ports[0].eq(self.ports[0] + one)
        m.d.sync += self.ports[1].eq(self.ports[1] + int(0.5*one))
        m.d.sync += self.ports[1].eq(self.ports[1] + int(0.25*one))

        for sig in self.ports:
            m.d.comb += self.o.eq( self.b[-1] + (sum([self.b[n] * port for n, port in enumerate(self.ports)]) >> offset) )

        return m

if __name__ == "__main__":
    top = Perceptron(8, 3*one, 2*one, one, one)
    main(top, ports=[top.ports, top.o])
