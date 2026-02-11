import json
import numpy as np
import pandas as pd
from load_past_experiments import load_results

k=1

exact_results_nodes = "results_moving_nodes.json"
exact_results_roots = "results_moving_roots.json"

rollout_results_nodes = f"rollout_test_results_{k}_nodes.json"
rollout_results_roots = f"rollout_test_results_{k}_roots.json"

with open(rollout_results_nodes, "r") as f:
    rollout_results_nodes = json.load(f)

with open(rollout_results_roots, "r") as f:
    rollout_results_roots = json.load(f)

result_nodes = load_results(exact_results_nodes)
result_roots = load_results(exact_results_roots)

dynamic_programming_results_1 = result_nodes["dynamic_programming"]
dynamic_programming_results_2 = result_roots["dynamic_programming"]

iqcp_results_nodes = result_nodes["iqcp"]
iqcp_results_roots = result_roots["iqcp"]

ilp_results_nodes = result_nodes["ilp"]
ilp_results_roots = result_roots["ilp"]

miqcp_results_nodes = result_nodes["miqcp"]
miqcp_results_roots = result_roots["miqcp"]

greedy_results_nodes = result_nodes["greedy"]
greedy_results_roots = result_roots["greedy"]

# convert to dataframe
df_rollout_nodes = pd.DataFrame(rollout_results_nodes)
df_rollout_roots = pd.DataFrame(rollout_results_roots)
df_dynamic_programming_nodes = pd.DataFrame(dynamic_programming_results_1)
df_dynamic_programming_roots = pd.DataFrame(dynamic_programming_results_2)
df_iqcp_nodes = pd.DataFrame(iqcp_results_nodes)
df_iqcp_roots = pd.DataFrame(iqcp_results_roots)
df_ilp_nodes = pd.DataFrame(ilp_results_nodes)
df_ilp_roots = pd.DataFrame(ilp_results_roots)
df_miqcp_nodes = pd.DataFrame(miqcp_results_nodes)
df_miqcp_roots = pd.DataFrame(miqcp_results_roots)
df_greedy_nodes = pd.DataFrame(greedy_results_nodes)
df_greedy_roots = pd.DataFrame(greedy_results_roots)

df_rollout_nodes = df_rollout_nodes.drop("sequence", axis=1)
df_rollout_roots = df_rollout_roots.drop("sequence", axis=1)

df_rollout_nodes = df_rollout_nodes.drop("root", axis=1)
df_rollout_roots = df_rollout_roots.drop("root", axis=1)

df_rollout_nodes = df_rollout_nodes.rename(columns={"id": "experiment"})
df_rollout_roots = df_rollout_roots.rename(columns={"id": "experiment"})

df_merged_1 = df_dynamic_programming_nodes.merge(df_iqcp_nodes, on="experiment", suffixes=('_dp', '_iqcp'), how='outer')
df_merged_1 = df_merged_1.merge(df_ilp_nodes, on="experiment", suffixes=('', '_ilp'), how='outer')
df_merged_1 = df_merged_1.merge(df_miqcp_nodes, on="experiment", suffixes=('', '_miqcp'), how='outer')
df_merged_1 = df_merged_1.merge(df_greedy_nodes, on="experiment", suffixes=('', '_greedy'), how='outer')
df_merged_1 = df_merged_1.merge(df_rollout_nodes, on="experiment", suffixes=('', '_rollout'), how='outer')

df_merged_2 = df_dynamic_programming_roots.merge(df_iqcp_roots, on="experiment", suffixes=('_dp', '_iqcp'), how='outer')
df_merged_2 = df_merged_2.merge(df_ilp_roots, on="experiment", suffixes=('', '_ilp'), how='outer')
df_merged_2 = df_merged_2.merge(df_miqcp_roots, on="experiment", suffixes=('', '_miqcp'), how='outer')
df_merged_2 = df_merged_2.merge(df_greedy_roots, on="experiment", suffixes=('', '_greedy'), how='outer')
df_merged_2 = df_merged_2.merge(df_rollout_roots, on="experiment", suffixes=('', '_rollout'), how='outer')

df_merged_1['optimal_rollout'] = df_merged_1['n_nodes'] - df_merged_1['final_damage']
df_merged_2['optimal_rollout'] = df_merged_2['n_nodes'] - df_merged_2['final_damage']

df_merged_1['diff_dp_rollout'] = df_merged_1['optimal_rollout'] - df_merged_1['optimal_dp']
df_merged_2['diff_dp_rollout'] = df_merged_2['optimal_rollout'] - df_merged_2['optimal_dp']

df_merged_1['diff_iqcp_rollout'] = df_merged_1['optimal_rollout'] - df_merged_1['optimal_iqcp']
df_merged_2['diff_iqcp_rollout'] = df_merged_2['optimal_rollout'] - df_merged_2['optimal_iqcp']

df_merged_1['diff_ilp_rollout'] = df_merged_1['optimal_rollout'] - df_merged_1['optimal']
df_merged_2['diff_ilp_rollout'] = df_merged_2['optimal_rollout'] - df_merged_2['optimal']

df_merged_1['diff_miqcp_rollout'] = df_merged_1['optimal_rollout'] - df_merged_1['optimal_miqcp']
df_merged_2['diff_miqcp_rollout'] = df_merged_2['optimal_rollout'] - df_merged_2['optimal_miqcp']

df_merged_1['diff_greedy_rollout'] = df_merged_1['optimal_rollout'] - df_merged_1['optimal_greedy']
df_merged_2['diff_greedy_rollout'] = df_merged_2['optimal_rollout'] - df_merged_2['optimal_greedy']

# Delete all messages columns
columns_to_drop_1 = [col for col in df_merged_1.columns if 'message' in col]
df_merged_1 = df_merged_1.drop(columns=columns_to_drop_1)
columns_to_drop_2 = [col for col in df_merged_2.columns if 'message' in col]
df_merged_2 = df_merged_2.drop(columns=columns_to_drop_2)

# Save merged dataframes to csv
df_merged_1.to_csv(f"compare_results_{k}_nodes.csv", index=False)
df_merged_2.to_csv(f"compare_results_{k}_roots.csv", index=False)

print("Saved compare_results_1.csv and compare_results_2.csv")