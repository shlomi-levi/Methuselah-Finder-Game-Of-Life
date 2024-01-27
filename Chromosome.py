from enum import Enum
from random import uniform

class INFINITY_TABLE(Enum):
    UNKNOWN = 0
    NO = 1
    YES = 2

class Chromosome_Representation:
    representation:set[tuple[int,int]]
    hash_string:str
    def get(self):
        return self.representation

    def __init__(self, representation:set[tuple[int, int]]):
        self.representation = representation
        self.hash_string = self.get_hash_string()

    def get_hash_string(self):
        ret = ''

        members = []
        for alive_location in self.representation:
            members.append(alive_location)

        members.sort(key=lambda x:x[0])

        for alive_location in members:
            ret += str(alive_location[0]) + str(alive_location[1])

        return ret

    def __hash__(self):
        return self.hash_string.__hash__()
    def __eq__(self, other):
        if not isinstance(other, Chromosome_Representation):
            return False

        for member in self.representation:
            if member not in other.representation:
                return False

        for member in other.representation:
            if member not in self.representation:
                return False

        return True

    @staticmethod
    def create_random_representation(bounding_square:int, alive_chance:float):
        representation: set[tuple[int, int]] = set()

        for i in range(bounding_square):
            for j in range(bounding_square):
                r = uniform(0, 1)
                if r <= alive_chance:
                    representation.add((i, j))

        return Chromosome_Representation(representation)

class Chromosome:
    representation:Chromosome_Representation
    hash_string:str
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

        return self.representation.__eq__(other)



