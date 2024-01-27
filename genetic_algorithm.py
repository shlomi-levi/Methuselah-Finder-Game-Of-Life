import GameOfLife
from Chromosome import Chromosome
from Chromosome import Chromosome_Representation
from typing import Callable
from random import uniform
from Roulette import Roulette

INITIAL_CONFIGURATION_SQUARE_SIZE = 8

class genetic_algorithm:
    alive_chance_in_initialization:float
    crossover_chance:float
    mutation_chance:float
    population_size:int

    game_of_life_instance:GameOfLife

    def __init__(self, alive_chance_in_initialization:float, mutation_chance:float, mutation_function, crossover_chance:float, crossover_function:Callable[[Chromosome, Chromosome], str], population_size:int, num_of_generations:int, game_of_life_instance:GameOfLife, fitness_function:Callable[[Chromosome], float]):
        self.alive_chance_in_initialization = alive_chance_in_initialization
        self.mutation_chance = mutation_chance
        self.mutation_function = mutation_function
        self.crossover_chance = crossover_chance
        self.crossover_function = crossover_function
        self.population_size = population_size
        self.game_of_life_instance = game_of_life_instance
        self.num_of_generations = num_of_generations
        self.fitness_function = fitness_function

    def create_random_population(self) -> list[Chromosome]:
        population = []
        s = set()

        for i in range(self.population_size):
            print(i)
            random_representation = Chromosome_Representation.create_random_representation(INITIAL_CONFIGURATION_SQUARE_SIZE, self.alive_chance_in_initialization)

            while random_representation in s:
                random_representation = Chromosome_Representation.create_random_representation(INITIAL_CONFIGURATION_SQUARE_SIZE, self.alive_chance_in_initialization)

            s.add(random_representation)
            c:Chromosome = self.game_of_life_instance.simulate(random_representation)

            population.append(c)

        return population


    def run(self) -> Chromosome:
        population:list[Chromosome] = self.create_random_population() # Create random population

        for i in range(self.num_of_generations):
            print("Entering ", i, " iteration of genetic algorithm")
            r:Roulette = Roulette(population, self.fitness_function)
            next_population = []

            while len(next_population) < self.population_size:
                if r.size() < 2:
                    r = Roulette(population, self.fitness_function)

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

                offspring_representation = self.crossover_function(parent1, parent2)

                self.mutate(offspring_representation)

                offspring:Chromosome = GameOfLife.simulate(offspring_representation)
                next_population.append(offspring)

            population = next_population

        return max(population, key=lambda x: self.fitness_function(x))
