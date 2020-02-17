from nmigen import *
from nmigen.cli import main

# python3 -m ML simulate -c 10 -v test.vcd
from .perceptron import Perceptron

from .settings import *

class Main(Elaboratable):
	def __init__(self, b):

		for n, value in enumerate(b):
			b[n] = int(value*ONE)

		self.b = b
		self.s = [Signal(WIDTH) for _ in enumerate(b[:-1])]
		self.ret = Signal(WIDTH)

	def elaborate(self, platform):
		m = Module()

		m.submodules.per = Perceptron(*self.b)
		# or anonymous submodules
		# m.submodules += Mod1(2)	

		x = [4, 4, 5, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2]
		clock = Signal(WIDTH)

		print(dir(clock))

		m.d.sync += clock.eq( clock + ONE )
		m.d.comb += self.s[0].eq( x[clock.signed] )

		m.d.comb += [ m.submodules.per[n].eq( signal ) for n, signal in enumerate(self.s) ]
		m.d.comb += self.ret.eq(m.submodules.per.o)

		return m

if __name__ == "__main__":
	b = [2.32831355e-02, -1.07644595e+00, -1.44067150e-01,  6.57402064e-03, -1.82427840e+00,  3.42047216e-03, -3.42657365e-03, -1.49541411e+01, -2.91748283e-01,  8.72400085e-01,  2.77567469e-01, 18.713908307334766]
	top = Main(b)
	main(top)


