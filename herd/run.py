import csv
import math
import random
import networkx as nx
import matplotlib.pyplot as plt

from constants import SUS, INF, REC
from graph import Graph
from visualize import plot_net

#! repeat with different seeds

seed = 10
num_nodes = 1000
max_timesteps = 120
β = 0.05
γ = 0.1
save = False
save_folder = 'scale'

import time
start_time = time.time()

random.seed(seed)


# spread the disease 😈
def step(G):
    statuses = [G.status(i) for i in G.nodes]
    for i in range(len(statuses)):
        # spread infection to susceptible neighbors
        if statuses[i] is INF:
            for j in G.neighbors(i):
                if G.status(j) is SUS:
                    if random.random() < β:
                        G.infect(j)
        
            # recovery
            if random.random() < γ:
                G.recover(i)


#################
# NETWORK TYPES #
#################

# small world
# G = Graph(nx.connected_watts_strogatz_graph, num_nodes, k=10, p=0.02, tries=100, seed=seed)

# scale free
G = Graph(nx.scale_free_graph, num_nodes, seed=seed)


############
# PANDEMIC #
############

# choose random initial infection
idx = random.randint(0, len(G.nodes) - 1)
G.infect(idx)

# track evolution of network
pos = nx.kamada_kawai_layout(G.G)
if save:
    plot_net(G, pos=pos, save=f'{save_folder}/0')

sus = [1]
inf = [0]
rec = [0]
for iter in range(max_timesteps):
    step(G)
    sus.append(G.counts[SUS] / num_nodes)
    inf.append(G.counts[INF] / num_nodes)
    rec.append(G.counts[REC] / num_nodes)

    if save:
        plot_net(G, pos=pos, save=f'{save_folder}/{iter + 1}')

# remove recovered to get residual network
recovered_nodes = [n for n in G.nodes if G.status(n) is REC]
G.remove_nodes_from(recovered_nodes)

# remove isolated nodes for better visualization
isolated_nodes = [n for n, deg in dict(G.degree()).items() if deg == 0]
G.remove_nodes_from(isolated_nodes)

plot_net(G, save=f'{save_folder}/residual')
plot_net(G)

# plot progress of pandemic
plt.close()
plt.plot(sus, label='S', lw=1)
plt.plot(inf, label='I', lw=1)
plt.plot(rec, label='R', lw=1)
plt.legend()
plt.show()
