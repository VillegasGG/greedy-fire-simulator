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