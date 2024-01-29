import GameOfLife
from Chromosome import Chromosome
from Chromosome import Chromosome_Representation
from typing import Callable
from random import uniform
from Roulette import Roulette

INITIAL_CONFIGURATION_SQUARE_SIZE = 8

class genetic_algorithm:
    alive_chance_in_initialization:float
    mutation_chance:float
    mutation_function:Callable[[Chromosome_Representation, int], Chromosome_Representation]
    crossover_chance:float
    crossover_function: Callable[[Chromosome, Chromosome, int], Chromosome_Representation]
    population_size:int
    num_of_generations:int
    evaluation_function:Callable[[Chromosome], float]
    initial_configuration_bounding_square:int

    def __init__(self, alive_chance_in_initialization, mutation_chance, mutation_function, crossover_chance, crossover_function, population_size, num_of_generations, evaluation_function, initial_config_bounding_sq):
        self.alive_chance_in_initialization = alive_chance_in_initialization
        self.mutation_chance = mutation_chance
        self.mutation_function = mutation_function
        self.crossover_chance = crossover_chance
        self.crossover_function = crossover_function
        self.population_size = population_size
        self.num_of_generations = num_of_generations
        self.evaluation_function = evaluation_function
        self.initial_configuration_bounding_square: initial_config_bounding_sq

    def create_random_population(self) -> list[Chromosome]:
        population = []
        s = set()

        for i in range(self.population_size):
            random_representation = Chromosome_Representation.create_random_representation(INITIAL_CONFIGURATION_SQUARE_SIZE, self.alive_chance_in_initialization)

            if not random_representation:
                print("NOT RANDOM REPRESENTATION") # todo: delete this

            while random_representation in s:
                random_representation = Chromosome_Representation.create_random_representation(INITIAL_CONFIGURATION_SQUARE_SIZE, self.alive_chance_in_initialization)

            s.add(random_representation)
            c:Chromosome = GameOfLife.simulate(random_representation)

            population.append(c)

        return population


    def run(self) -> Chromosome:
        population:list[Chromosome] = self.create_random_population() # Create random population

        for i in range(self.num_of_generations):
            print("Entering ", i, " iteration of genetic algorithm")
            r:Roulette = Roulette(population, self.evaluation_function)
            next_population = []

            while len(next_population) < self.population_size:
                if r.size() < 2:
                    r = Roulette(population, self.evaluation_function)

                # pick 2 parents by roulette
                parent1:Chromosome = r.get()
                parent2:Chromosome = r.get()

                crossover_chance = uniform(0, 1)

                if crossover_chance > self.crossover_chance:
                    next_population.append(parent1)

                    if len(next_population) == self.population_size:
                        break

                    next_population.append(parent2)
                    continue

                offspring_representation = self.crossover_function(parent1, parent2, self.initial_configuration_bounding_square ** 2)
                if not offspring_representation.get():
                    print("EEEEEEEEE")
                    exit()

                # self.mutation_function(offspring_representation, 8) # TODO: CHANGE THIS

                offspring:Chromosome = GameOfLife.simulate(offspring_representation)
                next_population.append(offspring)

            population = next_population

        return max(population, key=lambda x: self.evaluation_function(x))
