import GameOfLife
from Chromosome import Chromosome
from Chromosome import Chromosome_Representation
from typing import Callable
from random import uniform
from Roulette import Roulette
import pickle

INITIAL_CONFIGURATION_SQUARE_SIZE = 8

# Updates the result file with the best result found yet
def update_result_file(result_file, data:frozenset[tuple[int,int]]):
    with open(result_file, 'wb') as file:
        pickle.dump(data, file)

# Updates the average evaluation file with the current average evaluation array
def update_average_evaluation_file(avg_eval_file, data:list[float]):
    with open(avg_eval_file, 'wb') as file:
        pickle.dump(data, file)

class genetic_algorithm:
    alive_chance_in_initialization:float
    mutation_chance:float
    mutation_function:Callable[[Chromosome_Representation, float, int], Chromosome_Representation]
    crossover_chance:float
    crossover_function: Callable[[Chromosome, Chromosome, int], Chromosome_Representation]
    population_size:int
    num_of_generations:int
    evaluation_function:Callable[[Chromosome], float]
    initial_configuration_bounding_square:int
    max_alive_on_start:int
    border:int

    def __init__(self, alive_chance_in_initialization, mutation_chance, mutation_function, crossover_chance, crossover_function, population_size, evaluation_function, initial_config_bounding_sq, border, max_alive_on_start):

        if population_size < 2:
            raise ValueError("Population size must be at least 2.")

        self.alive_chance_in_initialization = alive_chance_in_initialization
        self.mutation_chance = mutation_chance
        self.mutation_function = mutation_function
        self.crossover_chance = crossover_chance
        self.crossover_function = crossover_function
        self.population_size = population_size
        self.evaluation_function = evaluation_function
        self.initial_configuration_bounding_square = initial_config_bounding_sq
        self.border = border
        self.max_alive_on_start = max_alive_on_start

    def create_random_population(self) -> list[Chromosome]:
        population = []
        s = set()

        for i in range(self.population_size):
            random_representation = Chromosome_Representation.create_random_representation(INITIAL_CONFIGURATION_SQUARE_SIZE, self.alive_chance_in_initialization)

            while random_representation in s:
                random_representation = Chromosome_Representation.create_random_representation(INITIAL_CONFIGURATION_SQUARE_SIZE, self.alive_chance_in_initialization)

            s.add(random_representation)
            c:Chromosome = GameOfLife.simulate(random_representation, self.border)

            population.append(c)

        return population

    def run(self, result_file:str, avg_evaluation_file:str):
        average_evaluation_list = []

        population:list[Chromosome] = self.create_random_population() # Create random population

        best_chromosome = population[0]
        update_result_file(result_file, best_chromosome.representation.get())

        representation_to_chromosome:dict[Chromosome_Representation, Chromosome] = dict()

        while True: # Iteration of the genetic algorithm
            r:Roulette = Roulette(population, self.evaluation_function)
            next_population = []

            while len(next_population) < self.population_size:
                if r.size() < 2:
                    r = Roulette(population, self.evaluation_function)

                # pick 2 parents by roulette
                parent1:Chromosome = r.get()
                parent2:Chromosome = r.get()

                crossover_chance = uniform(0, 1)

                if crossover_chance > self.crossover_chance: # If we don't need to crossover and mutate
                    next_population.append(parent1)

                    if len(next_population) == self.population_size:
                        break

                    next_population.append(parent2)
                    continue

                crossover_representation = self.crossover_function(parent1, parent2, self.max_alive_on_start)

                offspring_representation = self.mutation_function(crossover_representation, self.mutation_chance, self.initial_configuration_bounding_square)

                if offspring_representation in representation_to_chromosome:
                    offspring:Chromosome = representation_to_chromosome[offspring_representation]

                else:
                    offspring:Chromosome = GameOfLife.simulate(offspring_representation, self.border)
                    representation_to_chromosome[offspring_representation] = offspring

                next_population.append(offspring)

            population = next_population

            temp = [self.evaluation_function(x) for x in population]

            average_evaluation_list.append( sum(temp) / len(temp) ) # add average of current generation

            update_average_evaluation_file(avg_evaluation_file, average_evaluation_list)

            best_chromosome_current_iteration = max(population, key=lambda x: x.max_size)

            print(best_chromosome_current_iteration)

            if best_chromosome_current_iteration.max_size > best_chromosome.max_size:
                best_chromosome = best_chromosome_current_iteration
                update_result_file(result_file, best_chromosome.representation.get())

