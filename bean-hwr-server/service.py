import numpy as np
import os
from cnn.neural_net import NeuralNetwork


def analysis(interact_data):
    path = os.path.dirname(__file__)

    W_fc1 = np.load(path + "/np_weights/W_fc1.npy")
    W_fc2 = np.load(path + "/np_weights/W_fc2.npy")
    W_bfc1 = np.load(path + "/np_weights/W_bfc1.npy")
    W_bfc2 = np.load(path + "/np_weights/W_bfc2.npy")

    cnn = NeuralNetwork(np.shape([1, 1 * 1 * 120]),
                        [
                            {'type': 'fc', 'k': 240},
                            {'type': 'output', 'k': 47}
                        ])

    cnn.layers[0].set_weights(W_fc1)
    cnn.layers[0].set_biases(W_bfc1)
    cnn.layers[1].set_weights(W_fc2)
    cnn.layers[1].set_biases(W_bfc2)

    return cnn.output(interact_data, predict=True)[0]
