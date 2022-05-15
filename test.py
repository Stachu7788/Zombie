from simulation import Simulation
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

s = Simulation(200, 10, 30)

# =============================================================================
# fig, (ax, gr) = plt.subplots(2, figsize=(10, 10))
# 
# 
# anim = animation.FuncAnimation(fig, s.draw, frames=1000, interval=5, fargs=(ax, gr,))
# =============================================================================

s.simulate(1000)

# fig, (ax, gr) = plt.subplots(2, 1, figsize=(8, 10), gridspec_kw={'height_ratios': [4, 1]})

# a = s.find_nearby([.4, .6, .6, .8], 0)
# b = s.find_nearby([.6, .8, .6, .8], 0)
# s.draw(1, ax, gr)
# ax.grid(True)