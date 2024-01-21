from enum import Enum
from random import random

class INFINITY_TABLE(Enum):
    UNKNOWN = 0
    NO = 1
    YES = 2

class Chromosome:
    length:int
    representation:str
    lifespan:int
    max_size:int
    is_infinite:INFINITY_TABLE

    def create_random_chromosome(self, alive_chance:float):
        self.representation = ''

        for _ in range(self.length):
            r = random()

            if r <= alive_chance:
                self.representation += '1'

            else:
                self.representation += '0'

    def __init__(self, length, alive_chance:float):
        self.len = length

        self.create_random_chromosome(alive_chance)
