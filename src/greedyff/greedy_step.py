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

    def get_node_to_protect(self, candidates, firefighter):
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
            # print(f"Candidate: {candidate[0]}, Depth: {depth}, Time: {candidate[1]}")
        
        
        if(firefighter.protecting_node):
            return firefighter.protecting_node, candidates_time[firefighter.protecting_node]

        if not candidates_depths:
            return None, None
        
        max_depth = max(candidates_depths.values())
        
        node_to_protect =  [node for node, depth in candidates_depths.items() if depth == max_depth][0]

        return node_to_protect, candidates_time[node_to_protect]
    
    def select_action(self, env):
        """
        - Seleccion de un nodo a proteger: se selecciona el nodo con el subarbol mas grande (aunque este mas lejos)
        - Se mueve el bombero al nodo seleccionado

        Returns False if no node to protect is found, True otherwise
        """
        burned_and_burning_nodes = env.state.burned_nodes.union(env.state.burning_nodes)
        self.set_burned_nodes(burned_and_burning_nodes)

        candidates = get_candidates(env.tree, env.state, env.firefighter)
        node_to_protect, node_time = self.get_node_to_protect(candidates, env.firefighter)

        if node_to_protect is None:
            return False
        
        print('Node to protect: ' + str(int(node_to_protect)) + ' Time: ' + str(node_time))
        env.move(int(node_to_protect))
        return True