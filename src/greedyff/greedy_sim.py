from greedyff.simulation import Simulation
from greedyff.tree_generator import generate_random_tree
from greedyff.greedy_step import GreedyStep
from pathlib import Path

class GreedySim:
    def __init__(self, env = None, ff_speed:float = 1.0, output_dir = "output"):	
        if env is not None:
            self.env = env
            self.d_tree = env.tree
            self.ff_speed = env.firefighter.speed
        else:
            self.env = None
            self.ff_speed = ff_speed
        
        self.output_dir = Path(output_dir)
                    

    def run(self, tree=None, root=None):
        """
        Run the greedy simulation from beginning to end.
        If an environment is provided, it will use the existing env otherwise it will create a new one.
        A tree is required to initialize the simulation if no environment is provided.
        """
        if self.env is None:
            print("No environment provided, creating a new one.")
            
            # Validate a tree is provided
            if tree is None:
                raise ValueError("A tree must be provided to initialize the simulation.")
            
            # Generate directed tree from the provided tree
            self.d_tree, _ = tree.convert_to_directed(root)
            
        # Create the output and data directories if they don't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.joinpath("data").mkdir(parents=True, exist_ok=True)
        print(f"Output directory created at: {self.output_dir}")

        # Save the tree structure and sequence to JSON files
        self.d_tree.save_positions(self.output_dir / "data" / "positions.txt")
        self.d_tree.save_edges(self.output_dir / "data" / "edges.txt")

        if self.env is None:
            simulation = Simulation(policy=GreedyStep(self.d_tree), tree=self.d_tree, speed=self.ff_speed, output_dir=self.output_dir)
            simulation.run_simulation(self.output_dir)
        else:
            simulation = Simulation(policy=GreedyStep(self.d_tree), enviroment=self.env, speed=self.ff_speed, output_dir=self.output_dir)
            simulation.run_simulation(self.output_dir)

    def step(self, env=None):
        """
        Execute a single step of the simulation.
        """
        if self.env is None and env is None:
            raise ValueError("An environment must be provided to execute a step.")
        if self.env is not None and env is not None:
            raise ValueError("Environment already exists, cannot provide a new one.")
        if self.env is None:
            self.env = env
            self.d_tree = env.tree
            self.ff_speed = env.firefighter.speed

        policy = GreedyStep(self.d_tree)

        sim = Simulation(policy=policy, speed=self.ff_speed, output_dir=self.output_dir, enviroment=self.env)

        sim.execute_step(0)

        return sim.env
        

    