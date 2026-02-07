import networkx as nx
import numpy as np
from greedyff.tree_utils import Tree

def generate_prufer_sequence(n_nodes):
    """
    Generates a random Prüfer sequence.
    """
    return np.random.randint(0, n_nodes, size=n_nodes - 2)

def calculate_degrees(sequence, n_nodes):
    """
    Calculates the degrees of the nodes based on the Prüfer sequence
    """
    degrees = np.ones(n_nodes)
    counts = np.bincount(sequence, minlength=n_nodes)
    degrees += counts
    return degrees

def add_edge(edges, node1, node2, degrees):
    """
    Add an edge to the tree and update the degrees of the nodes.
    """
    edges.append((node1, node2))
    degrees[node1] -= 1
    degrees[node2] -= 1

def generate_positions(n_nodes, edges):
    """
    Generate random positions for the nodes of the tree using a force-directed layout algorithm.
    """
    tree = nx.Graph()
    tree.add_nodes_from(np.arange(n_nodes))
    tree.add_edges_from(edges)
    return nx.drawing.layout.fruchterman_reingold_layout(tree, dim=3, scale=1.)

def construct_edges(sequence, degrees):
    """
    Construct the edges of the tree based on the Prüfer sequence and the degrees of the nodes.
    """
    edges = []
    # Construct edges from the sequence
    for node in sequence:
        leaf = np.argwhere(degrees == 1)[0, 0]
        add_edge(edges, node, leaf, degrees)

    # Add the last edge
    remaining_nodes = np.argwhere(degrees == 1)[:, 0]
    assert remaining_nodes.shape[0] == 2, "There are more than 2 remaining degrees = 1"
    edges.append((remaining_nodes[1], remaining_nodes[0]))
    return edges

def create_tree_from_sequence(sequence, add_positions=True, positions=None):
    """
    Create a Tree object from a given Prüfer sequence, optionally adding positions to the nodes.
    """
    n_nodes = sequence.shape[0] + 2
    degrees = calculate_degrees(sequence, n_nodes)
    
    edges = construct_edges(sequence, degrees)

    if add_positions:
        positions = generate_positions(n_nodes, edges)
        
    return Tree(np.arange(n_nodes), np.array(edges), positions)

def validate_candidate_roots(type_root_degree, root_degree, counts):
    """
    Validates the candidate roots based on the degree of the root and the type of degree requirement.
    """
    if type_root_degree == "exact":
        return np.argwhere(counts == root_degree - 1).flatten()
    elif type_root_degree == "min":
        return np.argwhere(counts >= root_degree - 1).flatten()
    else:
        raise ValueError(f"Root degree type {type_root_degree} not recongized!")

def generate_random_tree(n_nodes, root_degree, type_root_degree, add_positions=True, max_trials=1000):    
    """
    Generetes a random tree with a specified number of nodes and a root node with a specific degree.
    """
    for i in range(max_trials):
        sequence = generate_prufer_sequence(n_nodes)
        counts = np.bincount(sequence, minlength=n_nodes)
        candidate_roots = validate_candidate_roots(type_root_degree, root_degree, counts)

        if len(candidate_roots) > 0:
            root = np.random.choice(candidate_roots)
            return create_tree_from_sequence(sequence, add_positions), sequence.tolist(), int(root)

    raise ValueError(f"Can't find a tree of {n_nodes} nodes and a root of degree {root_degree} in {max_trials} trials.")

    