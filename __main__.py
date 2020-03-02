import pickle

from nmigen import *
from nmigen.cli import main

from nmigen.back.pysim import *

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

		self.real = Signal(WIDTH)

		self.accuracy = Signal()

		self.total = Signal(WIDTH)
		self.correct = Signal(WIDTH)

	def elaborate(self, platform):
		m = Module()

		m.submodules.per = Perceptron(*self.b)
		# or anonymous submodules
		# m.submodules += Mod1(2)	

		#Verify the condition - abs(real - predict) <= 0.5
		m.d.comb += self.accuracy.eq( (self.real - self.ret <= int(0.5*ONE)) )
		m.d.comb += [ m.submodules.per[n].eq( signal ) for n, signal in enumerate(self.s) ]
		m.d.comb += self.ret.eq(m.submodules.per.o)

		m.d.sync += self.total.eq( self.total + ONE )
		with m.If(self.accuracy):
			m.d.sync += self.correct.eq( self.correct + ONE )

		return m

if __name__ == "__main__":
	b = [2.32831355e-02, -1.07644595e+00, -1.44067150e-01,  6.57402064e-03, -1.82427840e+00,  3.42047216e-03, -3.42657365e-03, -1.49541411e+01, -2.91748283e-01,  8.72400085e-01,  2.77567469e-01, 18.713908307334766]
	top = Main(b)
#	main(top)
	with open("./ML/data/wine.pickle", 'rb') as file:
		wine_data = pickle.load(file)

	with Simulator(top, vcd_file=open("test.vcd", "w")) as sim:
		def process():
			for line in wine_data[-200:]:
				for n, data in enumerate(line[:-1]):
					yield top.s[n].eq( int(data*ONE) )
				yield top.real.eq( int(line[-1]*ONE) )
				yield Tick()

		# Add a clock to our design
		sim.add_clock(1e-6)
		# Add 'process' as a testbench process
		sim.add_sync_process(process)
		# Run the simulation
		sim.run()