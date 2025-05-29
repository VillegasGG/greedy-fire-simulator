from greedyff.simulation import Simulation
from greedyff.tree_generator import generate_random_tree
from greedyff.greedy_step import GreedyStep
from pathlib import Path

class GreedySim:
    def __init__(
            self, 
            tree = None, 
            root = None,
            n_nodes:int = None, 
            root_degree:int = None, 
            type_root_degree:str = None, 
            ff_speed:float = 1.0, 
            output_dir = "output"):	
        """
        Initialize the GreedySim class 
        :param tree: Tree object to be used in the simulation
        :param n_nodes: Number of nodes in the tree
        :param root_degree: Degree of the root node
        :param type_root_degree: Type of root degree ('min' or 'max')
        :param ff_speed: Speed of the firefighter
        :param output_dir: Directory to save the output files
        """
        
        self.ff_speed = ff_speed
        self.output_dir = Path(output_dir)
        
        # If a tree is provided (check by attribute existence)
        if hasattr(tree, 'nodes') and hasattr(tree, 'edges'):

            # Root validation
            if root is None or root not in tree.nodes:
                raise ValueError(f"Root {root} is not in the provided tree nodes: {tree.nodes}")
            
            self.tree = tree
            self.root = root

            # If no necessary parameters are provided, use the tree's properties but advise
            if n_nodes is not None or root_degree is not None or type_root_degree is not None:
                print("Warning: Tree provided, but n_nodes, root_degree, or type_root_degree are set. Using tree properties instead.")

        # If not tree is provided, generate a random tree
        else:
            # Validate parameters
            if n_nodes is None or root_degree is None or type_root_degree is None:
                raise ValueError("No tree is provided! n_nodes, root_degree, and type_root_degree must be specified.")
        
            self.n_nodes = n_nodes
            self.root_degree = root_degree
            self.type_root_degree = type_root_degree
            self.tree, self.sequence, self.root = generate_random_tree(self.n_nodes, self.root_degree, self.type_root_degree)
            
        self.my_tree, _ = self.tree.convert_to_directed(self.root)

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

        simulation = Simulation(GreedyStep(self.my_tree), self.my_tree, self.ff_speed, self.output_dir)
        simulation.run_simulation(self.output_dir)


        