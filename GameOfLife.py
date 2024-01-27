from Chromosome import Chromosome, INFINITY_TABLE, Chromosome_Representation
import copy

ALIVE = 1
DEAD = 0

def count_alive_neighbors(alive_dict:set[tuple[int,int]], row:int, col:int) -> int:
    alive = 0

    positions = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                 (row, col - 1), (row, col + 1),
                 (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]

    for pos in positions:
        if pos in alive_dict:
            alive += 1

    return alive

def get_dead_neighbors(alive_dict:set[tuple[int,int]], row:int, col:int) -> list[tuple[int,int]]:
    result = []

    positions = [ (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                 (row, col - 1), (row, col + 1),
                 (row + 1, col - 1), (row + 1, col), (row + 1, col + 1) ]

    for pos in positions:
        if pos not in alive_dict:
            result.append(pos)

    return result

# Simulates the game of life for a starting representation for a set amount of generations.
# Returns a chromosome instance
def simulate(start:Chromosome_Representation) -> Chromosome:
    representation = start.get()

    if not representation:
        return Chromosome(start, 0, 0, 0, INFINITY_TABLE.NO)

    initial_size:int = len(representation)

    lifespan:int = 0
    max_size:int = initial_size
    is_infinite:INFINITY_TABLE = INFINITY_TABLE.UNKNOWN

    lookup_table = set()

    current_representation:Chromosome_Representation = start

    current_iteration_set = copy.deepcopy(representation) # alive set
    next_iteration_set = copy.deepcopy(current_iteration_set)

    while current_iteration_set and current_representation not in lookup_table:
        lookup_table.add(current_representation)

        lifespan += 1

        relevant_dead_cells:set[tuple[int,int]] = set()

        for alive_member_current_iteration in current_iteration_set: # Iterate through alive cells
            row, col = alive_member_current_iteration

            for dead_cell in get_dead_neighbors(current_iteration_set, row, col): # add relevant dead neighbor cells
                relevant_dead_cells.add(dead_cell)

            alive_neighbors_count = count_alive_neighbors(current_iteration_set, row, col)

            if alive_neighbors_count < 2 or alive_neighbors_count > 3:
                next_iteration_set.remove(alive_member_current_iteration)

        for relevant_dead_cell_current_iteration in relevant_dead_cells:
            row, col = relevant_dead_cell_current_iteration
            alive_neighbors_count = count_alive_neighbors(current_iteration_set, row, col)

            if alive_neighbors_count == 3:
                next_iteration_set.add(relevant_dead_cell_current_iteration)

        max_size = max(max_size, len(next_iteration_set))

        current_iteration_set = copy.deepcopy(next_iteration_set)

        current_representation = Chromosome_Representation(next_iteration_set)

    if current_representation in lookup_table:
        is_infinite = INFINITY_TABLE.YES

    else:
        is_infinite = INFINITY_TABLE.NO

    return Chromosome(start, lifespan, initial_size, max_size, is_infinite)

