import json

def save_results(burned_nodes, burning_nodes, protected_nodes, filename):
    results = {
        "burned_nodes": [int(node) for node in burned_nodes],
        "burning_nodes": [int(node) for node in burning_nodes],
        "protected_nodes": [int(node) for node in protected_nodes]
    }
    with open('result/' + filename, 'w') as file:
        json.dump(results, file)