import json
import os

def save_results(burned_nodes, burning_nodes, protected_nodes, filename, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    file_route = output_dir / filename

    results = {
        "burned_nodes": [int(node) for node in burned_nodes],
        "burning_nodes": [int(node) for node in burning_nodes],
        "protected_nodes": [int(node) for node in protected_nodes]
    }
    with open(file_route, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=2)

def save_history(history, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    file_route = output_dir / "history.json"
    with open(file_route, 'w', encoding='utf-8') as file:
        json.dump(history, file, indent=2)

def save_step_candidates(candidates, depths,  node_selected, time, remaining_time, step_dir):
    file_route = step_dir / f"candidates_{remaining_time}.json"
    
    with open(file_route, 'w', encoding='utf-8') as file:
        json.dump({
            "candidates": [(int(node[0]), float(node[1])) for node in candidates],
            "depths": {int(node): int(depth) for node, depth in depths.items()},
            "node_selected": int(node_selected),
            "time": float(time),
            "remaining_time": float(remaining_time)
        }, file, indent=2)
    file.close()