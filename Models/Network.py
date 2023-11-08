import numpy as np

# activation functions
sigmoid = lambda t: 1 / (1 + np.exp(-t))
f = lambda t: (t >= 1).astype(float)


class NeuralNetwork:

  def __init__(self, layer0, layer1, layer2):
    self.layer0 = layer0
    self.layer1 = layer1
    self.layer2 = layer2
    self.layer_1 = [0, 0, 0, 0]
    self.layer_2 = [0, 0]
    self.W1 = np.array([[1, 0], [0, 1], [0, 1], [1, 0]])

    self.W2 = np.array([
        [1, -100, 0, 0],
        [0, 0, 1, -100],
    ])

    self.W_1 = np.array([[-100, 0, 1, 0], [0, 1, 0, -100]])

    self.W_2 = np.array([[1, 0], [1, 0], [0, 1], [0, 1]])

    self.layer1 = f(np.dot(self.W1, self.layer0))
    self.layer2 = f(np.dot(self.W2, self.layer1))

  def feedforward(self):
    self.layer1 = f(np.dot(self.W1, self.layer0))
    self.layer2 = f(np.dot(self.W2, self.layer1))

  def backprop(self):
    self.layer_1 = f(np.dot(self.W_2, self.layer_2))
    self.layer0 = f(np.dot(self.W_1, self.layer_1) + self.layer0)
