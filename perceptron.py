from nmigen import *
from nmigen.cli import main

#python3 perceptron.py simulate -c 10 -v test.vcd

from .settings import OFFSET, WIDTH 

class Perceptron(Elaboratable):
    """
    A single neurone which does a linear combination between the inputs
    X*b + b0.

    X is the collection of ports, which is the input of the perceptron.

    init:
        n_bits : number of bits for each signal. Default: WIDTH variable in settings.
        *b : values of b on which will be multiplied with X. The last one is considered b0.
    """
    def __init__(self, *b, n_bits=WIDTH):
        self.b = b
        self.ports = [Signal(n_bits) for _ in range(len(b) - 1)]
        self.o = Signal(n_bits)

    def __getitem__(self, index):
        return self.ports[index]

    def elaborate(self, platform):
        m = Module()

        for sig in self.ports:
            m.d.comb += self.o.eq( self.b[-1] + (sum([self.b[n] * port for n, port in enumerate(self.ports)]) >> OFFSET) )

        return m

if __name__ == "__main__":
    from settings import one

    top = Perceptron(8, 3*one, 2*one, one, one)
    main(top, ports=[top.ports, top.o])
