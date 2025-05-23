from ctypes import *
import numpy as np
from collections import deque

class Tree:
    def __init__(self, nodes, edges, nodes_positions=None, is_adjacency_matrix=False):
        """
        Inicializa un objeto Tree
        """
        self.nodes = nodes
        self.nodes_positions = self.initialize_positions(nodes, nodes_positions)
        self.height = 0
        self.__is_directed__ = False
        self.root = None
        self.edges = self.initialize_edges(nodes, edges, is_adjacency_matrix)
    
    def initialize_positions(self, nodes, nodes_positions):
        """
        Inicializa las posiciones de los nodos si se proporcionan
        """
        if(nodes_positions is not None):
            return np.array([nodes_positions[i] for i in nodes])
        return None
        
    def initialize_edges(self, nodes, edges, is_adjacency_matrix):
        """
        Inicializa la matriz de adyacencia
        """
        if is_adjacency_matrix:
            return edges
        else:
            adjacency_matrix = np.zeros((len(nodes), len(nodes)))
            for o, d in edges:
                adjacency_matrix[o, d] = 1
                adjacency_matrix[d, o] = 1
            return adjacency_matrix
        
    def save_positions_to_json(self, filename):
        with open(filename, "w") as file:
            for i in range(self.nodes.shape[0]):
                file.write(f"{self.nodes[i]} {self.nodes_positions[i][0]} {self.nodes_positions[i][1]} {self.nodes_positions[i][2]} ")
                file.write("\n")

    def save_edges_to_json(self, filename):
        with open(filename, "w") as file:
            file.write(f"{self.root}\n")
            for i in range(self.edges.shape[0]):
                for j in range(self.edges.shape[1]):
                    if self.edges[i][j] == 1:
                        file.write(f"{i} {j}\n")


    @property
    def is_directed(self):
        """
        Indica si el árbol ha sido convertido en dirigido
        """
        return self.__is_directed__

    def __subtree_to_directed__(self, tree, node, visited):
        """
        Convierte un subárbol a un árbol dirigido, comenzando desde el nodo dado
        """
        height = 0
        max_height = 0
        visited[node] = True

        for neighbor in tree.nodes:
            if not visited[neighbor] and tree.edges[node][neighbor] != 0:
                tree.edges[neighbor][node] = 0
                height = self.__subtree_to_directed__(tree, neighbor, visited)
                if(height > max_height):
                    max_height = height

        return 1 + max_height
                
    def convert_to_directed(self, root):
        """
        Convierte el árbol en un árbol dirigido y calcula su altura
        """
        # Crea una copia del arbol actual
        directed_tree = Tree(
                    np.copy(self.nodes), 
                    np.copy(self.edges), 
                    None, 
                    is_adjacency_matrix=True
                )
        
        # Copia las direcciones de los nodos
        directed_tree.nodes_positions = np.copy(self.nodes_positions)

        visited = [False] * directed_tree.nodes.shape[0]
        height = self.__subtree_to_directed__(directed_tree, root, visited)
        directed_tree.__is_directed__ = True
        directed_tree.root = root
        directed_tree.height = height
    
        return directed_tree, height
    
    def get_path_to_root(self, node):
        """
        Obtiene el camino desde un nodo hasta la raíz del árbol.
        """
        assert self.__is_directed__, "The tree must be converted to directed"

        ancestors = [node]
        c_node = node

        for _ in range(self.nodes.shape[0]):
            if c_node != self.root:
                c_node = np.argwhere(self.edges.T[c_node] == 1)[0, 0]
            else:
                break
            
            ancestors.append(c_node)
            
        return np.array(ancestors)
        
    def get_subtree_nodes(self, node):
        """
        Obtiene todos los nodos en el subárbol a partir de un nodo dado.
        """
        assert self.__is_directed__, "The tree must be converted to directed"

        nodes = [node]
        c_node = node

        nodes_idx = 0

        for _ in range(self.nodes.shape[0]):
            if(nodes_idx >= len(nodes)):
                break

            c_node = nodes[nodes_idx]
            next_nodes = np.argwhere(self.edges[c_node] == 1).flatten()
            nodes += next_nodes.tolist()
            nodes_idx += 1

        return np.array(nodes)
    
    def get_neighbors(self, node):
        """
        Devuelve una lista de los nodos vecinos de un nodo dado
        """
        assert 0 <= node < len(self.nodes), "El índice del nodo está fuera de los límites"

        # Encuentra los índices de los nodos que son vecinos
        neighbors = np.argwhere(self.edges[node] == 1).flatten()
        
        return neighbors

class TREE(Structure):
    _fields_ = [
        ("n_nodes", c_uint8),
        ("height", c_uint8),
        ("n_leaves", c_uint8),
        ("nodes", POINTER(c_uint8)),
        ("nodes_x", POINTER(c_float)),
        ("nodes_y", POINTER(c_float)),
        ("nodes_z", POINTER(c_float)),
        ("egdes", POINTER(POINTER(c_float)))
    ]


def tree_to_structure(tree):
    assert tree.is_directed, "The tree must be converted to directed"

    n_nodes = tree.nodes.shape[0]
    n_positions = tree.nodes_positions.shape[0]
    n_leaves = (int) (np.argwhere(tree.edges.sum(axis=-1) == 0).flatten().shape[0])

    return TREE(
        n_nodes,
        tree.height,
        n_leaves,
        (c_uint8 * n_nodes)(*tree.nodes.tolist()),
        (c_float * n_positions)(*tree.nodes_positions[:, 0].tolist()),
        (c_float * n_positions)(*tree.nodes_positions[:, 1].tolist()),
        (c_float * n_positions)(*tree.nodes_positions[:, 2].tolist()),

        (POINTER(c_float) * n_nodes)(*[ (c_float * n_nodes)(*r) for r in tree.edges.tolist()])
        )
        

