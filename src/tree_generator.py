import networkx as nx
import numpy as np
from src.tree_utils import Tree

def generate_prufer_sequence(n_nodes):
    """
    Genera una secuencia de Prüfer aleatoria.
    """
    return np.random.randint(0, n_nodes, size=n_nodes - 2)

def calculate_degrees(sequence, n_nodes):
    """
    Calcula los grados iniciales de los nodos basados en la secuencia de Prüfer.
    """
    degrees = np.ones(n_nodes)
    counts = np.bincount(sequence, minlength=n_nodes)
    degrees += counts
    return degrees

def add_edge(edges, node1, node2, degrees):
    """
    Añade una arista al árbol y actualiza los grados de los nodos.
    """
    edges.append((node1, node2))
    degrees[node1] -= 1
    degrees[node2] -= 1

def generate_positions(n_nodes, edges):
    """
    Genera posiciones 3D para los nodos del árbol utilizando NetworkX
    """
    tree = nx.Graph()
    tree.add_nodes_from(np.arange(n_nodes))
    tree.add_edges_from(edges)
    return nx.drawing.layout.fruchterman_reingold_layout(tree, dim=3, scale=1.)

def construct_edges(sequence, degrees):
    """
    Construye una lista de aristas a partir de una secuencia de nodos y un array de grados.
    """
    edges = []
    # Construye las aristas a partir de la secuencia
    for node in sequence:
        leaf = np.argwhere(degrees == 1)[0, 0]
        add_edge(edges, node, leaf, degrees)

    # Agrega la última arista
    remaining_nodes = np.argwhere(degrees == 1)[:, 0]
    assert remaining_nodes.shape[0] == 2, "There are more than 2 remaining degrees = 1"
    edges.append((remaining_nodes[1], remaining_nodes[0]))
    return edges

def create_tree_from_sequence(sequence, add_positions=True):
    """
    Crea un árbol a partir de una secuencia de Prüfer.
    """
    n_nodes = sequence.shape[0] + 2
    degrees = calculate_degrees(sequence, n_nodes)
    
    edges = construct_edges(sequence, degrees)

    # Genera posiciones de ser necesario
    positions = None

    if add_positions:
        positions = generate_positions(n_nodes, edges)
        
    return Tree(np.arange(n_nodes), np.array(edges), positions)

def validate_candidate_roots(type_root_degree, root_degree, counts):
    """
    Valida y encuentra los nodos candidatos que cumplen con el criterio de grado raíz
    """
    if type_root_degree == "exact":
        return np.argwhere(counts == root_degree - 1).flatten()
    elif type_root_degree == "min":
        return np.argwhere(counts >= root_degree - 1).flatten()
    else:
        raise ValueError(f"Root degree type {type_root_degree} not recongized!")

def generate_random_tree(n_nodes, root_degree, type_root_degree, add_positions=True, max_trials=1000):    
    """
    Genera un árbol aleatorio con un nodo raíz de un grado especificado
    """
    for i in range(max_trials):
        sequence = generate_prufer_sequence(n_nodes)
        counts = np.bincount(sequence, minlength=n_nodes)
        candidate_roots = validate_candidate_roots(type_root_degree, root_degree, counts)

        if len(candidate_roots) > 0:
            root = np.random.choice(candidate_roots)
            return create_tree_from_sequence(sequence, add_positions), sequence.tolist(), int(root)

    raise ValueError(f"Can't find a tree of {n_nodes} nodes and a root of degree {root_degree} in {max_trials} trials.")

    