from genetic_algorithm import genetic_algorithm
from Chromosome import Chromosome, Chromosome_Representation
# from math import floor
# import GUI

alive_chance_in_initialization = 0.05
mutation_chance = 0.1
crossover_chance = 0.7
population_size = 10
num_of_generations = 10

def crossover_function(c1: Chromosome, c2: Chromosome) -> str:
    pass # TODO: IMPLEMENT THIS

def mutation_function(representation:Chromosome_Representation) -> Chromosome_Representation:
    pass # TODO:IMPLEMENT THIS

def fitness_function(c:Chromosome) -> float:
    return c.max_size / c.initial_size
    # return (c.max_size / c.initial_size) + c.lifespan

def main():
    g = genetic_algorithm(alive_chance_in_initialization, mutation_chance, mutation_function, crossover_chance,
                          crossover_function, population_size, num_of_generations, l, fitness_function)

    result:Chromosome = g.run()

    print("Lifespan: ", result.lifespan , "\nInitial size: ", result.initial_size, "\nMax size: ", result.max_size)

    # table = g.game_of_life_instance.initialize_array(result.representation)
    #
    # tkinter_canvas = GUI.game_of_life(table, 500, rows_and_columns)
    # tkinter_canvas.mainloop()

if __name__ == "__main__":
    main()