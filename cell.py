from dataclasses import dataclass
possible_cells = ['organism', 'plant', 'wall', 'empty']


@dataclass
class Cell:
    """
    A cell in the environment.
    """
    x: int
    y: int
    cell_type: str = "empty"
    organism: 'Organism' = None

    def __init__(self, x, y, cell_type):
        self.x = x
        self.y = y
        self.cell_type = cell_type

    def __str__(self):
        return f"({self.x}, {self.y}) - {self.cell_type}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.cell_type == other.cell_type and self.organism == other.organism

    def __hash__(self):
        return hash((self.x, self.y))

    def get_pos(self):
        return self.x, self.y
    
    def get_type(self):
        return self.cell_type

    def get_organism(self):
        return self.organism