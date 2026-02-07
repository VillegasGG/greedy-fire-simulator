from pathlib import Path
from greedyff.greedy_step import GreedyStep

class GreedySim:
    def __init__(self, env = None, ff_speed:float = 1.0):	
        if env is not None:
            self.env = env
            self.d_tree =  env.state.tree
            self.ff_speed = env.firefighter.speed
            self.ff_position = env.firefighter.position
        else:
            self.env = None
            self.ff_speed = ff_speed                    

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
            self.d_tree = env.state.tree
            self.ff_speed = env.firefighter.speed

        self.execute_step()

        return self.env

    def firefighter_action(self):
        """
        Turno del bombero
        """

        exist_candidate = True

        while(self.env.firefighter.get_remaining_time() > 0 and exist_candidate):
            exist_candidate = GreedyStep(self.env).select_action()
            
    def execute_step(self):
        """
        Ejecuta un paso de la simulacion
        """
        if not self.env.state.burning_nodes:
            self.env.start_fire(self.env.state.tree.root)
            if self.env.firefighter.position is None:
                self.env.firefighter.add_random_initial_position()
            else: 
                self.env.firefighter.position = self.ff_position
            self.env.firefighter.init_remaining_time()
        
        if self.env.firefighter.get_remaining_time() == 0:
            self.env.propagate()
            self.env.firefighter.init_remaining_time()

        self.firefighter_action()
        self.env.propagate()
    
    def run_simulation(self):
        step = -1
        
        while not self.env.is_completely_burned():
            step += 1
            self.execute_step()

        # Return damage
        return len(self.env.state.burned_nodes) + len(self.env.state.burning_nodes)
