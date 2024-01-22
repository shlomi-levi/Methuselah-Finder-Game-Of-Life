from GameOfLife import GameOfLife
from Chromosome import Chromosome
from random import uniform

class genetic_algorithm:
    alive_chance_in_initialization:float
    crossover_chance:float
    mutation_chance:float
    population_size:int

    game_of_life_instance:GameOfLife

    def __init__(self, alive_chance_in_initialization:float, mutation_chance:float, crossover_chance:float, population_size:int, num_of_generations:int, game_of_life_instance:GameOfLife):
        self.alive_chance_in_initialization = alive_chance_in_initialization
        self.mutation_chance = mutation_chance
        self.crossover_chance = crossover_chance
        self.population_size = population_size
        self.game_of_life_instance = game_of_life_instance
        self.num_of_generations = num_of_generations

    @staticmethod
    def calculate_fitness(c:Chromosome):
        return c.lifespan + c.max_size

    @staticmethod
    def crossover(c1:Chromosome, c2:Chromosome) -> Chromosome.representation:
        # TODO: Change this
        pass

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

    def create_random_population(self):
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

    def run(self):
        population = self.create_random_population() # Create random population
        next_population = []

        for i in range(self.num_of_generations):
            while len(next_population) < self.population_size:
                # pick 2 parents by roulette
                parent1 = pick_parent
                parent2 = pick_parent

                crossover_chance = uniform(0, 1)
                if crossover_chance > self.crossover_chance:
                    next_population.add(parent1)
                    next_population.add(parent2)
                    continue

                temp_offspring_representation:str = crossover(parent1, parent2)
                offspring_representation = ''

                for j in range(len(temp_offspring_representation)):
                    mutation_chance = uniform(0, 1)

                    if mutation_chance <= self.mutation_chance:
                        offspring_representation += '1' if temp_offspring_representation[j] == '0' else '0'

                    else:
                        offspring_representation += temp_offspring_representation[j]


            offspring = create_chromosome_from_representation(offspring_representation)


