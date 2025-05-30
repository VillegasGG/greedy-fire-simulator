import time
from pathlib import Path
from greedyff.helpers import save_results, save_history
from greedyff.environment import Environment

class Simulation:
    def __init__(self, policy, speed, output_dir, tree = None, enviroment = None, ff_position=None, remaining_time=None):
        self.policy = policy
        self.output_dir = Path(output_dir)

        if enviroment is None:
            try:
                self.env = Environment(tree, speed, ff_position, remaining_time)
            except Exception as e:
                raise ValueError(f"Error initializing environment: {e}. Ensure the tree is valid and parameters are correct.") from e
        else:
            if hasattr(enviroment, 'tree') and hasattr(enviroment, 'firefighter'):
                self.env = enviroment
            else:
                raise ValueError("Provided environment does not have the required attributes (tree and firefighter).")

    def firefighter_action(self, step):
        """
        Turno del bombero
        """
        # Create path for step directory
        step_dir = self.output_dir / "steps_log" / f"step_{step}"
        step_dir.mkdir(parents=True, exist_ok=True)

        exist_candidate = True

        while(self.env.firefighter.get_remaining_time() > 0 and exist_candidate):
            exist_candidate = self.policy.select_action(self.env, step_dir)
            
    def execute_step(self, step):
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

        if not self.env.state.burning_nodes:
            self.env.start_fire(self.env.tree.root)
        else:
            self.firefighter_action(step)
            self.env.propagate()
    
    def run_simulation(self, output_dir):
        step = -1
        
        start_time = time.perf_counter()
        
        while not self.env.is_completely_burned():
            step += 1
            if step>0: print(f"{'#' * 50}\nWHEN STATE {step-1}:")
            self.execute_step(step)
        
        end_time = time.perf_counter()
            
        print('#' * 50)

        save_results(self.env.state.burned_nodes, self.env.state.burning_nodes, self.env.state.protected_nodes, "result.json", output_dir)
        save_history(self.env.history, output_dir)

        print('-' * 50 + f"\nDaño: {len(self.env.state.burned_nodes) + len(self.env.state.burning_nodes)}\n" + '-' * 50)
        print(f"Tiempo de ejecución total: {end_time - start_time:.4f} segundos")
