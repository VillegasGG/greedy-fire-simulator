from pathlib import Path
from greedyff.greedy_step import GreedyStep

class GreedySim:
    def __init__(self, env = None, ff_speed:float = 1.0, output_dir = "output"):	
        if env is not None:
            self.env = env
            self.d_tree = env.tree
            self.ff_speed = env.firefighter.speed
            self.ff_position = env.firefighter.position
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

        # Save the tree structure and sequence to JSON files
        # self.d_tree.save_positions(self.output_dir / "data" / "positions.txt")
        # self.d_tree.save_edges(self.output_dir / "data" / "edges.txt")

        damage = self.run_simulation()

        return damage

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

        self.execute_step()

        return self.env

    def firefighter_action(self):
        """
        Turno del bombero
        """

        exist_candidate = True

        while(self.env.firefighter.get_remaining_time() > 0 and exist_candidate):
            exist_candidate = GreedyStep(self.d_tree).select_action(self.env)
            
    def execute_step(self):
        """
        Ejecuta un paso de la simulacion:
        A) Si no hay nodos quemados:
            - Se inicia el fuego en el nodo raiz
            - Se coloca un bombero en una posicion aleatoria
        B) Si hay nodos quemados:
            - Turno del bombero dado que el anterior fue propagacion o inicio del fuego
            - Turno de la propagacion del fuego
        """
        if self.env.firefighter.get_remaining_time() is None or self.env.firefighter.get_remaining_time() <= 0:
            self.env.firefighter.init_remaining_time()
            # print(f"Step {step}: Firefighter's remaining time initialized to {self.env.firefighter.get_remaining_time()}")

        if not self.env.state.burning_nodes:
            self.env.start_fire(self.env.tree.root)
            if self.env.firefighter.position is None:
                self.env.firefighter.add_random_initial_position()
            else: 
                self.env.firefighter.position = self.ff_position
        else:
            self.firefighter_action()
            # print(f"Step {step}: Firefighter's remaining time after action: {self.env.firefighter.get_remaining_time()}")
            self.env.propagate()
    
    def run_simulation(self):
        step = -1
        
        while not self.env.is_completely_burned():
            step += 1
            print(f"--- Step {step} ---")
            print(f"Firefighter position: {self.env.firefighter.position}, Remaining time: {self.env.firefighter.get_remaining_time()}")
            self.execute_step()

        # Return damage
        return len(self.env.state.burned_nodes) + len(self.env.state.burning_nodes)
