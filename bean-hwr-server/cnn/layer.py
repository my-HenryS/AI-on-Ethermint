from abc import ABCMeta, abstractmethod


class Layer(object):
    __metaclass__ = ABCMeta

    is_output = False
    activation = True
    u_type = 'adam'

    @abstractmethod
    def output_size(self):
        pass

    @abstractmethod
    def predict(self, batch):
        pass

    @abstractmethod
    def set_weights(self, dir):
        pass


