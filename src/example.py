from greedyff.greedy_sim import GreedySim
from greedyff.tree_generator import generate_random_tree

def example_without_tree():
    n_nodes = 5
    root_degree = 3
    type_root_degree = 'min'
    ff_speed = 1
    dir_name = "output2"
    
    greedy_simulation = GreedySim(
        n_nodes=n_nodes, 
        root_degree=root_degree, 
        type_root_degree=type_root_degree, 
        ff_speed=ff_speed, 
        output_dir=dir_name)
    greedy_simulation.run()

def example_with_tree():
    n_nodes = 5
    root_degree = 3
    type_root_degree = 'min'
    ff_speed = 1
    dir_name = "output2"
    tree, _, root = generate_random_tree(n_nodes, root_degree, type_root_degree)

    greedy_simulation = GreedySim(
        tree=tree, 
        root=root, 
        ff_speed=ff_speed, 
        output_dir=dir_name)
    greedy_simulation.run()


def main():
    example_with_tree()
    

if __name__ == "__main__":
    main()