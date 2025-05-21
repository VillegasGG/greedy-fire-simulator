from collections import deque
from src.helpers import save_step_candidates

class GreedyStep():
    def __init__(self, tree):
        self.tree = tree
        self.burned_nodes = set()

    def show_candidates(self, message, candidates, fire_time, time_ff_reach=None):
        print(message)
        print(f'Len candidates: {len(candidates)}')
        for candidate in candidates:
            print(f'Node: {candidate} | Fire time: {fire_time[candidate]} | Time to reach: {time_ff_reach[candidate] if time_ff_reach else "Not calculated"}')
        print('-' * 50)

    def show_candidates_tuple(self, message, candidates, fire_time):
        print(message)
        print(f'Len candidates: {len(candidates)}')
        # for candidate in candidates:
        #     print(f'Node: {candidate[0]} | Time to reach: {candidate[1]} | Fire time: {fire_time[candidate[0]]}')
        # print('-' * 50)

    def get_candidate_subtree(self, node): 
        queue = []
        visited = set()
        visited.add(node)
        queue.append(node)

        while queue:
            s = queue.pop(0)
            neighbors = self.tree.get_neighbors(s)
            for neighbor in neighbors:
                if neighbor not in visited:
                    if neighbor not in self.burned_nodes:
                        queue.append(neighbor)
                        visited.add(neighbor)
            
        return visited

    def get_node_to_protect(self, candidates, firefighter, step_dir):
        """
        Selecciona el nodo a proteger basado en el subarbol más grande
        """

        candidates_depths = {}
        candidates_time = {}

        for candidate in candidates:
            subtree = self.get_candidate_subtree(candidate[0])
            depth = len(subtree)
            candidates_depths[candidate[0]] = depth
            candidates_time[candidate[0]] = candidate[1]

        if not candidates_depths:
            print('No candidates')
            return None, None
        
        max_depth = max(candidates_depths.values())
        
        node_to_protect =  [node for node, depth in candidates_depths.items() if depth == max_depth][0]
        print('Node protected: ' + str(int(node_to_protect)) + ' Safe: ' + str(max_depth) + ' nodes')

        if(firefighter.protecting_node):
            if(firefighter.protecting_node != node_to_protect):
                if candidates_depths[firefighter.protecting_node] < candidates_depths[node_to_protect]:
                    print('!'*50)
                    print(f'FF is moving to node {node_to_protect} but better option is {firefighter.protecting_node}')
                    print(candidates_depths)
                    print(f'Actual protecting node: {firefighter.protecting_node} has {candidates_depths[firefighter.protecting_node]} nodes')
                    print(f'New protecting node: {node_to_protect} has {candidates_depths[node_to_protect]} nodes')
                    print('!'*50)
            
            # Save current calculation
            save_step_candidates(candidates, candidates_depths, firefighter.protecting_node, candidates_time[firefighter.protecting_node],  firefighter.get_remaining_time(), step_dir)

            return firefighter.protecting_node, candidates_time[firefighter.protecting_node]
        
        # Save current calculation
        save_step_candidates(candidates, candidates_depths, node_to_protect, candidates_time[node_to_protect],  firefighter.get_remaining_time(), step_dir)

        return node_to_protect, candidates_time[node_to_protect]
        
    # Function to know in how many steps the fire will reach each node
    def steps_to_reach_all(self):
        
        layer = {}
        visited = set()
        
        # BFS to get the layers of the tree
        queue = deque()
        
        for node in self.burned_nodes:
            queue.append(node)
            visited.add(node)
            layer[int(node)] = 0

        while queue:
            s = queue.popleft()
            neighbors = self.tree.get_neighbors(s)

            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    layer[int(neighbor)] = layer[s] + 1

        return layer
    
    def get_final_candidates(self, candidates, fire_time, time_ff_reach, env):

        final_candidates = set()

        # Filter candidates that can be reached before the fire
        for candidate in candidates:
            time_ff_reach_candidate = time_ff_reach[candidate]
            time_to_burn_candidate = fire_time[candidate]
            remaining_time = env.firefighter.get_remaining_time()
            if time_ff_reach_candidate > time_to_burn_candidate:
                continue
            elif remaining_time < 1:
                next_step_burn = time_to_burn_candidate - 1
                next_step_ff = time_ff_reach_candidate - remaining_time
                if next_step_ff < next_step_burn:
                    final_candidates.add((candidate, time_ff_reach[candidate]))
                else:
                    continue
            else:
                if time_ff_reach[candidate] < time_to_burn_candidate:
                    final_candidates.add((candidate, time_ff_reach[candidate]))

        return final_candidates
    
    def is_protected_by_ancestor(self, node, env):
        path = env.tree.get_path_to_root(node)
        for ancestor in path:
            if ancestor in env.state.protected_nodes:
                return True
        return False

    def get_not_protected_nodes(self, env):
        candidates = set()

        unnafected_nodes = set(env.tree.nodes) - env.state.burned_nodes - env.state.protected_nodes - env.state.burning_nodes

        for element in unnafected_nodes:
            is_protected = self.is_protected_by_ancestor(element, env)
            if not is_protected:
                candidates.add(element)

        return candidates

    def get_candidates(self, env):
        burned_and_burning_nodes = env.state.burned_nodes.union(env.state.burning_nodes)
        self.burned_nodes = burned_and_burning_nodes

        first_candidates = self.get_not_protected_nodes(env)

        ff_distances = env.firefighter.get_distances_to_nodes(first_candidates)
        fire_time = self.steps_to_reach_all()

        time_ff_reach = {} # Time taken to reach each candidate
        for candidate in first_candidates:
            time_ff_reach[candidate] = ff_distances[candidate] / env.firefighter.speed
      
        final_candidates = self.get_final_candidates(first_candidates, fire_time, time_ff_reach, env)
        
        self.show_candidates_tuple("Final candidates:", final_candidates, fire_time)

        return final_candidates

    def select_action(self, env, step_dir):
        """
        - Seleccion de un nodo a proteger: se selecciona el nodo con el subarbol mas grande (aunque este mas lejos)
        - Se mueve el bombero al nodo seleccionado

        Returns False if no node to protect is found, True otherwise
        """
        
        candidates = self.get_candidates(env)
        node_to_protect, node_time = self.get_node_to_protect(candidates, env.firefighter, step_dir)
        
        if node_to_protect is not None:
            node_pos = env.tree.nodes_positions[node_to_protect]
            if(env.firefighter.get_remaining_time() >= node_time):
                env.state.protected_nodes.add(node_to_protect)
                env.firefighter.move_to_node(node_pos, node_time)
                env.firefighter.protecting_node = None
            else:
                env.firefighter.move_fraction(node_pos)
                env.firefighter.protecting_node = node_to_protect
                
            env.firefighter.print_info()
            return True

        else:
            print('No node to protect')
            return False






            


