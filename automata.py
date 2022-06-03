"""module for discrete evolving automata"""
import random
class Automata:
    def __init__(self) -> None:
        self.GENOME_SIZE = 8
        self.genome = '0'*(2*self.GENOME_SIZE)
        self.health = 10
        self.age = 0
        self.energy = 10
        self.x = None
        self.y = None

    def __str__(self) -> str:
        pass
    def _behavior_decider(self)->None:
        pass
    def move_ability(self) -> None:
        pass
    def see_ability(self) -> None:
        pass
    def eat_ability(self) -> None:
        pass
    def reproduce_ability(self) -> None:
        pass
    def kill_ability(self) -> None:
        pass
    def photosyth_ability(self) -> None:
        pass
    def produce_ability(self) -> None:
        pass
    def hybernate_ability(self) -> None:
        pass
    def mutate(self) -> None:
        mutation_position = random.randint(0, self.GENOME_SIZE)
        self.genome = self.genome[:mutation_position] + str(int(self.genome[mutation_position])^1) + self.genome[mutation_position+1:]
        
    def crossover(self, other) -> None:
        if not isinstance(other, Automata):
            raise TypeError("other must be an Automata")
        if self.GENOME_SIZE != other.GENOME_SIZE:
            raise ValueError("other must have the same genome size")
        crossing = random.randint(0, self.GENOME_SIZE)
        self.genome, other.genome = self.genome[0:crossing] + other.genome[crossing:], other.genome[0:crossing] + self.genome[crossing:]
        return self, other

    def get_genome(self) -> list:
        return self.genome
    def get_health(self) -> int:
        return self.health
    def get_age(self) -> int:
        return self.age
    def get_energy(self) -> int:
        return self.energy
    