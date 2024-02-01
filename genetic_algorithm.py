import GameOfLife
from Chromosome import Chromosome
from Chromosome import Chromosome_Representation
from typing import Callable
from random import uniform
from Roulette import Roulette
from ResultsFormat import Result
import pickle
from constants import SAVE_FILE_NAME

class genetic_algorithm:
    alive_probability_in_initialization:float
    mutation_probability:float
    mutation_function:Callable[[Chromosome_Representation], Chromosome_Representation]
    crossover_probability:float
    crossover_function: Callable[[Chromosome, Chromosome], Chromosome_Representation]
    population_size:int
    num_of_generations:int
    evaluation_function:Callable[[Chromosome], float]
    max_alive_on_start:int
    grid_edges:tuple[int, int]

    def __init__(self, alive_probability_in_initialization, mutation_probability, mutation_function, crossover_probability, crossover_function, population_size, evaluation_function, grid_edges, max_alive_on_random_population, num_of_generations):

        if population_size < 2:
            raise ValueError("Population size must be at least 2.")

        self.alive_probability_in_initialization = alive_probability_in_initialization
        self.mutation_probability = mutation_probability
        self.mutation_function = mutation_function
        self.crossover_probability = crossover_probability
        self.crossover_function = crossover_function
        self.population_size = population_size
        self.evaluation_function = evaluation_function
        self.grid_edges = grid_edges
        self.max_alive_on_random_population = max_alive_on_random_population
        self.num_of_generations = num_of_generations

    def create_random_population(self) -> list[Chromosome]:
        population = []
        s = set()

        for i in range(self.population_size):
            random_representation = Chromosome_Representation.create_random_representation(self.grid_edges, self.alive_probability_in_initialization, self.max_alive_on_random_population)

            while random_representation in s:
                random_representation = Chromosome_Representation.create_random_representation(self.grid_edges, self.alive_probability_in_initialization, self.max_alive_on_random_population)

            s.add(random_representation)
            c:Chromosome = GameOfLife.simulate(random_representation, self.grid_edges, self.evaluation_function)

            population.append(c)

        return population

    def run(self):

        population:list[Chromosome] = self.create_random_population() # Create random population

        best_chromosome = population[0]
        best_chromosome_by_generation = []
        evaluation_list_by_generation = []

        representation_to_chromosome:dict[Chromosome_Representation, Chromosome] = dict()

        for i in range(self.num_of_generations):
            r:Roulette = Roulette(population, self.evaluation_function)
            next_population = []

            while len(next_population) < self.population_size:
                if r.size() < 2:
                    r = Roulette(population, self.evaluation_function)

                # pick 2 parents by roulette
                parent1:Chromosome = r.get()
                parent2:Chromosome = r.get()

                crossover_probability = uniform(0, 1)

                if crossover_probability > self.crossover_probability: # If we don't need to crossover and mutate
                    next_population.append(parent1)

                    if len(next_population) == self.population_size:
                        break

                    next_population.append(parent2)
                    continue

                offspring_representation = self.crossover_function(parent1, parent2)

                mutation_probability = uniform(0, 1)

                if mutation_probability <= self.mutation_probability:
                    offspring_representation = self.mutation_function(offspring_representation)

                if offspring_representation in representation_to_chromosome:
                    offspring:Chromosome = representation_to_chromosome[offspring_representation]

                else:
                    offspring:Chromosome = GameOfLife.simulate(offspring_representation, self.grid_edges, self.evaluation_function)
                    representation_to_chromosome[offspring_representation] = offspring

                next_population.append(offspring)

            population = next_population

            # Data related stuff
            best_chromosome_by_generation.append(max(population, key=lambda x:x.evaluation_value))
            
            if best_chromosome_by_generation[-1].evaluation_value > best_chromosome.evaluation_value:
                best_chromosome = best_chromosome_by_generation[-1]
                
            current_generation_evaluation = [x.evaluation_value for x in population]
            evaluation_list_by_generation.append(current_generation_evaluation)
            #   #   #

            print("Ended iteration number", i + 1, "/", self.num_of_generations, "of genetic algorithm")

        res = Result(self.grid_edges, best_chromosome, best_chromosome_by_generation, evaluation_list_by_generation, self.num_of_generations)

        try:
            with open(SAVE_FILE_NAME, 'wb') as file:
                pickle.dump(res, file)

        except Exception as e:
            print(e)

        print("Best chromosome found: ", best_chromosome)