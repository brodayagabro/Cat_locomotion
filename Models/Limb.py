from .Network import NeuralNetwork
from .Muscule import Muscule, Angles
import numpy as np

class Limb(NeuralNetwork, Muscule, Angles):
  def __init__(self, l, a, b, layer0, layer1, layer2):
    self.a = a
    self.b = b
    self.length = l
    Muscule.__init__(self, a, b)
    Angles.__init__(self, a, b)
    NeuralNetwork.__init__(self, layer0, layer1, layer2)
