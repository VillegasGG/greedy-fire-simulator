from greedy.greedy_step import GreedyStep
from firefighter import Firefighter
from fire_state import FireState
import copy

class Environment:
    def __init__(self, tree):
        self.tree = tree
        self.state = FireState(tree)
        self.firefighter = Firefighter(tree)

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


