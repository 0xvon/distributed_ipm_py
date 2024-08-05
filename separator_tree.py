import networkx as nx
import matplotlib.pyplot as plt

def balanced_vertex_separator(G):
    """
    Find a balanced vertex separator for the graph G.
    The separator will split the graph into two edge-disjoint subgraphs, where
    the separator nodes are shared between the two subgraphs.
    """
    if len(G) == 0:
        return set(), set(), set()

    # For a grid graph, calculate the dimensions
    side_length = int(len(G.nodes())**0.5)
    
    # Find the middle row nodes (approximation)
    separator = set()
    for i in range(side_length):
        node = (side_length // 2) * side_length + i
        separator.add(node)
    
    # Separate the graph into two edge-disjoint subgraphs by removing the separator nodes
    H1 = set()
    H2 = set()
    for node in G.nodes():
        if node not in separator:
            if all(neighbor not in separator for neighbor in G.neighbors(node)):
                if len(H1) < len(H2):
                    H1.add(node)
                else:
                    H2.add(node)
            elif any(neighbor in separator for neighbor in G.neighbors(node)):
                if len(H1) < len(H2):
                    H1.add(node)
                else:
                    H2.add(node)
    
    # Ensure that H1 and H2 include the separator nodes
    H1.update(separator)
    H2.update(separator)
    
    return separator, H1, H2

def recursive_partition(G):
    """
    Recursively partition the graph G and return the separator tree.
    """
    if len(G) <= 2:
        return None, G.nodes()
    
    # Find a balanced separator
    separator, set1, set2 = balanced_vertex_separator(G)
    
    # Create the subgraphs
    H1 = G.subgraph(set1).copy()
    H2 = G.subgraph(set2).copy()

    # Recurse on the subgraphs
    T1, nodes1 = recursive_partition(H1)
    T2, nodes2 = recursive_partition(H2)
    
    # Create the separator tree node
    T = {
        'separator': separator,
        'left': T1,
        'right': T2,
        'nodes': list(nodes1) + list(nodes2)
    }
    
    return T, T['nodes']

def plot_graph(G, title):
    """
    Plot the grid graph G with grid-like layout.
    """
    pos = {n: (n % 5, n // 5) for n in G.nodes()}  # Grid layout
    plt.figure(figsize=(6, 6))
    plt.title(title)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
    plt.show()

if __name__ == "__main__":
    # 1. Create a 5x5 planar grid graph
    G = nx.grid_2d_graph(5, 5)
    G = nx.convert_node_labels_to_integers(G)
    
    # Plot the original graph
    plot_graph(G, title="Original 5x5 Planar Graph")
    
    # 2. Generate the separator tree
    separator_tree, _ = recursive_partition(G)
    
    # Plot the graph after partitioning (if needed)
    separator = separator_tree['separator']
    H1_nodes = separator_tree['left']['nodes'] if separator_tree['left'] else []
    H2_nodes = separator_tree['right']['nodes'] if separator_tree['right'] else []
    
    separator_graph = G.subgraph(separator)
    H1 = G.subgraph(H1_nodes)
    H2 = G.subgraph(H2_nodes)

    plot_graph(H1, title="Left splitted Planar Graph")
    plot_graph(H2, title="Right splitted 5x5 Planar Graph")
    