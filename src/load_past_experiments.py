import json 
import os

# Load experiments from a directory
def load_experiments(dir):
    files = []
    for file in os.listdir(dir):
        if file.startswith("experiments_") and file.endswith(".json"):
            files.append(os.path.join(dir, file))
    experiment_file = []
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            experiment_file.append(data)
    return experiment_file

# Load results from a directory
def load_results(dir):
    files = []
    for file in os.listdir(dir):
        if file.startswith("results_") and file.endswith(".json"):
            files.append(os.path.join(dir, file))
    results_file = []
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            results_file.append(data)
    return results_file

dir = "experiments"
files = load_experiments(dir)
print(f"Loaded {len(files)} experiment files from {dir} folder.")

experiments = []
for file in files:
    for experiment in file:
        experiments.append(experiment)
print(f"Loaded {len(experiments)} experiments from {dir} folder.")

files_results = load_results(dir)
print(f"Loaded {len(files_results)} results files from {dir} folder.")
results = []
for file in files_results:
    for result in file:
        results.append(result)
print(f"Loaded {len(results)} results from {dir} folder.")