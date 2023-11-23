
## Display action of LIMB


import pandas as pd
import matplotlib.pyplot as plt
from Models.Runner import Runner
from Models.Limb import Limb
import numpy as np
from time import sleep 
from matplotlib import animation

act1 = lambda x: ((x+3)//6)%2
segment = Limb(10, 3, 4, [1, 0], [0, 0, 0, 0], [])
N = int(input("time="))
sim_name= f"Simulation t={N} loops";
simulation = Runner(N, segment)
segment = simulation.run_simulate(act1)
    
print("segment params:")
df = pd.DataFrame(data = {
            "a" : [simulation.limb.a],
            "b" : [simulation.limb.b],
            "length" : [simulation.limb.length],
            "Time" : [f"{0}..{N}sec"] 
        })
print(df)
    
#display
fig, axs = plt.subplots(1, 2, figsize=(12, 7))
fig.suptitle(sim_name);
axs[0].set_title("Dynamics of sigment")
axs[0].set_xlabel("X")
axs[0].set_ylabel("Y")
axs[1].set_title("Evolution of musculs length")
axs[1].set_xlabel("N")
axs[1].set_ylabel("Length")

line_loc, = axs[0].plot([], [], 'r-', marker='o')  
line_f, = axs[1].plot([], [], 'b', label="flexor")
line_e, = axs[1].plot([], [], 'y', label = "extenzor")
axs[1].legend(loc=4)
l = simulation.limb.length
time = simulation.time
r = np.linspace(0, l, 2) 
fl = simulation.detector.flexor
el = simulation.detector.extenzor

def update(frame):
    cos_a = simulation.detector.alpha_flexor[frame]
    sin_a = np.sqrt(1-cos_a**2)
    y = r * sin_a
    x = r * cos_a + l
    line_loc.set_data(x, y)
    x1 = time[:frame]
    yf = fl[:frame]
    ye = el[:frame]
    line_f.set_data(x1, yf)
    line_e.set_data(x1, ye)
    return line_f,line_e,line_loc

def init():
    axs[0].set_xlim(0, 20)
    axs[0].set_ylim(-10, 10) 
    axs[1].set_xlim(0, N)
    axs[1].set_ylim(0, 7)
    line_f.set_data([],[])
    line_e.set_data([],[])
    line_loc.set_data([],[])
    return line_f, line_e, line_loc
    
ani_locomotion = animation.FuncAnimation(fig, update, frames=N,
                    init_func=init, blit=True)

ani_locomotion.save(f"{sim_name}.gif")
plt.show()