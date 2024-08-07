import networkx as nx
from separator import planar_separator_algorithm
from utils import plot_graph

def recursive_separation(G):
    """
    Recursively partition the graph G and return the separator tree.
    """
    if len(G) <= 2:
        return None, G.nodes()
    
    # Find a balanced separator
    separator, H1, H2 = planar_separator_algorithm(G)
    # # Create the subgraphs
    # H1 = G.subgraph(set1).copy()
    # H2 = G.subgraph(set2).copy()

    # Recurse on the subgraphs
    T1, nodes1 = recursive_separation(H1)
    T2, nodes2 = recursive_separation(H2)
    
    # Create the separator tree node
    T = {
        'separator': separator,
        'left': T1,
        'right': T2,
        'nodes': list(nodes1) + list(nodes2)
    }
    
    return T, T['nodes']

if __name__ == "__main__":
    # 1. Create a 5x5 planar grid graph
    G = nx.grid_2d_graph(5, 5)
    G = nx.convert_node_labels_to_integers(G)
    nx.set_node_attributes(G, 1, 'cost')
    
    # Plot the original graph
    plot_graph(G, title="Original 5x5 Planar Graph")
    
    # 2. Generate the separator tree
    separator_tree, _ = recursive_separation(G)