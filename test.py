from simulation import Simulation
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

s = Simulation()
fig, ax = plt.subplots(figsize=(10, 10))

def init():
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return ax



anim = animation.FuncAnimation(fig, s.draw, frames=1000, interval=5, fargs=(ax,))



