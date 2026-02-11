import csv
import pandas as pd


def open_csv_to_dataframe(file_name):
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    df = pd.DataFrame(data[1:], columns=data[0])
    return df

def get_columns_to_compare(df_rollout, df_parallel):
    columns_to_compare = {}
    for index, row in df_rollout.iterrows():
        id = row['experiment']
        optimal_rollout = row['optimal_rollout']
        optimal_parallel = df_parallel[df_parallel['experiment'] == id]['optimal_rollout'].values[0]
        columns_to_compare[id] = [optimal_rollout, optimal_parallel]
    return columns_to_compare

def load_colums_to_compare(k):
    rollout_file_nodes = f"compare_results_{k}_nodes.csv"
    rollout_file_roots = f"compare_results_{k}_roots.csv"
    parallel_file_nodes = f"compare_results_parallel_{k}_nodes.csv"
    parallel_file_roots = f"compare_results_parallel_{k}_roots.csv"

    df_rollout_nodes = open_csv_to_dataframe(rollout_file_nodes)
    df_rollout_roots = open_csv_to_dataframe(rollout_file_roots)
    df_parallel_nodes = open_csv_to_dataframe(parallel_file_nodes)
    df_parallel_roots = open_csv_to_dataframe(parallel_file_roots)

    columns_to_compare_nodes = get_columns_to_compare(df_rollout_nodes, df_parallel_nodes)
    columns_to_compare_roots = get_columns_to_compare(df_rollout_roots, df_parallel_roots)

    return columns_to_compare_nodes, columns_to_compare_roots

def test_comparison():
    k = 1

    columns_to_compare_nodes, columns_to_compare_roots = load_colums_to_compare(k)
    for id, cols in columns_to_compare_nodes.items():
        rollout = cols[0]
        parallel = cols[1]
        assert int(parallel) == int(rollout), f"Optimal parallel {parallel} is different from optimal rollout {rollout} for test ID {id}"
   
    


