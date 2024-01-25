from enum import Enum

class INFINITY_TABLE(Enum):
    UNKNOWN = 0
    NO = 1
    YES = 2

class Chromosome:
    length:int
    representation:str
    lifespan:int
    initial_size:int
    max_size:int
    is_infinite:INFINITY_TABLE

    def __init__(self, length, representation:str, lifespan:int, initial_size:int, max_size:int, is_infinite:INFINITY_TABLE):
        self.length = length
        self.representation = representation
        self.lifespan = lifespan
        self.initial_size = initial_size
        self.max_size = max_size
        self.is_infinite = is_infinite
