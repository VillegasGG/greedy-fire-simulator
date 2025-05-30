from greedyff.greedy_sim import GreedySim
from greedyff.tree_generator import generate_random_tree
from greedyff.greedy_step import GreedyStep
from greedyff.simulation import Simulation
from greedyff.environment import Environment

def example_with_initialized_sim():
    n_nodes = 50
    root_degree = 5
    type_root_degree = 'min'
    ff_speed = 1
    dir_name = "output"
    tree, _, root = generate_random_tree(n_nodes, root_degree, type_root_degree)
    d_tree, _ = tree.convert_to_directed(root)
    ff_position = (0,0,0)

    greedy_simulation = GreedySim(
        env = Environment(d_tree, ff_speed, ff_position, remaining_time=1),
        ff_speed=ff_speed, 
        output_dir=dir_name)
    
    greedy_simulation.run(tree, root)

def example_after_step():
    n_nodes = 15
    root_degree = 5
    type_root_degree = 'min'
    ff_speed = 1
    dir_name = "output"
    tree, _, root = generate_random_tree(n_nodes, root_degree, type_root_degree)
    d_tree, _ = tree.convert_to_directed(root)
    ff_position = (0,0,0)

    env = Environment(d_tree, ff_speed, ff_position, remaining_time=1)
    
    greedy_simulation = GreedySim(env=env, ff_speed=ff_speed, output_dir=dir_name)
    
    env_after1 = greedy_simulation.step()
    
    print("After step:")
    env_after1.firefighter.print_info()
    env_after1.state.print_info()
    print("***********")

    greedy_simulation2 = GreedySim(env=env_after1, ff_speed=ff_speed, output_dir="output_after")
    env2 = greedy_simulation2.step()

    print("After second step:")
    env2.firefighter.print_info()
    env2.state.print_info()
    print(env2.history)

    greedy_simulation3 = GreedySim(env=env2, ff_speed=ff_speed, output_dir="output_after2")
    env3 = greedy_simulation3.step()
    print("After third step:")
    env3.firefighter.print_info()
    env3.state.print_info()
    print(env3.history)
    print("***********")

    # end 
    greedy_simulation4 = GreedySim(env=env3, ff_speed=ff_speed, output_dir="output_after3")
    greedy_simulation4.run()

def main():
    example_after_step()
    

if __name__ == "__main__":
    main()