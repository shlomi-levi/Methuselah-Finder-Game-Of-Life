from enum import Enum
from random import uniform

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
    def create_random_representation(bounding_square:int, alive_chance:float):
        alive_members: set[tuple[int, int]] = set()

        while not alive_members:
            for i in range(bounding_square):
                for j in range(bounding_square):
                    r = uniform(0, 1)
                    if r <= alive_chance:
                        alive_members.add((i, j))

        return Chromosome_Representation(alive_members)

class Chromosome:
    representation:Chromosome_Representation
    lifespan:int
    initial_size:int
    max_size:int
    is_infinite:INFINITY_TABLE

    def __init__(self, representation:Chromosome_Representation, lifespan:int, initial_size:int, max_size:int, is_infinite:INFINITY_TABLE):
        self.representation = representation
        self.lifespan = lifespan
        self.initial_size = initial_size
        self.max_size = max_size
        self.is_infinite = is_infinite

    def __hash__(self):
        return self.representation.__hash__()

    def __eq__(self, other):
        if not isinstance(other, Chromosome):
            return False

        return self.representation.__eq__(other.representation)

    def __str__(self):
        return f"Initial size: {self.initial_size} Lifespan: {self.lifespan} Max Size: {self.max_size}"