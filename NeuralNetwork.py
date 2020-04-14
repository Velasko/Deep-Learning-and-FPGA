from nmigen import *
from nmigen.cli import main

from .layer import Layer

from .settings import WIDTH

class NeuralNetwork(Elaboratable):
	"""
		attributes:
		 - layers : list with each layer
		 - input : list of signals which will be connected to the first layer
		 - output : list of signals which will be connected to the output perceptrons
 		 - output : list of signals which will be connected to the raw output perceptrons
	"""
	def __init__(self, layers, limits=None, n_bits=WIDTH, use_raw=False):
		""" - layers: matrice which is passed to each layer of the AI
			- limits: matrix on which each line is passed to the coresponding layer
			- n_bits: int representing the ammount of bits to be used
			- use_raw: if the float value is passed (instead of the boolean) to the next layer
		"""
		if limits is None:
			limits = [None]*len(layers)

		self.layers = [Layer(matrix, limits=limits[n], n_bits=n_bits) for n, matrix in enumerate(layers)]

		for n, layer in enumerate(self.layers[1:]):
			#n will take the previous layer due the [1:], which skips the first item
			if len(self.layers[n].output) != len(layer.input):
				raise Exception("(must change the type of error) Incoerence between the layer matrix")

		self.input = [Signal(n_bits) for _ in layers[0]]
		self.output = [Signal(n_bits) for _ in layers[-1]]
		self.raw = [Signal(n_bits) for _ in layers[-1]]

		self.use_raw = use_raw

	def __getitem__(self, index):
		return self.layers[index]

	def __iter__(self, *args, **kwargs):
		return self.layers.__iter__(*args, **kwargs)

	def __eq__(self, other):
		if not isinstance(other, NeuralNetwork):
			return False
		return all([other.layers[n] == layer for n, layer in enumerate(self)])

	def elaborate(self, platform):
		m = Module()
		m.submodules += self.layers

		#to connect each layer
		for n, layer in enumerate(self.layers[1:]):
			#n will take the previous layer due the [1:], which skips the first item

			connection = self.layers[n].output
			if self.use_raw:
				self.layers[n].raw

			for pos, wire in enumerate(connection):
				m.d.comb += wire.eq(layer[pos])

		#conecting the first layer to the module input
		for perceptron in self.layers[0]:
			for n, inp in enumerate(self.input):
				m.d.comb += perceptron[n].eq(inp)

		#conecting the last layer to the module output
		for n, perceptron in enumerate(self.layers[-1]):
			m.d.comb += self.output[n].eq(perceptron)

		return m
