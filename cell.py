from dataclasses import dataclass
import random
import pygame
possible_cells = ['organism', 'plant', 'wall', 'empty']
COEFF = 18



@dataclass
class Cell:
    """
    A cell in the environment.
    """
    x: int
    y: int
    cell_type: str = "empty"
    light: int = 10

    organism: "Automata" = None

    def __str__(self):
        # return f"({self.x}, {self.y}) - {self.cell_type}"
        return "M" if self.organism != None else "_" if self.cell_type == "empty" else "f"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.cell_type == other.cell_type and self.organism == other.organism

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

    def __init__(self, x, y,  light):
        colors = [(245, 236, 142), (247, 129, 134), (150, 110, 212)]
        super().__init__(x, y, possible_cells[0], light)

        self.color = random.choice(colors)

    def draw(self, screen):
        x = self.x * COEFF + COEFF // 2
        y = self.y * COEFF + COEFF // 2
        pygame.draw.circle(screen, self.color,
                           (x, y), Organism.radius)


class Plant(Cell):
    color = (110, 212, 123)
    radius = 7

    def __init__(self, x, y,  light):
        super().__init__(x, y, possible_cells[1], light)

    def draw(self, screen):
        x = self.x * COEFF + COEFF // 2
        y = self.y * COEFF + COEFF // 2
        pygame.draw.circle(screen, Plant.color,
                           (x, y), Plant.radius, 4)


class Wall(Cell):
    color = (51, 53, 53)
    size = (16, 16)

    def __init__(self, x, y, light):
        super().__init__(x, y, possible_cells[2], light)

    def draw(self, screen):
        x = self.x * COEFF
        y = self.y * COEFF
        pygame.draw.rect(screen, Wall.color,
                         (x, y, Wall.size[0], Wall.size[1]))


if __name__ == "__main__":
    cell = Cell(1, 2, "wall", 10)
    print(cell)
