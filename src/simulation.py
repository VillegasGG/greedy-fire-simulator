import time
from src.helpers import save_results
from src.environment import Environment

class Simulation:
    def __init__(self, policy, tree):
        self.env = Environment(tree)
        self.policy = policy

    def firefighter_action(self):
        """
        Turno del bombero
        """
        exist_candidate = True

        while(self.env.firefighter.get_remaining_time() > 0 and exist_candidate):
            exist_candidate = self.policy.select_action(self.env)
            
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
        self.env.firefighter.init_remaining_time()

        if not self.env.state.burning_nodes:
            self.env.start_fire(self.env.tree.root)
        else:
            self.firefighter_action()
            self.env.propagate()
    
    def run_simulation(self):
        step = -1
        
        start_time = time.perf_counter()
        
        while not self.env.is_completely_burned():
            step += 1
            if step>0: print(f"{'#' * 50}\nWHEN STATE {step-1}:")
            self.execute_step()
        
        end_time = time.perf_counter()
            
        print('#' * 50)

        save_results(self.env.state.burned_nodes, self.env.state.burning_nodes, self.env.state.protected_nodes, "result.json")
        
        print('-' * 50 + f"\nDaño: {len(self.env.state.burned_nodes) + len(self.env.state.burning_nodes)}\n" + '-' * 50)
        print(f"Tiempo de ejecución total: {end_time - start_time:.4f} segundos")
