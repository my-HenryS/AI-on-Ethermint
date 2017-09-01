import numpy as np
from .neural_layer import NeuralLayer
import cnn.utils as u
import os


class ConvLayer(NeuralLayer):
    ##n.weight n.b should be initialized
    def __init__(self, input_size, k, f=3, s=1, p=1, u_type='adam', a_type='relu'):
        self.image_size = 0
        self.w = input_size[2]
        self.h = input_size[1]
        self.d = input_size[0]

        self.k = k
        self.f = f
        self.s = s
        self.p = p

        self.w2 = int((self.w - self.f + 2 * self.p) / self.s + 1)
        self.h2 = int((self.h - self.f + 2 * self.p) / self.s + 1)
        self.d2 = k

        super(ConvLayer, self).__init__(f*f*self.d, k, u_type=u_type, a_type=a_type)

    def predict(self, batch):
        cols = u.im2col_indices(batch, self.f, self.f, self.p, self.s)
        sum_weights = []
        for n in self.neurons:
            n.last_input = cols
            sum_weights.append(n.weights)

        sum_weights = np.array(sum_weights)
        strength = sum_weights.dot(cols).reshape(self.k, self.h2, self.w2, -1).transpose(3, 0, 1, 2)

        if self.activation:
            if self.a_type == 'sigmoid':
                return u.sigmoid(strength)
            else:
                #result = u.relu(strength)
                #result = result.transpose(0,2,3,1)
                #np.savetxt(os.path.dirname(__file__)+"//output_"+str(self.k)+".txt",result,"%s")
                return u.relu(strength)
        else:
            return strength

    def output_size(self):
        return (self.d2, self.h2, self.w2)

