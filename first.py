from random import random
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()


grid = np.zeros((100, 100))
grid[(20, 15)] = 1
grid[(30, 45)] = 1
grid[(45, 0)] = 1
grid_history = np.zeros(grid.shape)
grid_copy = deepcopy(grid)

grid_size = len(grid)               #* must be square

N = grid_size ** 2
T = 0.6
R = 0.1

can_stop = False


def get_neighbors(r, c):
    possible = [
        (r-1,c),
        (r,c-1),
        (r,c+1),
        (r+1,c)
    ]
    return [x for x in possible if (0 <= x[0] < grid_size and 0 <= x[1] < grid_size)]


def updatefig(*args):
    global grid, grid_history

    for r in range(len(grid)):
        for c in range(len(grid[r])):
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
    
    # update grid from copy
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            grid[r][c] = grid_copy[r][c]

    # update history
    grid_history += np.clip(grid, 0, 1)

    global can_stop
    counts = np.unique(grid)
    if len(counts) == 2:
        if can_stop:
            quit()
        else:
            can_stop = True

    # im.set_array(grid_history / np.max(grid_history))
    im.set_array(np.clip(grid_history / 100, 0, 1))
    return im,


im = plt.imshow(grid, animated=True)
# fig.colorbar(im)

ani = animation.FuncAnimation(fig, updatefig, interval=50, blit=True)
plt.show()