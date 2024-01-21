from Chromosome import Chromosome
from Chromosome import INFINITY_TABLE
from math import floor
import copy

class GameOfLife:
    rows:int
    cols:int

    num_of_generations:int

    def __init__(self, rows:int, cols:int, num_of_generations):
        self.rows = rows
        self.cols = cols
        self.num_of_generations = num_of_generations

    def get_index(self, index:int) -> tuple[int, int]:
        row = int(floor(index / self.cols))
        col = index % self.cols

        return row, col

    # Simulates the game of life for a set amount of generations.
    # Returns a tuple consisting of life span, max size, and is infinite
    def simulate(self, start:Chromosome.representation):
        if len(start) == start.count('0'):
            return 0, 0, INFINITY_TABLE.NO

        if self.rows * self.cols != len(start):
            raise ValueError("Invalid number of bits in representation")

        lifespan:int = 0
        max_size:int = start.representation.count('1')
        is_infinite:INFINITY_TABLE = INFINITY_TABLE.UNKNOWN

        lookup_table = set()
        lookup_table.add(start)

        def initialize_array():
            array = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

            for t in range(len(start)):
                row, col = self.get_index(t)
                array[row][col] = start[t]

            return array

        table = initialize_array()

        def advance() -> tuple[str, list[list[int]]]:
            def count_alive_neighbors(row, col):
                alive = 0

                positions = [ (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                              (row, col - 1), (row, col + 1),
                              (row + 1, col - 1), (row + 1, col), (row + 1, col + 1) ]

                for x, y in positions:
                    if 0 <= x < self.rows and 0 <= y < self.cols:
                        if table[x][y] == '1':
                            alive += 1

                return alive

            result = copy.copy(table)
            repr_string = ''

            for r in range(self.rows):
                for c in range(self.cols):
                    alive_neighbors = count_alive_neighbors(r, c)

                    if table[r][c] == 1:
                        repr_string += '1'

                        if alive_neighbors < 2 or alive_neighbors > 3:
                            result[r][c] = 0

                    elif table[r][c] == 0:
                        repr_string += '0'

                        if alive_neighbors == 3:
                            result[r][c] = 1
            return repr_string, result

        for i in range(self.num_of_generations):
            lifespan += 1
            next_representation_string, next_table = advance()

            if next_representation_string in lookup_table:
                is_infinite = INFINITY_TABLE.YES
                break

            if not next_representation_string:
                is_infinite = INFINITY_TABLE.NO
                break

            table = next_table

            max_size = max(max_size, next_representation_string.count('1'))

        return lifespan, max_size, is_infinite
