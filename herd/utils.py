import csv


# graph to csv
def to_csv(G, name):
    with open(f'data/{name}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['source', 'source_attr', 'target', 'target_attr'])
        for i in G.nodes:
            for j in G.neighbors(i):
                writer.writerow([i, get_status(G, i), j, get_status(G, j)])
