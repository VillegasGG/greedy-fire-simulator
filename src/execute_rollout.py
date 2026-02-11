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

def run_rollout(k):
    experiments = load_experiments()
    
    # Create new json file for results
    with open(f"rollout_test_results_{k}.json", "w") as f:
        json.dump([], f)

    for exp in experiments:
        print(f"Running test for experiment ID: {exp['id']}")
        result = test_tree_rollout(exp, k)
        
        # Append result to json file
        with open(f"rollout_test_results_{k}.json", "r") as f:
            current_results = json.load(f)

        current_results.append(result)

        with open(f"rollout_test_results_{k}.json", "w") as f:
            json.dump(current_results, f, indent=4)

    # split results into two files, one for nodes and one for roots
    with open(f"rollout_test_results_{k}.json", "r") as f:
        all_results = json.load(f)
    
    # first 60 results are for nodes, the rest are for roots
    nodes_results = all_results[:60]
    roots_results = all_results[60:]

    with open(f"rollout_test_results_{k}_nodes.json", "w") as f:
        json.dump(nodes_results, f, indent=4)

    with open(f"rollout_test_results_{k}_roots.json", "w") as f:
        json.dump(roots_results, f, indent=4)
