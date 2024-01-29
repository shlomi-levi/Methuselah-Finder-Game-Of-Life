from genetic_algorithm import genetic_algorithm
from Chromosome import Chromosome, Chromosome_Representation
from math import floor, ceil
# import GUI

alive_chance_in_initialization = 0.1
mutation_chance = 0.1
crossover_chance = 0.7
population_size = 20
num_of_generations = 3000
initial_configuration_bounding_square = 8

def crossover_function(c1: Chromosome, c2: Chromosome, max_alive:int) -> Chromosome_Representation:
    c1_alive_members:list = c1.representation.get_members()
    c2_alive_members:list = c2.representation.get_members()

    c1_alive_members.sort(key=lambda x: x[0])
    c2_alive_members.sort(key=lambda x: x[0])

    new_len = min(max(len(c1_alive_members), len(c2_alive_members)), max_alive)

    result_set = set()

    for i in range(int(ceil(new_len / 2))):
        result_set.add(c1_alive_members[i])

    j = 0
    for i in range(int(ceil(new_len / 2)), new_len):
        result_set.add(c2_alive_members[j])
        j += 1

    return Chromosome_Representation(result_set)

def mutation_function(representation:Chromosome_Representation, initial_config_bounding_square:int) -> Chromosome_Representation:
    return representation
    # TODO:IMPLEMENT THIS


def evaluation_function(c:Chromosome) -> float:
    if c.initial_size == 0:
        return 0

    return c.max_size / c.initial_size
    # return (c.max_size / c.initial_size) + c.lifespan

def main():
    g = genetic_algorithm(alive_chance_in_initialization, mutation_chance, mutation_function, crossover_chance,
                          crossover_function, population_size, num_of_generations, evaluation_function, initial_configuration_bounding_square)

    result:Chromosome = g.run()

    print("Lifespan: ", result.lifespan , "\nInitial size: ", result.initial_size, "\nMax size: ", result.max_size)

    # table = g.game_of_life_instance.initialize_array(result.representation)
    #
    # tkinter_canvas = GUI.game_of_life(table, 500, rows_and_columns)
    # tkinter_canvas.mainloop()

if __name__ == "__main__":
    main()