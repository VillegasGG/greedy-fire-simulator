import json
import numpy as np
from greedyff.tree_generator import create_tree_from_sequence
from load_past_experiments import load_experiments, load_results
from rollout import rollout


# generate a tree from sequence prufer, nodes positions and root

def test_tree_rollout(data):
    n_nodes = data["n_nodes"]
    positions = data["nodes_positions"]
    prufer_sequence = data["sequence"]
    root = data["root"]

    sequence = np.array(prufer_sequence)
    tree = create_tree_from_sequence(sequence, add_positions=False, positions=positions)
    d_tree, _ = tree.convert_to_directed(root)

    solution, final_damage, time_taken = rollout(d_tree)

    # Return json format
    result = {
        "id": data["id"],
        "n_nodes": n_nodes,
        "root": root,
        "sequence": prufer_sequence,
        "solution": solution,
        "final_damage": final_damage,
        "time_taken": time_taken
    }

    return result



experiments = load_experiments()
# test = experiments[0]

# test_tree_rollout(test)

results = []

for exp in experiments:
    print(f"Running test for experiment ID: {exp['id']}")
    result = test_tree_rollout(exp)
    results.append(result)

# Save results to a json file
with open("rollout_test_results.json", "w") as f:
    json.dump(results, f, indent=4)
    
