from greedyff.firefighter import Firefighter
from greedyff.fire_state import FireState
import copy

class Environment:
    def __init__(self, tree, speed, ff_position, remaining_time, fire_state=None):
        self.firefighter = Firefighter(tree, speed, ff_position, remaining_time)

        if fire_state is None:
            self.state = FireState(tree)
        else:
            self.state = fire_state

    def copy(self):
        """
        Copy the environment
        """
        return copy.deepcopy(self)
    
    def start_fire(self, initial_node):
        if initial_node in self.state.tree.nodes:
            self.state.burning_nodes.add(initial_node)
        else:
            raise ValueError("The initial node does not exist in the tree.")

    def propagate(self):
        new_burning_nodes = set()
        
        for node in self.state.burning_nodes:
            neighbors = self.state.tree.get_neighbors(node)  # Method in the Tree class to get neighboring nodes
            for neighbor in neighbors:
                if neighbor not in self.state.burned_nodes and neighbor not in self.state.burning_nodes:
                    if neighbor not in self.state.protected_nodes:    # If node is not defended, it will burn
                        new_burning_nodes.add(neighbor)
        
        # Update the state of the nodes
        # print(f"Propagating fire. New burning nodes: {new_burning_nodes}")
        self.state.burned_nodes.update(self.state.burning_nodes)
        self.state.set_burning_nodes(new_burning_nodes)

    def is_completely_burned(self):
        """
        Check if there are no more nodes to burn
        """
        if not self.state.burning_nodes and not self.state.burned_nodes:
            return False

        for node in self.state.burning_nodes:
            neighbors = self.state.tree.get_neighbors(node)
            for neighbor in neighbors:
                if neighbor not in self.state.burned_nodes and neighbor not in self.state.burning_nodes and neighbor not in self.state.protected_nodes:
                    return False
        return True

    def move(self, node):
        """
        Move the firefighter to the indicated node, either completely or partially.
        Does not accept None as a node!!
        """
        if node not in self.state.tree.nodes:
            raise ValueError("The node to move to does not exist in the tree.")
        
        node_position = self.state.tree.nodes_positions[node]
        ff_remaining_time = self.firefighter.get_remaining_time()
        node_time = self.firefighter.calc_time_to_node(node)

        if ff_remaining_time >= node_time:
            self.state.protected_nodes.add(node)
            self.firefighter.move_to_node(node_position, node_time)
            self.firefighter.protecting_node = None
        else:
            self.firefighter.move_fraction(node_position)
            self.firefighter.protecting_node = node

    def log_state(self):
        print(f"Burned Nodes: {self.state.burned_nodes}")
        print(f"Burning Nodes: {self.state.burning_nodes}")
        print(f"Protected Nodes: {self.state.protected_nodes}")
        print(f"Protecting Node: {self.firefighter.protecting_node}")