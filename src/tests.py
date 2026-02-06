import numpy as np
from greedyff.tree_generator import create_tree_from_sequence
from load_past_experiments import load_experiments, load_results
from rollout import rollout
from greedyff.greedy_sim import GreedySim
from greedyff.environment import Environment
import json


# generate a tree from sequence prufer, nodes positions and root

def test_tree_rollout(data, k):
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

if __name__ == "__main__":
    k=1
    experiments = load_experiments()
    

    results = []

    for exp in experiments:
        print(f"Running test for experiment ID: {exp['id']}")
        result = test_tree_rollout(exp, k)
        results.append(result)

    # Save results to a json file
    with open(f"rollout_test_results_{k}.json", "w") as f:
        json.dump(results, f, indent=4)
