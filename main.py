import numpy as np
from matplotlib import pyplot as plt
from Models.Limb import Limb
from Models.Runner import Runner

# activation functions
sigmoid = lambda t: 1/(1+np.exp(-t))
f = lambda t: (t >= 1).astype(float)
act1 = lambda x: ((x+1)//6)%2 #сюда надо веса и как либо обучать

def main():
    N = 
    time = list(range(N))

    segment = Limb(10, 3, 4, [1, 0], [0, 0, 0, 0], [])
    simulation = Runner(N, segment)
    simulation.run_simulate(act1)
    simulation.display_layer("layer2")
    simulation.display_layer("layer0")
    simulation.display_limb()
    plt.show()
    #time
    time = list(range(N))

if __name__=="__main__":
    main()