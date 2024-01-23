from genetic_algorithm import genetic_algorithm
from GameOfLife import GameOfLife
from Chromosome import Chromosome

alive_chance_in_initialization = 0.2
mutation_chance = 0.1
crossover_chance = 0.7
population_size = 50

def main():
    l = GameOfLife(50, 50, 200) # 50x50 grid, 200 generations of the game.
    g = genetic_algorithm(alive_chance_in_initialization, mutation_chance, crossover_chance, population_size, 100, l)

    result:Chromosome = g.run()


if __name__ == "__main__":
    main()