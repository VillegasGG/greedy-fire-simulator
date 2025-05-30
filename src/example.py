from greedyff.greedy_sim import GreedySim
from greedyff.tree_generator import generate_random_tree


def example_with_tree():
    n_nodes = 15
    root_degree = 5
    type_root_degree = 'min'
    ff_speed = 1
    dir_name = "output_tree"
    tree, _, root = generate_random_tree(n_nodes, root_degree, type_root_degree)

    greedy_simulation = GreedySim(ff_speed=ff_speed, output_dir=dir_name)
    greedy_simulation.run(tree, root)


def main():
    example_with_tree()
    

if __name__ == "__main__":
    main()