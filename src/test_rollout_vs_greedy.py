import numpy as np
import pytest
from greedyff.tree_generator import create_tree_from_sequence
from load_past_experiments import load_experiments, load_results
from rollout import rollout
from greedyff.greedy_sim import GreedySim
from greedyff.environment import Environment
import json


# generate a tree from sequence prufer, nodes positions and root

def run_rollout(data, k):
    n_nodes = data["n_nodes"]
    positions = data["nodes_positions"]
    prufer_sequence = data["sequence"]
    root = data["root"]
    initial_ff_position = data["initial_firefighter_position"]
    sequence = np.array(prufer_sequence)
    tree = create_tree_from_sequence(sequence, add_positions=False, positions=positions)
    d_tree, _ = tree.convert_to_directed(root)

    solution, final_damage, time_taken = rollout(d_tree, ff_position=initial_ff_position, k=k)

    # Return json format
    result = {
        "id": data["id"],
        "n_nodes": n_nodes,
        "root": root,
        "sequence": prufer_sequence,
        "solution": solution,
        "final_damage": final_damage,
        "time_taken": time_taken,
    }

    return result

def run_for_id(id_test, k):
    experiments = load_experiments()
    test = experiments[id_test-1]
    exp_id = test["id"]
    n_nodes = test["n_nodes"]
    positions = test["nodes_positions"]
    prufer_sequence = test["sequence"]
    root = test["root"]
    initial_ff_position = test["initial_firefighter_position"] 
    
    print(f"Experiment ID: {exp_id}")
    print(f"Nodes: {n_nodes}")
    print(f"Root: {root}")
    print(f"Initial firefighter position: {initial_ff_position}")

    sequence = np.array(prufer_sequence)
    tree = create_tree_from_sequence(sequence, add_positions=False, positions=positions)
    d_tree, _ = tree.convert_to_directed(root)

    print("GREEDY")

    env = Environment(tree=d_tree, speed=1, ff_position=initial_ff_position, remaining_time=1)
    g_sim = GreedySim(env=env, ff_speed=1)
    damage = g_sim.run()

    print(f"Experiment ID: {exp_id}")
    print(f"Nodes: {n_nodes}")
    print(f"Greedy damage: {damage}")

    positions = test["nodes_positions"]

    print("ROLLOUT")
    result = run_rollout(test, k)
    print(result)

    optimal_greedy = n_nodes - damage
    optimal_rollout = n_nodes - result["final_damage"]

    return optimal_greedy, optimal_rollout

@pytest.mark.parametrize("id_test, k", [
    (2, 1),
    (10, 1),
    (16, 1),
    (56, 1),
])
def test_rollout_is_better_or_equal(id_test, k):
    optimal_greedy, optimal_rollout = run_for_id(id_test, k)
    assert int(optimal_rollout) >= int(optimal_greedy), f"Optimal rollout {optimal_rollout} is not better than optimal greedy {optimal_greedy} for test ID {id_test}"
    
