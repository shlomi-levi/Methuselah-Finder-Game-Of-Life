from enum import Enum
from random import uniform
from math import floor, ceil

class INFINITY_TABLE(Enum):
    UNKNOWN = 0
    NO = 1
    YES = 2

class Chromosome_Representation:
    alive_members:frozenset[tuple[int,int]]
    def get(self):
        return self.alive_members

    def get_members(self):
        members = []
        for alive_location in self.alive_members:
            members.append(alive_location)

        return members

    def __init__(self, alive_members:set[tuple[int, int]]):
        self.alive_members = frozenset(alive_members)

    def __hash__(self):
        return hash(self.alive_members)
    def __eq__(self, other):
        if not isinstance(other, Chromosome_Representation):
            return False

        for member in self.alive_members:
            if member not in other.alive_members:
                return False

        for member in other.alive_members:
            if member not in self.alive_members:
                return False

        return True

    @staticmethod
    def create_random_representation(grid_edges:tuple[int, int], alive_chance:float, max_alive:int):
        alive_members: set[tuple[int, int]] = set()
        alive_members_count = 0

        # I don't want the living members to appear at the edges of the grid
        first_x = int(ceil(0.25 * grid_edges[0]))
        last_x = int(floor(0.75 * grid_edges[0]))

        first_y = int(ceil(0.25 * grid_edges[1]))
        last_y = int(floor(0.75 * grid_edges[1]))
        # # #

        while not alive_members:
            for coor_x in range(first_x, last_x):
                for coor_y in range(first_y, last_y):
                    r = uniform(0, 1)
                    if r <= alive_chance:
                        alive_members.add((coor_x, coor_y))
                        alive_members_count += 1

                        if alive_members_count >= max_alive:
                            return Chromosome_Representation(alive_members)

        return Chromosome_Representation(alive_members)

class Chromosome:
    representation:Chromosome_Representation
    lifespan:int
    initial_size:int
    max_size:int
    is_infinite:INFINITY_TABLE
    evaluation_value:float

    def __init__(self, representation:Chromosome_Representation, lifespan:int, initial_size:int, max_size:int, is_infinite:INFINITY_TABLE):
        self.representation = representation
        self.lifespan = lifespan
        self.initial_size = initial_size
        self.max_size = max_size
        self.is_infinite = is_infinite
        self.evaluation_value = 0.0

    def set_evaluation_value(self, val):
        self.evaluation_value = val

    def __hash__(self):
        return self.representation.__hash__()

    def __eq__(self, other):
        if not isinstance(other, Chromosome):
            return False

        return self.representation.__eq__(other.representation)

    def __str__(self):
        return f"Initial size: {self.initial_size} Lifespan: {self.lifespan} Max Size: {self.max_size}"