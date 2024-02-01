from Chromosome import Chromosome


class Result:
    grid_edges:tuple[int, int]
    best_chromosome_found:Chromosome
    best_by_generation:list[Chromosome]
    evaluation_list_by_generation:list[list[float]]

    def __init__(self, grid_edges, best_chromosome_found, best_by_generation, evaluation_list_by_generation):
        self.grid_edges = grid_edges
        self.best_chromosome_found = best_chromosome_found
        self.best_by_generation = best_by_generation
        self.evaluation_list_by_generation = evaluation_list_by_generation

