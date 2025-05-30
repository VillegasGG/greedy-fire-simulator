from greedyff.firefighter import Firefighter
from greedyff.fire_state import FireState
import copy

class Environment:
    def __init__(self, tree, speed, ff_position, remaining_time, fire_state=None):
        self.tree = tree
        self.firefighter = Firefighter(tree, speed, ff_position, remaining_time)
        self.history = []

        if fire_state is None:
            self.state = FireState(tree)
        else:
            self.state = fire_state

    def copy(self):
        """
        Copia el estado de la simulacion
        """
        return copy.deepcopy(self)
    
    def start_fire(self, initial_node):
        if initial_node in self.tree.nodes:
            self.state.burning_nodes.add(initial_node)
        else:
            raise ValueError("The initial node does not exist in the tree.")
        
        # Add a random firefighter position
        self.firefighter.add_random_initial_position()

    def propagate(self):
        new_burning_nodes = set()
        
        for node in self.state.burning_nodes:
            neighbors = self.tree.get_neighbors(node)  # Method in the Tree class to get neighboring nodes
            for neighbor in neighbors:
                if neighbor not in self.state.burned_nodes and neighbor not in self.state.burning_nodes:
                    if neighbor not in self.state.protected_nodes:    # If node is not defended, it will burn
                        new_burning_nodes.add(neighbor)
        
        # Update the state of the nodes
        self.state.burned_nodes.update(self.state.burning_nodes)
        self.state.set_burning_nodes(new_burning_nodes)

    def is_completely_burned(self):
        """
        Checa si ya no hay nodos por quemar
        """
        if not self.state.burning_nodes and not self.state.burned_nodes:
            return False

        for node in self.state.burning_nodes:
            neighbors = self.tree.get_neighbors(node)
            for neighbor in neighbors:
                if neighbor not in self.state.burned_nodes and neighbor not in self.state.burning_nodes and neighbor not in self.state.protected_nodes:
                    return False
        return True

    def update_history(self, dict_info):
        """
        Actualiza el historial de la simulacion
        """
        self.history.append(dict_info)