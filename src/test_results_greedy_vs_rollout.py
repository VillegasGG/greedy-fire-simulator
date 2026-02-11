import csv
import pandas as pd

def load_columns_to_compare(file_name):

    # open csv file and save as dataframe
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    df = pd.DataFrame(data[1:], columns=data[0])
    
    # get columns to compare as dict id: [col1, col2]
    columns_to_compare = {}
    for index, row in df.iterrows():
        id = row['experiment']
        col1 = row['optimal_greedy']
        col2 = row['optimal_rollout']
        columns_to_compare[id] = [col1, col2]

    return columns_to_compare


def test_comparison():
    file = "compare_results_1_nodes.csv"
    columns_to_compare = load_columns_to_compare(file)

    for id, cols in columns_to_compare.items():
        greedy = cols[0]
        rollout = cols[1]
        assert int(rollout) >= int(greedy), f"Optimal rollout {rollout} is not better than optimal greedy {greedy} for test ID {id}"

