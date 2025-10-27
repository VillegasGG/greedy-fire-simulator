import time
from greedyff.greedy_sim import GreedySim
from greedyff.get_candidates_utils import get_candidates
from greedyff.environment import Environment

def k_steps(env, k):
    '''
    Perform k steps making copies of the environment for each candidate and performing a greedy simulation from there.
    '''
    if k==0:
        print(f"STEP {k} - GREEDY SIMULATION FINAL...")
        greedy_simulation_final = GreedySim(env=env, ff_speed=1, output_dir="final_greedy_output")
        damage = greedy_simulation_final.run()
        return damage, None
    

    print(f"STEP {k}...")
    min_damage = float('inf')
    best_candidate = None
    env.log_state()

    if env.firefighter.get_remaining_time() is None or env.firefighter.get_remaining_time() <= 0:
        env.firefighter.init_remaining_time()

    if env.firefighter.protecting_node is not None:
        node_to_protect = env.firefighter.protecting_node
        node_time_to_reach = env.firefighter.get_distance_to_node(node_to_protect) / env.firefighter.speed
        candidates = [(node_to_protect, node_time_to_reach)]
    else:
        candidates = get_candidates(env.tree, env.state, env.firefighter)

    if not candidates:
        greedy_simulation_final = GreedySim(env=env, ff_speed=1, output_dir="final_greedy_output")
        damage = greedy_simulation_final.run()
        return damage, None

    for candidate in candidates:
        env_copy = env.copy()
        env_copy.move(int(candidate[0]))
        if env_copy.firefighter.get_remaining_time() == 0:
            env_copy.propagate()
        env_copy.log_state()
        damage, _ = k_steps(env_copy, k-1)
        if damage < min_damage:
            min_damage = damage
            best_candidate = candidate
        print(f"Best candidate at step {k}: {best_candidate} with damage {min_damage}")
    return min_damage, best_candidate

def rollout(d_tree, ff_position, k=2):
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
    greedy_simulation = GreedySim(env=env, ff_speed=1, output_dir="rollout_output")

    # First step: initialize fire
    env_rollout = greedy_simulation.step()
    state = env_rollout.state

    print(f"Burned nodes after greedy step: {state.burned_nodes}")
    print(f"Burning nodes after greedy step: {state.burning_nodes}")
    print(f"Protected nodes after greedy step: {state.protected_nodes}")

    while env_rollout.is_completely_burned() == False:
        if env_rollout.firefighter.get_remaining_time() is None or env_rollout.firefighter.get_remaining_time() <= 0:
            env_rollout.firefighter.init_remaining_time()
        else:
            # Turno del bombero
            exist_candidate = True
            while env_rollout.firefighter.get_remaining_time() > 0 and exist_candidate:
                damage, best_candidate = k_steps(env_rollout, k)
                if best_candidate is not None and int(best_candidate[0]) not in [int(node[0]) for node in solution]:
                    solution.append(best_candidate)
                print(f"Best candidate from rollout: {best_candidate}")
                if best_candidate is None:
                    exist_candidate = False
                else:
                    env_rollout.move(int(best_candidate[0]))
                    # env_rollout.log_state()
                    print(f"ENV: Firefighter moved to protect node {best_candidate}")

            # Turno de la propagacion del fuego
            env_rollout.propagate()

    final_damage = len(env_rollout.state.burned_nodes) + len(env_rollout.state.burning_nodes)

    end_time = time.perf_counter()

    # Save report with the solution, damage, num nodes and time taken
    solution = [int(node[0]) for node in solution if node is not None]

    # with open("rollout_report.txt", "w") as f:
    #     f.write(f"Rollout Report\n")
    #     f.write(f"====================\n")
    #     f.write(f"Solution: {solution}\n")
    #     f.write(f"Damage: {final_damage}\n")
    #     f.write(f"Number of Nodes: {len(d_tree.nodes)}\n")
    #     f.write(f"Time Taken: {end_time - start_time:.4f} seconds\n")

    return solution, final_damage, end_time - start_time
