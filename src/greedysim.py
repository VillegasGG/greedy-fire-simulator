from src.simulation import Simulation
from src.tree_generator import generate_random_tree
from src.greedy_step import GreedyStep

class GreedySim:
    def __init__(self, n_nodes, root_degree, type_root_degree):
        """
        Initialize the GreedySim class with the number of nodes, root degree, and type of root degree.
        :param n_nodes: Number of nodes in the tree
        :param root_degree: Degree of the root node
        :param type_root_degree: Type of root degree ('min' or 'max')
        """
        self.n_nodes = n_nodes
        self.root_degree = root_degree
        self.type_root_degree = type_root_degree
        self.tree, self.sequence, self.root = generate_random_tree(self.n_nodes, self.root_degree, self.type_root_degree)
        self.my_tree, _ = self.tree.convert_to_directed(self.root)

    def run(self):
        """
        Run the greedy simulation.
        """
        simulation = Simulation(GreedyStep(self.my_tree), self.my_tree)
        self.my_tree.save_positions_to_json("data/positions.json")
        self.my_tree.save_edges_to_json("data/edges.json")
        simulation.run_simulation()


        