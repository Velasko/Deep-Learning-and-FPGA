from nmigen import *
from nmigen.cli import main

from .settings import OFFSET, WIDTH, ONE

class Perceptron(Elaboratable):
	"""
	A single neurone which does a linear combination between the inputs
	X*b + b0.

	X is the collection of ports, which is the input of the perceptron.

	init:
		n_bits : number of bits for each signal. Default: WIDTH variable in settings.
		*b : values of b on which will be multiplied with X. The last one is considered b0.
	"""
	def __init__(self, *b, n_bits=WIDTH, lim=0.5):
		self.lim = int(lim*ONE)
		self.b = b
		self.ports = [Signal(n_bits) for _ in range(len(b) - 1)]
		self.raw = Signal(n_bits)
		self.out = Signal(n_bits)

	def __getitem__(self, index):
		return self.ports[index]

	def __eq__(self, other):
		if not isinstance(other, Perceptron):
			return false
		return (self.b == other.b and self.lim == other.lim)

	def elaborate(self, platform):
		m = Module()

		m.d.comb += self.raw.eq( self.b[-1] + (sum([self.b[n] * port for n, port in enumerate(self.ports)]) >> OFFSET) )
		m.d.comb += self.out[16].eq( self.raw > self.lim )

		return m

if __name__ == "__main__":
	from .settings import ONE as one

	top = Perceptron(8, 3*one, 2*one, one, one)
	main(top, ports=[top.ports, top.o])
