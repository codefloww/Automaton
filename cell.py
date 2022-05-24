from abc import abstractmethod
from dataclasses import dataclass
@dataclass
class Cell:
    """
    A cell in the environment.
    """
    x: int
    y: int
    cell_type: str
    light: int = 10
    organism: 'Organism' = None

    @abstractmethod
    def __str__(self):
        return f"({self.x}, {self.y}) - {self.cell_type}"
    @abstractmethod
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.cell_type == other.cell_type
    @abstractmethod
    def __hash__(self):
        return hash((self.x, self.y))

if __name__ == "__main__":
    cell = Cell(1, 2, "wall", 10)
    print(cell)