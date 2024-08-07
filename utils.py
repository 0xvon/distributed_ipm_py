import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(G, title):
    """
    Plot the grid graph G with grid-like layout.
    """
    pos = {n: (n % 5, n // 5) for n in G.nodes()}  # Grid layout
    plt.figure(figsize=(6, 6))
    plt.title(title)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
    plt.show()