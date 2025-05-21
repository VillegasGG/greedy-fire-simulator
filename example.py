from src.greedysim import GreedySim

def main():
    n_nodes = 13
    root_degree = 5
    type_root_degree = 'min'
    
    greedy_simulation = GreedySim(n_nodes, root_degree, type_root_degree)
    greedy_simulation.run()

if __name__ == "__main__":
    main()