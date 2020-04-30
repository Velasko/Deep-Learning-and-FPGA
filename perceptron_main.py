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
		self.correct = Signal(WIDTH)
		self.total = Signal(WIDTH)

	def elaborate(self, platform):
		m = Module()

		m.submodules.per = Perceptron(*self.b)
		# or anonymous submodules
		# m.submodules += Mod1(2)	

		m.d.comb += [ m.submodules.per[n].eq( signal ) for n, signal in enumerate(self.s) ]
		m.d.comb += self.ret.eq(m.submodules.per.raw)


		#[source for creating testbench] http://blog.lambdaconcept.com/doku.php?id=nmigen:nmigen_sim_testbench_sync

		#If we got the value in the corresponding range
		# accuracy <- round(predict) == real
		m.d.comb += self.accuracy.eq( ((self.ret >> OFFSET) + self.ret[15])*ONE == self.real )

		# if accuracy:
		# 	correct += 1
		with m.If(self.accuracy):
			m.d.sync += self.correct.eq( self.correct + ONE )
		#by knowing the total and how many we got correct,
		#it's easy to know the % of what we got right
		m.d.sync += self.total.eq( self.total + ONE )

		return m

if __name__ == "__main__":
	#b is the liniar coeficients used on the linear regression and will be passed to the perceptron
	b = [2.32831355e-02, -1.07644595e+00, -1.44067150e-01,  6.57402064e-03, -1.82427840e+00,  3.42047216e-03, -3.42657365e-03, -1.49541411e+01, -2.91748283e-01,  8.72400085e-01,  2.77567469e-01, 18.713908307334766]
	top = Main(b)
#	main(top)
	
	#opening dataset to get the data for the test
	with open("./ML/data/wine.pickle", 'rb') as file:
		wine_data = pickle.load(file)

	#starting simulation
	wine_data = [0]*len(wine_data[1]) + wine_data
	with Simulator(top, vcd_file=open("test.vcd", "w")) as sim:
		def process():
			#we want to execute for each line of the test
			for line in wine_data[-200:]:
				#so we add the input of each row to the correct signal on the board
				for n, data in enumerate(line[:-1]):
					yield top.s[n].eq( int(data*ONE) )

				#we put the test output so the board can verify and
				#it's easier to check on the simulation
				#how many we got right
				yield top.real.eq( int(line[-1]*ONE) )
				yield Tick()

		# Add a clock to our design
		sim.add_clock(1e-6)
		# Add 'process' as a testbench process
		sim.add_sync_process(process)
		# Run the simulation
		sim.run()