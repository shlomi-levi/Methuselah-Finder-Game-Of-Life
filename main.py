from genetic_algorithm import genetic_algorithm
from Chromosome import Chromosome, Chromosome_Representation
from math import ceil
from random import uniform
import GUI

FILE_NAME = 'results.data'

alive_chance_in_initialization = 0.15
mutation_chance = 0.15
crossover_chance = 0.8
population_size = 20
initial_configuration_bounding_square = 10
max_alive_on_start = 40
border = 200

def crossover_function(c1: Chromosome, c2: Chromosome, max_alive:int) -> Chromosome_Representation:
    c1_alive_members:list = c1.representation.get_members()
    c2_alive_members:list = c2.representation.get_members()

    c1_alive_members.sort(key=lambda x: x[0])
    c2_alive_members.sort(key=lambda x: x[0])

    c2_alive_members.reverse()

    new_len = min(max(len(c1_alive_members), len(c2_alive_members)), max_alive)

    result_set = set()

    result_set.update(c1_alive_members[:int(ceil(new_len/2))])

    result_set.update(c2_alive_members[:int(ceil(new_len/2))])

    return Chromosome_Representation(result_set)

def mutate(representation:Chromosome_Representation, m_chance:float, initial_config_bounding_square:int) -> Chromosome_Representation:
    rep = set(representation.get())

    for i in range(initial_config_bounding_square):
        for j in range(initial_config_bounding_square):
            r = uniform(0, 1)

            if r > m_chance: # If we don't need to mutate this square
                continue

            # If we do need to mutate this square
            if (i,j) in rep:
                rep.remove( (i,j) )

            else:
                rep.add( (i, j) )

    return Chromosome_Representation(rep)

def evaluation_function(c:Chromosome) -> float:
    if c.initial_size == 0:
        return 0

    # return ( (1/c.initial_size) * 0.7) + (c.max_size * 0.35) + (c.lifespan * 0.4)
    return c.max_size / c.initial_size

def main():
    g = genetic_algorithm(alive_chance_in_initialization, mutation_chance, mutate, crossover_chance,
                          crossover_function, population_size, evaluation_function, initial_configuration_bounding_square, border, max_alive_on_start)

    g.run("b")

    # rows_and_columns = 400
    #
    # table = [ [0 for _ in range(rows_and_columns)] for _ in range(rows_and_columns)]
    #
    # k = [(4, 0), (5, 4), (5, 1), (5, 7), (7, 4), (7, 1), (4, 5), (5, 0), (3, 6), (5, 3), (0, 4), (2, 1), (6, 1), (7, 0), (7, 6), (4, 1), (4, 4), (5, 5), (1, 1), (2, 6), (7, 5)]
    #
    # for t in k:
    #     table [ t[0] ] [ t[1] ] = 1
    #
    # tkinter_canvas = GUI.game_of_life(table, 500, rows_and_columns)
    # tkinter_canvas.mainloop()

if __name__ == "__main__":
    main()