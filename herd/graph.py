from constants import STATUS, SUS, INF, REC


def get_status(G, node_idx):
    return G.nodes[node_idx][STATUS]


def set_status(G, node_idx, status):
    old_status = get_status(G, node_idx)
    if status is not old_status:
        G.nodes[node_idx][STATUS] = status
        return True
    return False


class Graph:
    def __init__(self, creation_fn, num_nodes, **kwargs):
        # create initial network with all nodes susceptible
        self.G = creation_fn(num_nodes, **kwargs).to_undirected()
        for i in self.G.nodes:
            self.G.nodes[i][STATUS] = SUS

        # initial counts for each type of node
        self.counts = {
            SUS: num_nodes,
            INF: 0,
            REC: 0
        }
    
    def status(self, node_idx):
        return get_status(self.G, node_idx)

    def infect(self, node_idx):
        if set_status(self.G, node_idx, INF):
            self.counts[INF] += 1
            self.counts[SUS] -= 1
    
    def recover(self, node_idx):
        if set_status(self.G, node_idx, REC):
            self.counts[REC] += 1
            self.counts[INF] -= 1

    def __getattr__(self, k):
        return getattr(self.G, k)
