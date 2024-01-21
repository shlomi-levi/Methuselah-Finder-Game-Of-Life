from GameOfLife import GameOfLife
from Chromosome import Chromosome

class genetic_algorithm:
    alive_chance_in_initialization:float
    permutation_chance:float
    crossover_change:float
    population_size:int

    game_of_life_instance:GameOfLife

    def __init__(self, alive_chance_in_initialization:float, permutation_chance:float, crossover_chance:float, population_size:int, num_of_generations:int, game_of_life_instance:GameOfLife):
        self.alive_chance_in_initialization = alive_chance_in_initialization
        self.permutation_chance = permutation_chance
        self.crossover_change = crossover_chance
        self.population_size = population_size
        self.game_of_life_instance = game_of_life_instance
        self.num_of_generations = num_of_generations

    @staticmethod
    def calculate_fitness(c:Chromosome):
        return c.lifespan + c.max_size

    def crossover(self, c1:Chromosome, c2:Chromosome) -> Chromosome.representation:
        pass
    def create_random_population(self):
        population = []
        s = set()

        for i in range(self.population_size):
            c = Chromosome(self.game_of_life_instance.rows * self.game_of_life_instance.cols, self.alive_chance_in_initialization)

            while c.representation in s:
                c = Chromosome(self.game_of_life_instance.rows * self.game_of_life_instance.cols, self.alive_chance_in_initialization)

            c.lifespan, c.max_size, c.is_infinite = self.game_of_life_instance.simulate(
                self.game_of_life_instance.num_of_generations)

        return population

    def run(self):
        population = self.create_random_population() # Create random population

        for i in range(self.num_of_generations):



