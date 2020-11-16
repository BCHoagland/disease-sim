import networkx as nx
import matplotlib.pyplot as plt

from constants import SUS, INF, REC
from graph import get_status


node_colors = {SUS: 'b', INF: 'r', REC: 'k'}

def plot_net(G, pos=None, save=None):
    colors = [node_colors[G.status(i)] for i in G.nodes]
    if pos is not None:
        nx.draw(G.G, pos=pos, with_labels=False, node_size=5, arrows=True, width=0.2, edge_color='gray', node_color=colors)
    else:
        nx.draw_kamada_kawai(G.G, with_labels=False, node_size=5, arrows=True, width=0.2, edge_color='gray', node_color=colors)

    if save is not None:
        plt.savefig(f'img/{save}.png', dpi=500)
    else:
        plt.show()
