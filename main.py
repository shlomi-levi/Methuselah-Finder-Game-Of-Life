from genetic_algorithm import genetic_algorithm
from GameOfLife import GameOfLife
from Chromosome import Chromosome

alive_chance_in_initialization = 0.2
mutation_chance = 0.1
crossover_chance = 0.7
population_size = 50
num_of_generations = 100

def crossover_function(c1: Chromosome, c2: Chromosome) -> Chromosome.representation:
    # TODO: Change this
    pass

def fitness_function(c:Chromosome) -> float:
    return c.lifespan + c.max_size

def main():
    l = GameOfLife(50, 50, 200) # 50x50 grid, 200 generations of the game.
    g = genetic_algorithm(alive_chance_in_initialization, mutation_chance, crossover_chance,
                          crossover_function, population_size, num_of_generations, l, fitness_function)

    result:Chromosome = g.run()


if __name__ == "__main__":
    main()