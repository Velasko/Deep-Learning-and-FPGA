from nmigen import *
from nmigen.cli import main

from .perceptron import Perceptron

from .settings import WIDTH

class Layer(Elaboratable):
	def __init__(self, weight_matrix, limits=None, n_bits=WIDTH):
		"""
			- weight_matrix : coeficient matrix on which each line is a perceptron
			- limits : list on which will determine the value the perceptron returns 1.
			- n_bits : ammount of bit for each signal inside the layer 
		"""
		if limits is None:
			limits = [0.5 for _ in weight_matrix]

		size = len(weight_matrix[0])
		if any([size != len(line) for line in weight_matrix[1:]]):
			raise Exception("(must change the type of error) Perceptrons with different number of coeficients")

		if len(limits) != len(weight_matrix):
			raise Exception("(must change the type of error) Ammount of limits is different from ammount of perceptrons")

		self.perceptrons = [Perceptron(*line, lim=limits[n], n_bits=n_bits) for n, line in enumerate(weight_matrix)]

		self.input = [Signal(n_bits) for _ in weight_matrix[0][:-1]]

		self.output = []
		self.raw = []
		for _ in weight_matrix:
			self.output.append(Signal(n_bits))
			self.raw.append(Signal(n_bits))

	def __getitem__(self, index):
		return self.output[index]

	def __call__(self, index):
		return self.raw[index]

	def __iter__(self, *args, **kwargs):
		return self.perceptrons.__iter__(*args, **kwargs)

	def __eq__(self, other):
		if not isinstance(other, Layer):
			return False
		return all([other.perceptrons[n] == per for n, per in enumerate(self)])

	def elaborate(self, platform):
		m = Module()

		for n, port in enumerate(self.input):
			for per in self.perceptrons:
				m.d.comb += per[n].eq( port )

		for n, per in enumerate(self.perceptrons):
			m.submodules.__setattr__("perceptron_%d" % (n+1), per)

			m.d.comb += self.output[n].eq( per.out )
			m.d.comb += self.raw[n].eq( per.raw )

		return m