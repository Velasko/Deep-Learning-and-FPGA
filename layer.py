from nmigen import *
from nmigen.cli import main

from .perceptron import Perceptron

from .settings import WIDTH

class Layer(Elaboratable):
	def __init__(self, weight_matrix, limits=None, n_bits=WIDTH):
		if limits is None:
			limits = [0.5 for _ in weight_matrix[0]]

		# size limites = column ammount in weight_matrix

		self.perceptrons = [Perceptron(*line, lim=limits[n], n_bits=n_bits) for n, line in enumerate(weight_matrix)]

		self.input = [Signal(n_bits) for _ in weight_matrix[0][:-1]]

		self.output = []
		self.raw = []
		for _ in weight_matrix:
			self.output.append(Signal(n_bits))
			self.raw.append(Signal(n_bits))

	def __getitem__(self, index):
		return self.perceptrons[index].out

	def __call__(self, index):
		return self.perceptrons[index].raw

	def __iter__(self, *args, **kwargs):
		return self.perceptrons.__iter__(*args, **kwargs)

	def elaborate(self, platform):
		m = Module()
		m.submodules += self.perceptrons

		for n, port in enumerate(self.input):
			for per in self.perceptrons:
				m.d.comb += per[n].eq( port )

		for n, per in enumerate(self.perceptrons):
			m.d.comb += self.output[n].eq( per.out )
			m.d.comb += self.raw[n].eq( per.raw )

		return m