import random
import numpy as np

class Firefighter:
    def __init__(self, tree, speed, ff_position=None, remaining_time=None):
        self.speed = speed
        self.position = ff_position
        self.tree = tree
        self.remaining_time = remaining_time
        self.protecting_node = None

    def add_random_initial_position(self):
        '''
        Add a random firefighter position in tridimensional space with scale 1.
        '''
        random_point = (
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        )

        self.position = random_point

    def get_distance_to_node(self, node):
        position_node = self.tree.nodes_positions[node]
        return np.linalg.norm(position_node - self.position)    
    
    def get_distances_to_nodes(self, nodes):
        """
        Get distances to multiple nodes
        """
        distances = {}
        for node in nodes:
            distances[int(node)] = float(self.get_distance_to_node(node))
        return distances
    
    def init_remaining_time(self):
        self.remaining_time = 1
    
    def get_remaining_time(self):
        return self.remaining_time
    
    def decrease_remaining_time(self, time_to_decrease):
        self.remaining_time -= time_to_decrease

    def calc_new_pos(self, node_position):
        distance_between = np.linalg.norm(node_position - self.position)
        distance_can_move = self.speed * self.get_remaining_time()

        fraction = distance_can_move / distance_between

        new_x = self.position[0] + fraction * (node_position[0] - self.position[0])
        new_y = self.position[1] + fraction * (node_position[1] - self.position[1])
        new_z = self.position[2] + fraction * (node_position[2] - self.position[2])
        return (new_x, new_y, new_z)

    def move_to_node(self, node_position, node_time):
        self.position = node_position
        self.decrease_remaining_time(node_time)

    def move_fraction(self, node_position):
        new_pos = self.calc_new_pos(node_position)
        self.position = new_pos
        self.decrease_remaining_time(self.get_remaining_time())

    def calc_time_to_node(self, node):
        distance = self.get_distance_to_node(node)
        return distance / self.speed