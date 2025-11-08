import json 
import os

# Load experiments from a directory
def load_experiments(dir="experiments"):
    files = []
    for file in os.listdir(dir):
        if file.startswith("experiments_") and file.endswith(".json"):
            files.append(os.path.join(dir, file))
    experiment_file = []
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            experiment_file.append(data)

    experiments_list = []
    for file in experiment_file:
        for experiment in file:
            experiments_list.append(experiment)
    return experiments_list

# Load results from a directory
def load_results(file_name, dir="experiments"):
    file_path = os.path.join(dir, file_name)
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data
