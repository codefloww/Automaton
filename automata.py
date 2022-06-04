"""module for discrete evolving automata"""
import random
from environment import Environment

class Automata:
    def __init__(self, cell, env) -> None:
        self.GENOME_SIZE = 8
        self.genome = '1'*(2*self.GENOME_SIZE)
        # self.health = 10
        self.age = 0
        self.energy = 4
        self.cell = cell
        self.x = self.cell.x
        self.y = self.cell.y
        self.env = env

    def __str__(self) -> str:
        return f"{self.get_genome()} - {self.x}, {self.y}"

    def _abilities_decider(self) -> None:
        abilities_namings = [self.see_ability, self.move_ability, self.eat_ability,  self.kill_ability,self.hybernate_ability, self.photosynth_ability, self.reproduce_ability,self.produce_ability]
        abilities_strength = list(map(lambda x: int(self.genome[x:x+2], 2), range(0, self.GENOME_SIZE*2, 2)))
        abilities = {abilities_namings[i]: abilities_strength[i] for i in range(len(abilities_namings))}
        return abilities

    def _behavior_decider(self)->None:
        abilities = self._abilities_decider()
        completed_action = False
        for ability in abilities:
            if abilities[ability] > 0:
                completed_action = ability(abilities[ability], self.env)
            if completed_action:
                break

    def move_ability(self, strength, ) -> None:
        surr = self.see_ability(self._abilities_decider()[self.see_ability])
        def seek_danger():
            return [x for x in surr if x.organism != None]
        def look_for_pray():
            return [x for x in seek_danger() if x.organism.energy < self.energy] # замість self.energy підбиратимемо по силі бою, але зараз йой най буде
        def look_for_food():
            return [x for x in surr if x.cell_type == "plant"]
        danger_cells = seek_danger()
        pray_cells = look_for_pray()
        food_cells = look_for_food()

        # починаю прописувати логіку рішень
        if len(danger_cells) > 0:
            1 

    def see_ability(self, strength) -> None:
        return self.env.get_neighbors(self.x, self.y, strength)

    def eat_ability(self, strength) -> None:
        pass
    def reproduce_ability(self, strength) -> None:
        pass
    def kill_ability(self, strength) -> None:
        self
    def photosynth_ability(self, strength) -> None:
        pass
    def produce_ability(self, strength) -> None:
        self
    def hybernate_ability(self, strength) -> None:
        self.energy += strength if self.energy + strength <= 10 else 10 - self.energy


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

if __name__ == "__main__":
    env = Environment(10, 10)
    my_cell = env.get_cell(0, 0)
    my_cell.organism = Automata(my_cell, env)
    my_man = my_cell.organism
    print(my_man.move_ability(1))


