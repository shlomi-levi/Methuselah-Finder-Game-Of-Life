from genetic_algorithm import genetic_algorithm
from Chromosome import Chromosome, Chromosome_Representation
from math import ceil
from random import uniform

RESULT_FILE = 'result.data'
AVG_EVALUATION_FILE = 'evaluation.data'

alive_probability_in_initialization = 0.15
mutation_probability = 1.0
crossover_probability = 0.8
population_size = 20
max_alive_on_start = 32
num_of_generations = 20
grid_edges = (50, 50)

def crossover_function(c1: Chromosome, c2: Chromosome) -> Chromosome_Representation:
    c1_alive_members:list = c1.representation.get_members()
    c2_alive_members:list = c2.representation.get_members()

    c1_alive_members.sort(key=lambda x: x[0])
    c2_alive_members.sort(key=lambda x: x[0])

    c2_alive_members.reverse()

    new_len = min(max(len(c1_alive_members), len(c2_alive_members)), max_alive_on_start)

    result_set = set()

    result_set.update(c1_alive_members[:int(ceil(new_len/2))])

    result_set.update(c2_alive_members[:int(ceil(new_len/2))])

    return Chromosome_Representation(result_set)

# This mutation function kills living cells
def mutate(representation:Chromosome_Representation) -> Chromosome_Representation:
    inner_mutation_probability = 0.12

    rep = set(representation.get())

    members = list(rep)

    for cell in members:
        r = uniform(0, 1)

        if r <= inner_mutation_probability:
            rep.remove(cell)

    return Chromosome_Representation(rep)

def evaluation_function(c:Chromosome) -> float:
    if c.initial_size == 0:
        return 0

    # return ( (1/c.initial_size) * 0.7) + (c.max_size * 0.35) + (c.lifespan * 0.4)
    return c.max_size / c.initial_size

def main():
    g = genetic_algorithm(alive_probability_in_initialization, mutation_probability, mutate, crossover_probability,
                          crossover_function, population_size, evaluation_function, grid_edges, max_alive_on_start, num_of_generations)

    g.run(RESULT_FILE, AVG_EVALUATION_FILE)


if __name__ == "__main__":
    main()