import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import axes3d as p3

# Attach 3d axis to figure
fig = plt.figure()
ax = p3.Axes3D(fig)
lim = 1e12

# State vectors
v1 = np.array([0., 0., 0., 0., 0., 0.])
v2 = np.array([0., 0., 0., 0., 0., 0.])
v3 = np.array([0., 0., 0., 0., 0., 0.])


for v in [v1, v2, v3]:
    v[:3] = lim * np.random.rand(3) - lim/2
    v[3:] = 1e5 * np.random.rand(3) - 1e5/2
    

# =============================================================================
# # Custim assignments
# v2[0] = 23.7 * 149.6e9
# v3[1] = 13e3 * 149.6e9
# =============================================================================

# Properties and constants
m1 = 1.14 * 1.9884e30
m2 = 0.92 * 1.9884e30
m3 = 0.12 * 1.9884e30
G = 6.6743e-11
dt = 2e5

def dist(v, u):
    return np.linalg.norm(v[:3]-u[:3])
    

def update(dt):
    """
    dV = G*M/r^2 * dt
    dX = V * dt
    """
    r12 = dist(v1, v2)
    r13 = dist(v1, v3)
    r23 = dist(v2, v3)
    oldv1 = v1
    oldv2 = v2
    oldv3 = v3
    v1[3] += G*dt*(m2*(v2[0]-v1[0])/r12**3+
                   m3*(v3[0]-v1[0])/r13**3)
    v2[3] += G*dt*(m1*(v1[0]-v2[0])/r12**3+
                   m3*(v3[0]-v2[0])/r23**3)
    v3[3] += G*dt*(m1*(v1[0]-v3[0])/r13**3+
                   m2*(v2[0]-v3[0])/r23**3)
    v1[4] += G*dt*(m2*(v2[1]-v1[1])/r12**3+
                   m3*(v3[1]-v1[1])/r13**3)
    v2[4] += G*dt*(m1*(v1[1]-v2[1])/r12**3+
                   m3*(v3[1]-v2[1])/r23**3)
    v3[4] += G*dt*(m1*(v1[1]-v3[1])/r13**3+
                   m2*(v2[1]-v3[1])/r23**3)
    v1[5] += G*dt*(m2*(v2[2]-v1[2])/r12**3+
                   m3*(v3[2]-v1[2])/r13**3)
    v2[5] += G*dt*(m1*(v1[2]-v2[2])/r12**3+
                   m3*(v3[2]-v2[2])/r23**3)
    v3[5] += G*dt*(m1*(v1[2]-v3[2])/r13**3+
                   m2*(v2[2]-v3[2])/r23**3)
    v1[:3] += dt * oldv1[3:]
    v2[:3] += dt * oldv2[3:]
    v3[:3] += dt * oldv3[3:]

def draw(frame):
    update(dt)
    # print(f'v1: {v1}\nv2: {v2}\nv3: {v3}')
    ax.clear()
    ax.set_xlim3d([-lim, lim])
    ax.set_xlabel('X')

    ax.set_ylim3d([-lim, lim])
    ax.set_ylabel('Y')

    ax.set_zlim3d([-lim, lim])
    ax.set_zlabel('Z')
    ax.scatter(*v1[:3], c='blue')
    ax.scatter(*v2[:3], c='green')
    ax.scatter(*v3[:3], c='red')
    


anim = animation.FuncAnimation(fig, draw, 10)


