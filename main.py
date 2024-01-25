from genetic_algorithm import genetic_algorithm
from GameOfLife import GameOfLife
from Chromosome import Chromosome
from math import floor

alive_chance_in_initialization = 0.05
mutation_chance = 0.1
crossover_chance = 0.7
population_size = 10
num_of_generations = 10

def crossover_function(c1: Chromosome, c2: Chromosome) -> str:
    n = len(c1.representation)

    if n != len(c2.representation):
        raise ValueError("Crossover can only work on 2 chromosomes of the same size")

    return c1.representation[:floor(n/2)] + c2.representation[floor(n/2):]

def fitness_function(c:Chromosome) -> float:
    return c.max_size / c.initial_size
    # return (c.max_size / c.initial_size) + c.lifespan

def main():
    l = GameOfLife(50, 50, 500) # 50x50 grid, 500 generations of the game.
    g = genetic_algorithm(alive_chance_in_initialization, mutation_chance, crossover_chance,
                          crossover_function, population_size, num_of_generations, l, fitness_function)

    result:Chromosome = g.run()

    print("Lifespan: ", result.lifespan , "\nInitial size: ", result.initial_size, "\nMax size: ", result.max_size)


if __name__ == "__main__":
    main()