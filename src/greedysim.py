from src.simulation import Simulation
from src.tree_generator import generate_random_tree
from src.greedy_step import GreedyStep
from pathlib import Path

class GreedySim:
    def __init__(self, n_nodes, root_degree, type_root_degree, output_dir="output"):	
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
        self.output_dir = Path(output_dir)

    def run(self):
        """
        Run the greedy simulation.
        """

        # Create the output and data directories if they don't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.joinpath("data").mkdir(parents=True, exist_ok=True)

        # Save the tree structure and sequence to JSON files
        self.my_tree.save_positions_to_json(self.output_dir / "data" / "positions.json")
        self.my_tree.save_edges_to_json(self.output_dir / "data" / "edges.json")

        simulation = Simulation(GreedyStep(self.my_tree), self.my_tree)
        simulation.run_simulation(self.output_dir)


        