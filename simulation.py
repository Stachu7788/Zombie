import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

class Simulation:    
    def __init__(self, healthy: int = 900, armed: int = 50, infected: int = 50):
        self.healthy = healthy
        self.armed = armed
        self.infected = infected
        self.total = self.healthy + self.armed + self.infected
        self.population = np.zeros((self.total, 6))
        self.init_draw = False
        """
        population:
            0: id
            1: x coordinate
            2: y coordinate
            3: x direction speed
            4: y direction speed
            5: state(0: healthy, 1: armed, 2: infected 3: dead)
        """
        self.population[:, 0] = [x for x in range(self.total)]
        self.population[:, 1] = np.random.uniform(0.01, 0.99, self.total)
        self.population[:, 2] = np.random.uniform(0.01, 0.99, self.total)
        self.population[:, 3] = np.random.normal(0.15, 0.3, self.total)
        self.population[:, 4] = np.random.normal(0.15, 0.3, self.total)
        states = np.array(self.healthy*[0] + self.armed*[1] + self.infected*[2])
        self.population[:, 5] = np.random.permutation(states)
        
        # Simulation parameters
        self.chanceOfInfection = 0.1
        self.infectionRange = 0.05
        self.chanceOfDeath = 1.
        self.attackRange = 0.02
        self.chanceOfUpgrade = .001
        self.speed = 0.01
        
        
        # Simulation variables
        self.frames = 100
        self.stats = np.zeros((5, self.frames))
        self.statsArray = []
    
    def update_positions(self):
        self.population[:,1] = (self.population[:,1] + self.population[:,3] * 
                                self.speed)
        self.population[:,2] = (self.population[:,2] + self.population [:,4] * 
                                self.speed)
        
    def find_nearby(self, infection_zone, state):
        indices = np.int32(self.population[:,0][(infection_zone[0] < self.population[:,1]) &
                                            (self.population[:,1] < infection_zone[1]) &
                                            (infection_zone[2] < self.population [:,2]) &
                                            (self.population[:,2] < infection_zone[3]) &
                                            (self.population[:,5] == state)])
        return indices
        
    def calc_dist(self, idx, idy):
        a = self.population[idx, 1:3]
        b = self.population[idy, 1:3]
        return np.linalg.norm(a-b)
    
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

    def infect(self):
        infected = self.population[self.population[:, 5] == 2]
        
        for zombie in infected:
            infection_zone = [zombie[1] - self.infectionRange, 
                              zombie[1] + self.infectionRange,
                              zombie[2] - self.infectionRange,
                              zombie[2] + self.infectionRange]
            healthy_in_zone = self.find_nearby(infection_zone, 0)
            armed_in_zone = self.find_nearby(infection_zone, 1)
            healthy_in_zone = np.concatenate((healthy_in_zone, armed_in_zone))
            for healthy in healthy_in_zone:
                chanceOfInfection = self.chanceOfInfection * self.infectionRange
                if np.random.random() < chanceOfInfection:
                    self.population[healthy, 5] = 2
                    
    def attack(self):
        armed = self.population[self.population[:, 5] == 1]
        
        for fighter in armed:
            infection_zone = [fighter[1] - self.infectionRange, 
                              fighter[1] + self.infectionRange,
                              fighter[2] - self.infectionRange,
                              fighter[2] + self.infectionRange]
            zombie_in_zone = self.find_nearby(infection_zone, 2)
            for zombie in zombie_in_zone:
                chance_of_death = self.chanceOfDeath * self.attackRange
                if np.random.random() < chance_of_death:
                    self.population[zombie, 5] = 3
    
    def upgrade(self):
        dist = np.random.uniform(0., 1., self.total)
        self.population[:, 5] = np.where(np.logical_and(self.population[:, 5] == 0,
                                          dist<self.chanceOfUpgrade), 1, self.population[:, 5])

    def update(self):
        if self.init_draw:
            self.update_positions()
            self.infect()
            self.attack()
            self.upgrade()
            self.clip_positions()
        else:
            self.init_draw = True
    
    def draw(self, frame, ax, gr):
        self.update()
        ax.clear()
        gr.clear()
        
        ax.set_xlim(-0.01, 1.01)
        ax.set_ylim(-0.01, 1.01)
        
        gr.set_xlim(0, self.frames)
        
        healthy = self.population[self.population[:, 5] == 0][:, 1:3]
        ax.scatter(healthy[:, 0], healthy[:, 1], c='orange', marker='.')

        armed = self.population[self.population[:, 5] == 1][:, 1:3]
        ax.scatter(armed[:, 0], armed[:, 1], c='hotpink', marker='.')

        infected = self.population[self.population[:, 5] == 2][:, 1:3]
        ax.scatter(infected[:, 0], infected[:, 1], c='seagreen', marker='.')
        
        dead = self.population[self.population[:, 5] == 3][:, 1:3]
        # ax.scatter(dead[:, 0], dead[:, 1], c='k', marker='.')
        
        ax.set_title(f"Frame: {frame}, Healthy: {healthy.shape[0]}, "
                     f"Armed: {armed.shape[0]}, Infected: {infected.shape[0]},"
                     f" Dead: {dead.shape[0]}")
        
        self.stats[:, frame] = np.array([frame, healthy.shape[0], armed.shape[0],
                                         infected.shape[0], dead.shape[0]])
        if frame == self.frames - 1:
            self.statsArray.append(np.copy(self.stats))
        
        gr.plot(self.stats[0, :frame], self.stats[1, :frame], '-', color='orange', label='healthy')
        gr.plot(self.stats[0, :frame], self.stats[2, :frame], '-', color='hotpink', label='warriors')
        gr.plot(self.stats[0, :frame], self.stats[3, :frame], '-', color='seagreen', label='infected')
        gr.plot(self.stats[0, :frame], self.stats[4, :frame], '-', color='black', label='dead')
        
        gr.legend()
        
        return ax, gr

    def simulate(self, frames):
        fig, (ax, gr) = plt.subplots(2, 1, figsize=(8, 10), gridspec_kw={'height_ratios': [4, 1]})
        
        self.frames = frames

        self.stats = np.zeros((5, self.frames))

        self.anim = animation.FuncAnimation(fig, self.draw, frames=self.frames, interval=50, fargs=(ax, gr, ))

    def draw_stats(self, num = 0):
        if self.statsArray.__len__() >0:
            stats = self.statsArray[0]
        else:
            stats = self.stats
        plt.plot(stats[0, :], stats[1, :], '-', color='orange', label='healthy')
        plt.plot(stats[0, :], stats[2, :], '-', color='hotpink', label='warriors')
        plt.plot(stats[0, :], stats[3, :], '-', color='seagreen', label='infected')
        plt.plot(stats[0, :], stats[4, :], '-', color='black', label='dead')
        
        plt.legend()
        plt.grid()


