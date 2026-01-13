import time
from greedyff.greedy_sim import GreedySim
from greedyff.get_candidates_utils import get_candidates
from greedyff.environment import Environment
import multiprocessing

def _worker(args):
    env, candidate, k = args
    env_copy = env.copy()
    env_copy.move(int(candidate[0]))
    damage, _ = k_steps(env_copy, k-1)
    print(f"Candidate {candidate[0]} results in damage {damage}")
    return (damage, candidate)

def k_steps_paralel(env, k):
    min_damage = float('inf')
    best_candidate = None

    if k==0:
        greedy_simulation_final = GreedySim(env=env, ff_speed=1)
        damage = greedy_simulation_final.run()
        return damage, None  

    if env.firefighter.protecting_node is not None:
        node_to_protect = env.firefighter.protecting_node
        node_time_to_reach = env.firefighter.get_distance_to_node(node_to_protect) / env.firefighter.speed
        candidates = [(node_to_protect, node_time_to_reach)]
    else:
        candidates = get_candidates(env.tree, env.state, env.firefighter)
        if not candidates:
            greedy_simulation_final = GreedySim(env=env, ff_speed=1)
            damage = greedy_simulation_final.run()
            return damage, None
    workers = multiprocessing.cpu_count()
    print(f"Using {workers} workers for parallel {k}-steps")

    jobs = []

    for candidate in candidates:
        args = (env, candidate, k)
        jobs.append(args)

    with multiprocessing.Pool(processes=workers) as pool:
        damage_results = pool.map(_worker, jobs)

    for damage, candidate in damage_results:
        if damage < min_damage:
            min_damage = damage
            best_candidate = candidate
            print(f"New best candidate {best_candidate} with damage {min_damage} at k={k}")
            best_candidate_distance = env.firefighter.get_distance_to_node(candidate[0])
        elif damage == min_damage:
            candidate_distance = env.firefighter.get_distance_to_node(candidate[0])
            if candidate_distance < best_candidate_distance:
                best_candidate = candidate
                best_candidate_distance = candidate_distance
            msg = f"Candidate {candidate[0]} ties with damage {damage}"
            msg += f" and distance {candidate_distance}"
            msg += f", selected closer one {best_candidate[0]}"
            print(msg)
    
    return min_damage, best_candidate

def k_steps(env, k):
    '''
    Perform k steps making copies of the environment for each candidate and performing a greedy simulation from there.
    '''
    min_damage = float('inf')
    best_candidate = None

    t = env.firefighter.get_remaining_time()

    if t == 0:
        env.firefighter.init_remaining_time()
        env.propagate()

    if k==0:
        greedy_simulation_final = GreedySim(env=env, ff_speed=1)
        damage = greedy_simulation_final.run()
        return damage, None  

    if env.firefighter.protecting_node is not None:
        node_to_protect = env.firefighter.protecting_node
        node_time_to_reach = env.firefighter.get_distance_to_node(node_to_protect) / env.firefighter.speed
        candidates = [(node_to_protect, node_time_to_reach)]
    else:
        candidates = get_candidates(env.tree, env.state, env.firefighter)
        if not candidates:
            greedy_simulation_final = GreedySim(env=env, ff_speed=1)
            damage = greedy_simulation_final.run()
            return damage, None
    
    for candidate in candidates:
        t = env.firefighter.get_remaining_time()

        if t <= 0:
            env.firefighter.init_remaining_time()
            env.propagate()
        env_copy = env.copy()
        t = env_copy.firefighter.get_remaining_time()
        if t == 0:
            env_copy.firefighter.init_remaining_time()
            env_copy.propagate()
        env_copy.move(int(candidate[0]))
        if t == 0:
            env_copy.firefighter.init_remaining_time()
            env_copy.propagate()
        damage, _ = k_steps(env_copy, k-1)
        if damage < min_damage:
            min_damage = damage
            best_candidate = candidate
            best_candidate_distance = env.firefighter.get_distance_to_node(candidate[0])
        elif damage == min_damage:
            candidate_distance = env.firefighter.get_distance_to_node(candidate[0])
            if candidate_distance < best_candidate_distance:
                best_candidate = candidate
                best_candidate_distance = candidate_distance
            print(f"Candidategg {candidate[0]} ties with damage {damage}, selected closer one {best_candidate[0]}")


    return min_damage, best_candidate

def rollout(d_tree, ff_position, k):
    '''
    Perform a rollout simulation on the given tree starting from the root node.
    Args:
        tree: The tree structure representing the environment.
        ff_position: The initial position of the firefighter.
        k: The number of steps to rollout at future, after that it will continue with greedy policy.
    '''
    start_time = time.perf_counter()

    solution = []
    final_damage = None

    # Initialize the environment with the directed tree, firefighter speed, and position
    env = Environment(d_tree, speed=1, ff_position=ff_position, remaining_time=1)

    # Create a GreedySim instance with the environment
    greedy_simulation = GreedySim(env=env, ff_speed=1)

    # First step: initialize fire
    env_rollout = greedy_simulation.step()

    while env_rollout.is_completely_burned() == False:
        if env_rollout.firefighter.get_remaining_time() is None:
            env_rollout.firefighter.init_remaining_time()
        
        exist_candidate = True
       
        while exist_candidate:
            if env_rollout.firefighter.get_remaining_time() == 0:
                env_rollout.firefighter.init_remaining_time()
                env_rollout.propagate()
            _, best_candidate = k_steps_paralel(env_rollout, k)
            if best_candidate is not None and int(best_candidate[0]) not in [int(node[0]) for node in solution]:
                solution.append(best_candidate)
            if best_candidate is None:
                exist_candidate = False
            else:
                env_rollout.move(int(best_candidate[0]))

    final_damage = len(env_rollout.state.burned_nodes) + len(env_rollout.state.burning_nodes)

    end_time = time.perf_counter()

    solution = [int(node[0]) for node in solution if node is not None]

    return solution, final_damage, end_time - start_time
