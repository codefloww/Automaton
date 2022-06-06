from dataclasses import dataclass
import random
import pygame

possible_cells = ["organism", "plant", "wall", "empty"]
COEFF = 18


@dataclass
class Cell:
    """
    A cell in the environment.
    """

    x: int
    y: int
    cell_type: str = "empty"
    light: bool = False
    organism: "Automata" = None

    def __str__(self):
        # return f"({self.x}, {self.y}) - {self.cell_type}"
        return (
            "M" if self.organism != None else "_" if self.cell_type == "empty" else "f"
        )

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (
                self.x == other.x
                and self.y == other.y
                and self.cell_type == other.cell_type
                and self.organism == other.organism
            )
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def set_organism(self, automata):
        self.organism = automata

    def get_pos(self):
        return self.x, self.y

    def get_type(self):
        return self.cell_type

    def get_light(self):
        return self.light

    def get_organism(self):
        return self.organism

    def set_organism(self, organism):
        self.organism = organism


class Organism(Cell):
    radius = 10

    def __init__(self, x, y, light):
        colors = [(245, 236, 142), (247, 129, 134), (150, 110, 212)]
        super().__init__(x, y, possible_cells[0], light)

        self.color = self.set_color()

    def draw(self, screen):
        x = self.x * COEFF + COEFF // 2
        y = self.y * COEFF + COEFF // 2
        self.color = self.set_color()
        pygame.draw.circle(screen, self.color,
                           (x, y), Organism.radius)

    def set_color(self):
        colors = [(245, 236, 142), (247, 129, 134), (150, 110, 212)]
        if self.organism is None:
            return random.choice(colors)
        abilities = self.organism._abilities_decider()
        if abilities[self.organism.kill_ability] >= 2:
            return (247, 129, 134)  # red
        elif abilities[self.organism.eat_ability] >= 2:
            return (245, 236, 142)  # yellow
        elif abilities[self.organism.photosynth_ability] >= 2:
            return (110, 212, 123)  # green
        elif abilities[self.organism.produce_ability] >= 2:
            return (150, 110, 212)  # purple
        else:
            return (120, 120, 120)  # grey


class Plant(Cell):
    color = (110, 212, 123)
    radius = 7

    def __init__(self, x, y, light):
        super().__init__(x, y, possible_cells[1], light)

    def draw(self, screen):
        x = self.x * COEFF + COEFF // 2
        y = self.y * COEFF + COEFF // 2
        pygame.draw.circle(screen, Plant.color, (x, y), Plant.radius, 4)


class Wall(Cell):
    color = (51, 53, 53)
    size = (16, 16)

    def __init__(self, x, y, light):
        super().__init__(x, y, possible_cells[2], light)

    def draw(self, screen):
        x = self.x * COEFF
        y = self.y * COEFF
        pygame.draw.rect(screen, Wall.color, (x, y, Wall.size[0], Wall.size[1]))


if __name__ == "__main__":
    cell = Cell(1, 2, "wall", 10)
    print(cell)
