from GameOfLife import GameOfLife
from Chromosome import Chromosome
from typing import Callable
from random import uniform
from Roulette import Roulette

class genetic_algorithm:
    alive_chance_in_initialization:float
    crossover_chance:float
    mutation_chance:float
    population_size:int

    game_of_life_instance:GameOfLife

    def __init__(self, alive_chance_in_initialization:float, mutation_chance:float, crossover_chance:float, crossover_function:Callable[[Chromosome, Chromosome], Chromosome.representation], population_size:int, num_of_generations:int, game_of_life_instance:GameOfLife, fitness_function:Callable[[Chromosome], float]):
        self.alive_chance_in_initialization = alive_chance_in_initialization
        self.mutation_chance = mutation_chance
        self.crossover_chance = crossover_chance
        self.crossover_function = crossover_function
        self.population_size = population_size
        self.game_of_life_instance = game_of_life_instance
        self.num_of_generations = num_of_generations
        self.fitness_function = fitness_function

    def create_random_chromosome_representation(self) -> str:
        representation = ''

        length = self.game_of_life_instance.rows * self.game_of_life_instance.cols
        for _ in range(length):
            r = uniform(0, 1)

            if r <= self.alive_chance_in_initialization:
                representation += '1'

            else:
                representation += '0'

        return representation

    def create_random_population(self) -> list[Chromosome]:
        population = []
        s = set()

        for i in range(self.population_size):
            random_representation = self.create_random_chromosome_representation()

            while random_representation in s:
                random_representation = self.create_random_chromosome_representation()

            s.add(random_representation)
            c:Chromosome = self.game_of_life_instance.simulate(random_representation)

            population.append(c)

        return population


    def run(self) -> Chromosome:
        population:list[Chromosome] = self.create_random_population() # Create random population

        for i in range(self.num_of_generations):
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
                    next_population.append(parent2)
                    continue

                temp_offspring_representation:str = self.crossover_function(parent1, parent2)
                offspring_representation = ''

                for j in range(len(temp_offspring_representation)):
                    mutation_chance = uniform(0, 1)

                    if mutation_chance <= self.mutation_chance:
                        offspring_representation += '1' if temp_offspring_representation[j] == '0' else '0'

                    else:
                        offspring_representation += temp_offspring_representation[j]


                offspring:Chromosome = self.game_of_life_instance.simulate(offspring_representation)
                next_population.append(offspring)

            population = next_population

        return max(population, key=lambda x: self.fitness_function(x))
