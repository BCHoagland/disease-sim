from random import random
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# parameters
num_init_infected = 3
grid_size = 200
N = grid_size ** 2
T = 0.3
R = 0.1

# create grid and infect initial people randomly
grid = np.zeros((grid_size, grid_size))
for _ in range(num_init_infected):
    grid[tuple(np.random.randint(0, grid_size, 2))] = 1

# additional bookkeeping grids
grid_history = np.zeros(grid.shape)
grid_copy = deepcopy(grid)


def get_neighbors(r, c):
    possible = [
        (r-1,c),
        (r,c-1),
        (r,c+1),
        (r+1,c)
    ]
    return [x for x in possible if (0 <= x[0] < grid_size and 0 <= x[1] < grid_size)]


def gen():
    global grid
    t = 0
    while 1 in np.unique(grid):
        t += 1
        yield t


def updatefig(t):
    global grid, grid_history

    # update grid
    for r in range(grid_size):
        for c in range(grid_size):
            if grid[r][c] == 1:
                # random recovery chance
                if random() < R:
                    grid_copy[r][c] = 2
                else:
                    # randomly infect susceptible neighbors
                    neighbors = get_neighbors(r, c)
                    for n in neighbors:
                        if grid[n] == 0 and random() < T:
                            grid_copy[n] = 1
    np.copyto(grid, grid_copy)

    # update history
    grid_history += np.clip(grid, 0, 1)

    im.set_array(grid_history / np.max(grid_history))
    return im,


fig = plt.figure()
im = plt.imshow(grid, cmap='magma', animated=True)

ani = animation.FuncAnimation(fig, updatefig, frames=gen, repeat=False, interval=50, blit=True)
plt.show()
