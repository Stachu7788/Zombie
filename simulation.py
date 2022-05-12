import numpy as np
from matplotlib import pyplot as plt

class Simulation:    
    def __init__(self, healthy: int = 900, armed: int = 50, infected: int = 50):
        self.healthy = healthy
        self.armed = armed
        self.infected = infected
        self.total = self.healthy + self.armed + self.infected
        self.population = np.zeros((self.total, 10))
        """
        population:
            0: id
            1: x coordinate
            2: y coordinate
            3: x direction speed
            4: y direction speed
            5: state(0: healthy, 1: armed, 2: infected)
        """
        self.population[:, 0] = [x for x in range(self.total)]
        self.population[:, 1] = np.random.uniform(0.01, 0.99, self.total)
        self.population[:, 2] = np.random.uniform(0.01, 0.99, self.total)
        self.population[:, 3] = np.random.normal(0, 0.3, self.total)
        self.population[:, 4] = np.random.normal(0, 0.3, self.total)
        states = np.array(self.healthy*[0] + self.armed*[1] + self.infected*[2])
        self.population[:, 5] = np.random.permutation(states)
        
        self.chanceOfInfection = 0.03
        self.chanceOf__ = 0.05
        self.speed = 0.01
    
    def update_positions(self):
        self.population[:,1] = self.population[:,1] + self.population[:,3] * self.speed
        self.population[:,2] = self.population[:,2] + self.population [:,4] * self.speed
        
    def clip_positions(self):
        self.population[:, 3] = np.where(self.population[:, 1] < 0,
                                         -self.population[:, 3], 
                                         self.population[:, 3])
        self.population[:, 3] = np.where(self.population[:, 1] > 1,
                                         -self.population[:, 3], 
                                         self.population[:, 3])
        self.population[:, 4] = np.where(self.population[:, 2] < 0, 
                                         -self.population[:, 4], 
                                         self.population[:, 4])
        self.population[:, 4] = np.where(self.population[:, 2] > 1, 
                                         -self.population[:, 4], 
                                         self.population[:, 4])
        self.population[:, 1:3] = np.clip(self.population[:, 1:3], 0., 1.)
    
    def draw(self, frame, ax):
        ax.clear()
        ax.set_xlim(-0.01, 1.01)
        ax.set_ylim(-0.01, 1.01)
        
        healthy = self.population[self.population[:, 5] == 0][:, 1:3]
        ax.scatter(healthy[:, 0], healthy[:, 1], c='b', marker='.')

        armed = self.population[self.population[:, 5] == 1][:, 1:3]
        ax.scatter(armed[:, 0], armed[:, 1], c='hotpink', marker='.')

        infected = self.population[self.population[:, 5] == 2][:, 1:3]
        ax.scatter(infected[:, 0], infected[:, 1], c='g', marker='.')
        ax.set_title(f"Frame: {frame}")
        
        
        self.update_positions()
        self.clip_positions()
        return ax
        