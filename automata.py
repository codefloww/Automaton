"""module for discrete evolving automata"""
import random


class Automata:
    def __init__(self) -> None:
        self.GENOME_SIZE = 8
        self.genome = "0" * (2 * self.GENOME_SIZE)
        self.age = 0
        self.energy = 10
        self.x = None
        self.y = None

        self.DEFAULT_ENERGY_TO_MOVE = 2

    def __str__(self) -> str:
        pass

    def _abilities_decider(self) -> dict:
        abilities_namings = [
            self.see_ability,
            self.move_ability,
            self.eat_ability,
            self.kill_ability,
            self.hybernate_ability,
            self.photosyth_ability,
            self.reproduce_ability,
            self.produce_ability,
        ]
        abilities_strength = list(
            map(
                lambda x: int(self.genome[x : x + 2]), range(0, self.GENOME_SIZE * 2, 2)
            )
        )
        abilities = {
            abilities_namings[i]: abilities_strength[i]
            for i in range(len(abilities_namings))
        }
        return abilities

    def _behavior_decider(self) -> None:
        abilities = self._abilities_decider()
        completed_action = False
        for ability in abilities:
            if abilities[ability] > 0:
                completed_action = ability(abilities[ability])
            if completed_action:
                break

    def move_ability(self, strength) -> None:
        if self.energy < self.DEFAULT_ENERGY_TO_MOVE:
            return
        x, y = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
        self.x += x
        self.y += y

    def see_ability(self, strength) -> None:
        pass

    def eat_ability(self, strength) -> None:
        pass

    def reproduce_ability(self, strength) -> None:
        pass

    def kill_ability(self, strength) -> None:
        pass

    def photosyth_ability(self, strength) -> None:
        pass

    def produce_ability(self, strength) -> None:
        pass

    def hybernate_ability(self, strength) -> None:
        pass

    def mutate(self) -> None:
        mutation_position = random.randint(0, self.GENOME_SIZE)
        self.genome = (
            self.genome[:mutation_position]
            + str(int(self.genome[mutation_position]) ^ 1)
            + self.genome[mutation_position + 1:]
        )

    def crossover(self, other) -> None:
        if not isinstance(other, Automata):
            raise TypeError("other must be an Automata")
        if self.GENOME_SIZE != other.GENOME_SIZE:
            raise ValueError("other must have the same genome size")
        crossing = random.randint(0, self.GENOME_SIZE)
        self.genome, other.genome = (
            self.genome[0:crossing] + other.genome[crossing:],
            other.genome[0:crossing] + self.genome[crossing:],
        )
        return self, other

    def get_genome(self) -> list:
        return self.genome

    def get_age(self) -> int:
        return self.age

    def get_energy(self) -> int:
        return self.energy
