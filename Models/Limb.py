from .Network import NeuralNetwork
from .Muscule import Muscule, Angle


class Limb(NeuralNetwork, Muscule, Angle):
  def __init__(self, a, b, layer0, layer1, layer2):
    Muscule.__init__(self, a, b)
    Angle.__init__(self, a, b)
    NeuralNetwork.__init__(self, layer0, layer1, layer2)
