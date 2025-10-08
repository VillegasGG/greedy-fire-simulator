import json
import numpy as np
import pandas as pd
from load_past_experiments import load_results

# Load results from rollout_test_results.json
results = load_results()

# Load rollout results
with open("rollout_test_results_1.json", "r") as f:
    rollout_results_1 = json.load(f)

with open("rollout_test_results_2.json", "r") as f:
    rollout_results_2 = json.load(f)

results_1 = results[0]
results_2 = results[1]

print(f"Loaded {len(rollout_results_1)} rollout results.")
print(f"Loaded {len(rollout_results_2)} rollout results.")

dynamic_programming_results_1 = results_1["dynamic_programming"]
dynamic_programming_results_2 = results_2["dynamic_programming"]

iqcp_results_1 = results_1["iqcp"]
iqcp_results_2 = results_2["iqcp"]

ilp_results_1 = results_1["ilp"]
ilp_results_2 = results_2["ilp"]

miqcp_results_1 = results_1["miqcp"]
miqcp_results_2 = results_2["miqcp"]

greedy_results_1 = results_1["greedy"]
greedy_results_2 = results_2["greedy"]

print(f"Dynamic Programming results 1: {len(dynamic_programming_results_1)}")
print(f"Dynamic Programming results 2: {len(dynamic_programming_results_2)}")
print(f"IQCP results 1: {len(iqcp_results_1)}")
print(f"IQCP results 2: {len(iqcp_results_2)}")
print(f"ILP results 1: {len(ilp_results_1)}")
print(f"ILP results 2: {len(ilp_results_2)}")
print(f"MIQCP results 1: {len(miqcp_results_1)}")
print(f"MIQCP results 2: {len(miqcp_results_2)}")
print(f"Greedy results 1: {len(greedy_results_1)}")
print(f"Greedy results 2: {len(greedy_results_2)}")

# convert to dataframe
df_rollout_1 = pd.DataFrame(rollout_results_1)
df_rollout_2 = pd.DataFrame(rollout_results_2)
df_dynamic_programming_1 = pd.DataFrame(dynamic_programming_results_1)
df_dynamic_programming_2 = pd.DataFrame(dynamic_programming_results_2)
df_iqcp_1 = pd.DataFrame(iqcp_results_1)
df_iqcp_2 = pd.DataFrame(iqcp_results_2)
df_ilp_1 = pd.DataFrame(ilp_results_1)
df_ilp_2 = pd.DataFrame(ilp_results_2)
df_miqcp_1 = pd.DataFrame(miqcp_results_1)
df_miqcp_2 = pd.DataFrame(miqcp_results_2)
df_greedy_1 = pd.DataFrame(greedy_results_1)
df_greedy_2 = pd.DataFrame(greedy_results_2)

df_rollout_1 = df_rollout_1.drop("sequence", axis=1)
df_rollout_2 = df_rollout_2.drop("sequence", axis=1)

df_rollout_1 = df_rollout_1.drop("root", axis=1)
df_rollout_2 = df_rollout_2.drop("root", axis=1)

df_rollout_1 = df_rollout_1.rename(columns={"id": "experiment"})
df_rollout_2 = df_rollout_2.rename(columns={"id": "experiment"})

df_merged_1 = df_dynamic_programming_1.merge(df_iqcp_1, on="experiment", suffixes=('_dp', '_iqcp'), how='outer')
df_merged_1 = df_merged_1.merge(df_ilp_1, on="experiment", suffixes=('', '_ilp'), how='outer')
df_merged_1 = df_merged_1.merge(df_miqcp_1, on="experiment", suffixes=('', '_miqcp'), how='outer')
df_merged_1 = df_merged_1.merge(df_greedy_1, on="experiment", suffixes=('', '_greedy'), how='outer')
df_merged_1 = df_merged_1.merge(df_rollout_1, on="experiment", suffixes=('', '_rollout'), how='outer')  

df_merged_2 = df_dynamic_programming_2.merge(df_iqcp_2, on="experiment", suffixes=('_dp', '_iqcp'), how='outer')
df_merged_2 = df_merged_2.merge(df_ilp_2, on="experiment", suffixes=('', '_ilp'), how='outer')
df_merged_2 = df_merged_2.merge(df_miqcp_2, on="experiment", suffixes=('', '_miqcp'), how='outer')
df_merged_2 = df_merged_2.merge(df_greedy_2, on="experiment", suffixes=('', '_greedy'), how='outer')
df_merged_2 = df_merged_2.merge(df_rollout_2, on="experiment", suffixes=('', '_rollout'), how='outer')

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

# Save merged dataframes to csv
df_merged_1.to_csv("compare_results_1.csv", index=False)
df_merged_2.to_csv("compare_results_2.csv", index=False)

print("Saved compare_results_1.csv and compare_results_2.csv")