from greedyff.helpers import save_step_candidates
from greedyff.get_candidates_utils import get_candidates

class GreedyStep():
    def __init__(self, tree):
        self.tree = tree
        self.burned_nodes = set()

    def set_burned_nodes(self, burned_nodes):
        """
        Set the burned nodes
        """
        self.burned_nodes = burned_nodes

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
                    print(f'Actual protecting node: {firefighter.protecting_node} has {candidates_depths[firefighter.protecting_node]} nodes')
                    print(f'New protecting node: {node_to_protect} has {candidates_depths[node_to_protect]} nodes')
                    print('!'*50)
            
            # Save current calculation
            save_step_candidates(candidates, candidates_depths, firefighter.protecting_node, candidates_time[firefighter.protecting_node],  firefighter.get_remaining_time(), step_dir)

            return firefighter.protecting_node, candidates_time[firefighter.protecting_node]
        
        # Save current calculation
        save_step_candidates(candidates, candidates_depths, node_to_protect, candidates_time[node_to_protect],  firefighter.get_remaining_time(), step_dir)

        return node_to_protect, candidates_time[node_to_protect]
    
    def select_action(self, env, step_dir):
        """
        - Seleccion de un nodo a proteger: se selecciona el nodo con el subarbol mas grande (aunque este mas lejos)
        - Se mueve el bombero al nodo seleccionado

        Returns False if no node to protect is found, True otherwise
        """
        burned_and_burning_nodes = env.state.burned_nodes.union(env.state.burning_nodes)
        self.set_burned_nodes(burned_and_burning_nodes)

        candidates = get_candidates(env.tree, env.state, env.firefighter)
        node_to_protect, node_time = self.get_node_to_protect(candidates, env.firefighter, step_dir)
        
        if node_to_protect is not None:
            print('Node to protect: ' + str(int(node_to_protect)) + ' Time: ' + str(node_time))
            node_pos = env.tree.nodes_positions[node_to_protect]
            if(env.firefighter.get_remaining_time() >= node_time):
                env.state.protected_nodes.add(node_to_protect)
                env.firefighter.move_to_node(node_pos, node_time)
                env.firefighter.protecting_node = None
                env.update_history({
                    "step": env.firefighter.get_remaining_time(),
                    "burned_nodes": [int(node) for node in env.state.burned_nodes],
                    "burning_nodes": [int(node) for node in env.state.burning_nodes],
                    "protected_nodes": [int(node) for node in env.state.protected_nodes],
                    "firefighter_position": [float(pos) for pos in env.firefighter.position]
                })
            else:
                env.firefighter.move_fraction(node_pos)
                env.firefighter.protecting_node = node_to_protect
                
            env.firefighter.print_info()
            return True

        else:
            print('No node to protect')
            return False






            


