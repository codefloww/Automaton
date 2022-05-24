
from numpy import random


class Authomaton():
    def __init__(self, x, y, genome = None) -> None:
        self.x, self.y = x, y # position of the animal on the map
        self.genome = genome if genome != None else bin(random.randint(0, 31))[2:] # currently is a bit number
        self.genome = "0" * (5 - len(self.genome)) + self.genome
        self.stance = None # stance of the authomaton
        self.age = 0

    def new_generation(self, another_genome : int):
        """
        Creates the new generation of this cell mated with another cell.
        """
        # --Це кнш якщо ми будемо враховувати ще якийсь принцип зміни геному крім мутацій.
        output = ""
        for i in range(len(self.genome)):
            output += self.genome[i] if random.randint(0,100) > 50 else another_genome[i]
        return Authomaton(self.x, self.y, output)

    def mutate(self):
        to_replace = random.randint(0, len(self.genome)-1)
        new_gene = "0" if self.genome[to_replace] == "1" else "1"
        self.genome = self.genome[:to_replace] + new_gene + self.genome[to_replace + 1:]

    def act(self, stance_to_change):
        """
        Authomathon itself. Manages the stances which define the behaviour of the cell.
        """
        self.stance = stance_to_change
        if self.stance == "":
            pass #do a thing e.g mutate, mate, die, migrate.
        elif self.stance == "":
            pass #do a thing e.g mutate, mate, die, migrate.

    def __str__(self) -> str:
        return f"{self.genome} : {self.x}, {self.y}"

auth = Authomaton(0, 0)
print(auth)
auth.mutate()
print(auth)
