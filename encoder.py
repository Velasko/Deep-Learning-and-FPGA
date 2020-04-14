import json

from .settings import OFFSET, WIDTH, ONE

from .NeuralNetwork import NeuralNetwork
from .layer import Layer
from .perceptron import Perceptron

class MyEncoder(json.JSONEncoder):
	def default(self, o):
		if o.__class__ == Perceptron:
			return {'__{}__'.format(o.__class__.__name__) : {
						'b' : o.b,
						'lim' : o.lim/ONE
						}
					}

		elif o.__class__ == Layer:
			perceptrons = [self.default(perceptron) for perceptron in o.perceptrons]

			weight_matrix = []
			limits = []
			for jper in perceptrons:
				per = jper['__Perceptron__']
				weight_matrix.append(per['b'])
				limits.append(per['lim'])


			return {'__{}__'.format(o.__class__.__name__) : {
						'weight_matrix' : weight_matrix,
						'limits' : limits
						}
					}

		elif o.__class__ == NeuralNetwork:
			layers = [self.default(layer) for layer in o.layers]

			jlayers = []
			limits = []
			for jlayer in layers:
				layer = jlayer['__Layer__']
				jlayers.append(layer['weight_matrix'])
				limits.append(layer['limits'])


			return {'__{}__'.format(o.__class__.__name__) : {
						'layers' : jlayers,
						'limits' : limits,
						'use_raw' : o.use_raw
						}
					}

	def decode_object(o):
		if '__Perceptron__' in o:
			per = o['__Perceptron__']
			p = Perceptron(*per['b'], lim=per['lim'])

			return p

		if '__Layer__' in o:
			layer = o['__Layer__']
			l = Layer(layer['weight_matrix'], limits=layer['limits'] )

			return l

		if '__NeuralNetwork__' in o:
			N = o['__NeuralNetwork__']
			NN = NeuralNetwork(N['layers'], limits=N['limits'], use_raw=N['use_raw'])

			return NN

		return o

if __name__ == '__main__':
	one = ONE
	x = NeuralNetwork([[[1, 2, 3], [2, 3, 4], [1, 1, 1]], [[2, 2, 2, 2], [3, 3, 3, 3]]], limits=[[1, 1, 2], [1, 2]])

	y = json.dumps(x, cls=MyEncoder, indent=4)
	print(y)

	z = json.loads(y, object_hook=MyEncoder.decode_object)

	print(x == z)