from Chromosome import Chromosome
from Chromosome import INFINITY_TABLE
from math import floor
import copy

ALIVE=1
DEAD=0

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

    # Advance one step in the game of life
    def advance(self, table:list[list[int]]) -> tuple[str, list[list[int]]]:
        def count_alive_neighbors(row, col):
            alive = 0

            positions = [ (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                          (row, col - 1), (row, col + 1),
                          (row + 1, col - 1), (row + 1, col), (row + 1, col + 1) ]

            for x, y in positions:
                if 0 <= x < self.rows and 0 <= y < self.cols:
                    if table[x][y] == ALIVE:
                        alive += 1

            return alive

        result = copy.copy(table)
        repr_string = ''

        for r in range(self.rows):
            for c in range(self.cols):
                alive_neighbors = count_alive_neighbors(r, c)

                if table[r][c] == ALIVE:
                    if alive_neighbors < 2 or alive_neighbors > 3:
                        result[r][c] = DEAD

                elif table[r][c] == DEAD:
                    if alive_neighbors == 3:
                        result[r][c] = ALIVE

                repr_string += str(result[r][c])

        if repr_string.count('0') == len(repr_string):
            return None, result # type:ignore

        return repr_string, result

    # Initializes the table for the game of life
    def initialize_array(self, start:str):
        array = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        for t in range(len(start)):
            row, col = self.get_index(t)
            array[row][col] = int(start[t])

        return array

    # Simulates the game of life for a starting representation for a set amount of generations.
    # Returns a chromosome instance
    def simulate(self, start:str) -> Chromosome:
        length = len(start)

        if length == start.count('0'):
            return Chromosome(length, start, 0, 0, 0, INFINITY_TABLE.NO)

        initial_size:int = start.count('1')

        if self.rows * self.cols != len(start):
            raise ValueError("Invalid number of bits in representation")

        lifespan:int = 0
        max_size:int = initial_size
        is_infinite:INFINITY_TABLE = INFINITY_TABLE.UNKNOWN

        lookup_table = set()
        lookup_table.add(start)

        table = self.initialize_array(start)

        for i in range(self.num_of_generations):
            lifespan += 1
            next_representation_string, next_table = self.advance(table)

            if not next_representation_string:
                print("DIES")
                is_infinite = INFINITY_TABLE.NO
                break

            if next_representation_string in lookup_table:
                is_infinite = INFINITY_TABLE.YES
                break

            table = next_table

            max_size = max(max_size, next_representation_string.count('1'))

        return Chromosome(length, start, lifespan, initial_size, max_size, is_infinite)
