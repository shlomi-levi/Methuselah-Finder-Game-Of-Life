from genetic_algorithm import genetic_algorithm
from Chromosome import Chromosome, Chromosome_Representation
from math import ceil
from random import uniform

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

    c2_alive_members.reverse() # Reverse order of c2 to try and avoid collisions with c1 when adding members from c2 to the set.

    new_len = min(max(len(c1_alive_members), len(c2_alive_members)), max_alive_on_start)

    result_set = set()

    complete_from:list

    if len(c1_alive_members) <= len(c2_alive_members):
        result_set.update(c1_alive_members[:min(len(c1_alive_members), int(ceil(new_len/2)))])
        complete_from = c2_alive_members

    else:
        result_set.update(c2_alive_members[:min(len(c2_alive_members), int(ceil(new_len / 2)))])
        complete_from = c1_alive_members

    added = len(result_set)

    for alive_cell in complete_from:
        if added >= new_len:
            break

        if alive_cell not in result_set:
            result_set.add(alive_cell)
            added += 1

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

    return ( (1/c.initial_size) * 0.7) + (c.max_size * 0.5) + (c.lifespan * 0.4)
    # return c.max_size / c.initial_size

def start():
    g = genetic_algorithm(alive_probability_in_initialization, mutation_probability, mutate, crossover_probability,
                          crossover_function, population_size, evaluation_function, grid_edges, max_alive_on_start, num_of_generations)

    g.run()


if __name__ == "__main__":
    start()