from .neural_layer import NeuralLayer
from .conv_layer import ConvLayer
from .pool_layer import PoolLayer
import numpy as np
import cnn.utils

class NeuralNetwork(object):

    def __init__(self, input_shape, layer_list, loss='softmax'):
        self.layers = []

        # dropout
        self.dropout_p = 1
        self.t = 0
        self.loss = loss
        self.result = None

        next_input_size = input_shape
        for l in layer_list:
            if l['type'] == 'conv':
                l.pop('type')
                conv = ConvLayer(next_input_size, **l)
                self.layers.append(conv)
                next_input_size = conv.output_size()

            elif l['type'] == 'pool':
                l.pop('type')
                pool = PoolLayer(next_input_size, **l)
                self.layers.append(pool)
                next_input_size = pool.output_size()

            elif l['type'] == 'fc':
                l.pop('type')
                fc = NeuralLayer(next_input_size, **l)
                self.layers.append(fc)
                next_input_size = fc.output_size()

            elif l['type'] == 'output':
                l.pop('type')
                fc = NeuralLayer(next_input_size, **l)
                fc.is_output = True
                fc.activation = False
                self.layers.append(fc)
                next_input_size = fc.output_size()


    def output(self, batch, predict = False):
        next_input = batch
        for index, layer in enumerate(self.layers):
            next_input = layer.predict(next_input)

            if (self.dropout_p < 1) and (type(layer).__name__ == 'NeuralLayer') and not layer.is_output:
                next_input *= self.dropout_p

        result = next_input
        if predict:
            self.result = np.argmax(result, axis=0)
        else:
            self.result = result
        return self.result

    def toFile(self, dir):
        np.save(dir, self.result)

