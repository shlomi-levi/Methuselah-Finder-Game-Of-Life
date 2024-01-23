from Chromosome import Chromosome
from random import uniform

class Roulette:
    __probabilities_list__:list[float]
    __fitness_function__:callable
    __total_fitness__:float
    __participants__:list[Chromosome]

    def calculate_probabilities(self):
        last_probability = 0
        self.__probabilities_list__ = []

        for c in self.__participants__:
            current_participant_probability = self.__fitness_function__(c) / self.__total_fitness__

            last_probability += current_participant_probability

            self.__probabilities_list__.append(last_probability)

    def size(self):
        return len(self.__participants__)
    def is_empty(self):
        return len(self.__participants__) == 0

    def get(self) -> Chromosome:
        if self.is_empty():
            raise ValueError("Roulette is empty")

        r = uniform(0, 1)

        chosen_index = 0

        if len(self.__participants__) > 1:
            for i in range(1, len(self.__probabilities_list__) - 1):
                if self.__probabilities_list__[i - 1] <= r <= self.__probabilities_list__[i + 1]:
                    chosen_index = i
                    break

        chosen_element:Chromosome = self.__participants__.pop(chosen_index)
        self.__total_fitness__ -= self.__fitness_function__(chosen_element)

        self.calculate_probabilities()

        return chosen_element


    def __init__(self, participants:list[Chromosome], fitness_function):
        self.__participants__ = participants
        self.__fitness_function__ = fitness_function

        fitness_list = [self.__fitness_function__(x) for x in self.__participants__]
        self.__total_fitness__ = sum(fitness_list)

        self.calculate_probabilities()
