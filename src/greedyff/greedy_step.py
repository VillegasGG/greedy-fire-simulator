from greedyff.helpers import save_step_candidates
from greedyff.get_candidates_utils import get_candidates
from greedyff.fire_state import FireState


class GreedyStep():
    def __init__(self, env):
        self.env = env  

    def set_burned_nodes(self, burned_nodes):
        """
        Set the burned nodes
        """
        self.env.state.set_burned_nodes(burned_nodes)

    def get_candidate_subtree(self, node): 
        queue = []
        visited = set()
        visited.add(node)
        queue.append(node)

        while queue:
            s = queue.pop(0)
            neighbors = self.env.state.tree.get_neighbors(s)
            for neighbor in neighbors:
                if neighbor not in visited:
                    if neighbor not in self.env.state.burned_nodes:
                        queue.append(neighbor)
                        visited.add(neighbor)
            
        return visited

    def get_node_to_protect(self, candidates):
        """
        Select a node to protect based on the largest subtree
        """

        candidates_depths = {}
        candidates_time = {}

        for candidate in candidates:
            subtree = self.get_candidate_subtree(candidate[0])
            depth = len(subtree)
            candidates_depths[candidate[0]] = depth
            candidates_time[candidate[0]] = candidate[1]        
        
        if not candidates_depths:
            return None, None
        
        max_depth = max(candidates_depths.values())
        
        final_candidates =  [node for node, depth in candidates_depths.items() if depth == max_depth]
        node_to_protect = min(final_candidates, key=lambda n: candidates_time[n])

        return node_to_protect, candidates_time[node_to_protect]
    
    def select_action(self):
        """
        - Select a node to protect
        - Move the firefighter to that node

        Returns False if no node to protect is found, True otherwise
        """
        if self.env.firefighter.protecting_node is not None:
            self.env.move(int(self.env.firefighter.protecting_node))
            return True
        
        candidates = get_candidates(self.env.state.tree, self.env.state, self.env.firefighter)
        node_to_protect, node_time = self.get_node_to_protect(candidates)

        if node_to_protect is None:
            return False
        
        self.env.move(int(node_to_protect))
        return True