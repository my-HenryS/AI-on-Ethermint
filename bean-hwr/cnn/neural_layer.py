from .layer import Layer
from .neuron import Neuron
import numpy as np
import cnn.utils as u
import os


class NeuralLayer(Layer):

    ##n.weight n.b should be initialized
    def __init__(self, input_size, k, u_type='adam', a_type='relu'):
        self.neurons = []
        self.forward_result = None
        self.k = k

        self.u_type = u_type
        self.a_type = a_type

        if isinstance(input_size, tuple):
            input_size = np.prod(input_size)

        for n in range(k):
            self.neurons.append(Neuron(input_size))

    def predict(self, batch):
        if batch.ndim > 2:
            batch = batch.transpose(0,2,3,1).reshape(-1,batch.shape[0])

        forward_result = []
        for n in self.neurons:
            if self.activation:
                if self.a_type == 'relu':
                    forward_result.append(u.relu(n.strength(batch)))
                elif self.a_type == 'sigmoid':
                    forward_result.append(u.sigmoid(n.strength(batch)))
            else:
                forward_result.append(n.strength(batch))

        self.forward_result = np.array(forward_result)

        #np.savetxt(os.path.dirname(__file__) + "/output_" + str(self.k) + ".txt", self.forward_result, "%s")
        return self.forward_result

    def output_size(self):
        if self.forward_result:
            return self.forward_result.shape[1:]
        else:
            return self.k

    def set_weights(self, weights):
        for n in range(self.k):
            self.neurons[n].weights = weights[:,n]
        return

    def set_biases(self, biases):
        for n in range(self.k):
            self.neurons[n].bias = biases[n]
        return

