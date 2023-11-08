import numpy as np
from matplotlib import pyplot as plt
from Models.Limb import Limb
from Models.Runner import Runner

# activation functions
sigmoid = lambda t: 1/(1+np.exp(-t))
f = lambda t: (t >= 1).astype(float)
act1 = lambda x: (x//6)%2 #сюда надо веса и как либо обучать

N = 30
time = list(range(N))

segment = Limb(3, 4, [1, 0], [0, 0, 0, 0], [])
simulation = Runner(N, segment)
simulation.run_simulate()
simulation.display("layer0")
#time
time = list(range(N))