import networkx as nx
import numpy as np
from collections import deque
from utils import plot_graph

# A SEPARATOR THEOREM FOR PLANAR GRAPHS
# by Richard J. Lipton and Robert E. Tarjan
# https://www.cs.princeton.edu/courses/archive/fall06/cos528/handouts/sepplanar.pdf
def planar_separator_algorithm(G):
    # Step 1: Find a planar embedding of G and construct a representation for it
    pos = nx.planar_layout(G)
    
    # Step 2: Find the connected components of G and determine the cost of each one
    components = list(nx.connected_components(G))
    
    component_costs = {frozenset(comp): sum(G.nodes[v]['cost'] for v in comp) for comp in components}
    
    # If all components have costs <= 2/3, construct the partition and return
    if all(cost <= 2/3 for cost in component_costs.values()):
        return G.nodes
    
    # Otherwise, find the most costly component
    target_component = max(component_costs, key=component_costs.get)
    
    # Step 3: Find a breadth-first spanning tree of the most costly component
    root = list(target_component)[0]
    bfs_tree = nx.bfs_tree(G.subgraph(target_component), root)
    
    # Compute levels and the number of vertices in each level L(l)
    levels = {}
    level_sizes = {}
    for node in bfs_tree.nodes:
        level = nx.shortest_path_length(bfs_tree, source=root, target=node)
        levels[node] = level
        if level not in level_sizes:
            level_sizes[level] = 0
        level_sizes[level] += 1
    
    # Step 4: Find the critical level l1 such that the total cost of levels 0 through l1-1 does not exceed 1/2,
    # but the total cost of levels 0 through l1 does exceed 1/2.
    cumulative_cost = 0
    l1 = None
    total_cost = sum(G.nodes[v]['cost'] for v in target_component)
    half_cost = total_cost / 2
    
    for level in sorted(level_sizes.keys()):
        if cumulative_cost + level_sizes[level] > half_cost:
            l1 = level
            break
        cumulative_cost += level_sizes[level]
    
    # k is the number of vertices in levels 0 through l1
    k = sum(level_sizes[l] for l in range(l1 + 1))
    
    # Step 5: Find the highest level l0 <= l1 such that L(l0) + 2(l1 - l0) <= 2√k,
    # and the lowest level l2 >= l1 + 1 such that L(l2) + 2(l2 - l1 - 1) <= 2√(n-k).
    sqrt_k = 2 * np.sqrt(k)
    sqrt_n_minus_k = 2 * np.sqrt(len(G.nodes) - k)
    
    l0_candidates = [l for l in range(l1 + 1) if level_sizes[l] + 2 * (l1 - l) <= sqrt_k]
    if l0_candidates:
        l0 = max(l0_candidates)
    else:
        l0 = l1  # Fallback to l1 if no valid l0 is found
    
    l2_candidates = [l for l in range(l1 + 1, max(level_sizes.keys()) + 1) if level_sizes[l] + 2 * (l - l1 - 1) <= sqrt_n_minus_k]
    if l2_candidates:
        l2 = min(l2_candidates)
    else:
        l2 = l1 + 1  # Fallback to l1+1 if no valid l2 is found
    
    # Step 6: Identify separator nodes
    separator_nodes = [node for node, level in levels.items() if level == l1]
    
    # Step 7: Create subgraphs
    subgraph1_nodes = {node for node in target_component if node in levels and levels[node] <= l1}
    subgraph2_nodes = {node for node in target_component if node in levels and levels[node] > l1}

    # Include separator nodes in both subgraphs
    subgraph1 = G.subgraph(subgraph1_nodes | set(separator_nodes)).copy()
    subgraph2 = G.subgraph(subgraph2_nodes | set(separator_nodes)).copy()

    plot_graph(subgraph1, title="Subgraph 1")
    plot_graph(subgraph2, title="Subgraph 2")
    
    return separator_nodes, subgraph1, subgraph2

# Nested Dissection Meets IPMs: Planar Min-Cost Flow in Nearly-Linear Time
# http://arxiv.org/abs/2205.01562
def recursive_separation(G):
    """
    Recursively partition the graph G and return the separator tree.
    """
    if len(G) <= 2:
        return None, G.nodes()
    
    # Find a balanced separator
    separator, H1, H2 = planar_separator_algorithm(G)
    
    # Stop recursion if subgraphs are edge-less
    if H1.number_of_edges() == 0 or H2.number_of_edges() == 0:
        return None, G.nodes()

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

def print_separator_tree(tree, depth=0):
    if tree is None:
        return
    indent = "  " * depth
    print(f"{indent}Separator: {tree['separator']}")
    if tree['left'] or tree['right']:
        print(f"{indent}Left:")
        print_separator_tree(tree['left'], depth + 1)
        print(f"{indent}Right:")
        print_separator_tree(tree['right'], depth + 1)

if __name__ == "__main__":
    # 1. Create a 5x5 planar grid graph
    G = nx.grid_2d_graph(5, 5)
    G = nx.convert_node_labels_to_integers(G)
    nx.set_node_attributes(G, 1, 'cost')
    
    # Plot the original graph
    plot_graph(G, title="Original 5x5 Planar Graph")
    
    # 2. Generate the separator tree
    separator_tree, _ = recursive_separation(G)
    print_separator_tree(separator_tree)
