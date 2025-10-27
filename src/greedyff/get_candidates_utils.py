from collections import deque

def is_protected_by_ancestor(node, tree, state):
    path = tree.get_path_to_root(node)
    for ancestor in path:
        if ancestor in state.protected_nodes:
            return True
    return False

def is_protected_by_descendant(node, tree, state):
    path = tree.get_subtree_nodes(node)
    for descendant in path:
        if descendant in state.protected_nodes:
            return True
    return False

def get_not_protected_nodes(tree, state):
    candidates = set()
    unnafected_nodes = set(tree.nodes) - state.burned_nodes - state.protected_nodes - state.burning_nodes

    for element in unnafected_nodes:
        is_protected_anc = is_protected_by_ancestor(element, tree, state)
        is_protected_desc = is_protected_by_descendant(element, tree, state)
        if not is_protected_anc and not is_protected_desc:
            candidates.add(element)

    return candidates

# Function to know in how many steps the fire will reach each node
def steps_to_reach_all(tree, state):
    
    layer = {}
    visited = set()
    
    # BFS to get the layers of the tree
    queue = deque()

    total_burned_nodes = state.burned_nodes.union(state.burning_nodes)
    
    for node in total_burned_nodes:
        queue.append(node)
        visited.add(node)
        layer[int(node)] = 0

    while queue:
        s = queue.popleft()
        neighbors = tree.get_neighbors(s)

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                layer[int(neighbor)] = layer[s] + 1

    return layer


def get_final_candidates(candidates, fire_time, time_ff_reach, ff):

    final_candidates = set()

    # Filter candidates that can be reached before the fire
    for candidate in candidates:
        time_ff_reach_candidate = time_ff_reach[candidate]
        time_to_burn_candidate = fire_time[candidate]
        remaining_time = ff.get_remaining_time()
        if time_ff_reach_candidate > time_to_burn_candidate:
            continue
        elif remaining_time < 1:
            next_step_burn = time_to_burn_candidate - 1
            next_step_ff = time_ff_reach_candidate - remaining_time
            if next_step_ff < next_step_burn:
                final_candidates.add((candidate, time_ff_reach_candidate))
            else:
                continue
        else:
            if time_ff_reach_candidate < time_to_burn_candidate:
                final_candidates.add((candidate, time_ff_reach_candidate))

    return final_candidates

def get_candidates(tree, state, ff):
    first_candidates = get_not_protected_nodes(tree, state)

    ff_distances = ff.get_distances_to_nodes(first_candidates)
    fire_time = steps_to_reach_all(tree, state)

    time_ff_reach = {} # Time taken to reach each candidate
    for candidate in first_candidates:
        time_ff_reach[candidate] = ff_distances[candidate] / ff.speed
    
    final_candidates = get_final_candidates(first_candidates, fire_time, time_ff_reach, ff)

    return final_candidates