from Chromosome import Chromosome, Chromosome_Representation
from typing import Callable

# Counts and returns the number of neighbors that are alive, relative to the cell in (row, col)
def count_alive_neighbors(alive_dict:set[tuple[int,int]], row:int, col:int, grid_edges:tuple[int, int]) -> int:
    alive = 0

    positions = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                 (row, col - 1), (row, col + 1),
                 (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]

    for pos in positions:
        if not 0 <= pos[0] < grid_edges[0]:
            continue

        if not 0 <= pos[1] < grid_edges[1]:
            continue

        if pos in alive_dict:
            alive += 1

    return alive

# Returns a list consisting of all the dead neighbors that the cel in (row, col) has.
def get_dead_neighbors(alive_set, row:int, col:int, grid_edges:tuple[int, int]) -> list[tuple[int,int]]:
    result = []

    positions = [ (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                 (row, col - 1), (row, col + 1),
                 (row + 1, col - 1), (row + 1, col), (row + 1, col + 1) ]

    for pos in positions:
        if not 0 <= pos[0] < grid_edges[0]:
            continue

        if not 0 <= pos[1] < grid_edges[1]:
            continue

        if pos not in alive_set:
            result.append(pos)

    return result

# Simulates the game of life for a starting configuration.
# Returns a chromosome instance
def simulate(start:Chromosome_Representation, grid_edges:tuple[int, int], evaluation_function:Callable[[Chromosome], float]) -> Chromosome:
    representation = start.get() # Get the frozen set that consists of living cells

    if not representation: # If there are no living cells
        return Chromosome(start, 0, 0, 0)

    initial_size:int = len(representation)

    lifespan:int = 0
    max_size:int = initial_size

    lookup_table = set()

    current_representation:Chromosome_Representation = start

    current_iteration_set = set(representation)
    next_iteration_set = current_iteration_set.copy()

    while current_iteration_set and current_representation not in lookup_table:
        lookup_table.add(current_representation)

        lifespan += 1

        relevant_dead_cells:set[tuple[int,int]] = set()

        for alive_cell in current_iteration_set: # Iterate through alive cells
            row, col = alive_cell

            relevant_dead_cells.update(get_dead_neighbors(current_iteration_set, row, col, grid_edges)) # Add relevant dead neighbor cells

            alive_neighbors_count = count_alive_neighbors(current_iteration_set, row, col, grid_edges)

            if alive_neighbors_count < 2 or alive_neighbors_count > 3:
                next_iteration_set.remove(alive_cell)

        for dead_cell in relevant_dead_cells: # Iterate through dead cells
            row, col = dead_cell
            alive_neighbors_count = count_alive_neighbors(current_iteration_set, row, col, grid_edges) # Get count of living cells that the current dead cell has

            if alive_neighbors_count == 3:
                next_iteration_set.add(dead_cell) # If the current dead cell has exactly 3 living neighbors, resucitate it

        max_size = max(max_size, len(next_iteration_set))

        current_iteration_set = next_iteration_set.copy()

        current_representation = Chromosome_Representation(next_iteration_set)

    c = Chromosome(start, lifespan, initial_size, max_size)
    c.set_evaluation_value(evaluation_function(c))
    return c

