import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from simulation import Simulation
from config_tree import my_tree
from greedy_step import GreedyStep

def main():
    greedy_simulation = Simulation(GreedyStep(my_tree), my_tree)
    my_tree.save_positions_to_json("data/positions.json")
    my_tree.save_edges_to_json("data/edges.json")
    greedy_simulation.run_simulation()
 
if __name__ == "__main__":
    main()


# Checar como paralelizar rollout con cuda o hilos