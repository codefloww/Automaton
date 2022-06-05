from dataclasses import dataclass

possible_cells = ["organism", "plant", "wall", "empty"]


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
        return f"({self.x}, {self.y}) - {self.cell_type}"

    def __eq__(self, other):

        return (
            self.x == other.x
            and self.y == other.y
            and self.cell_type == other.cell_type
            and self.organism == other.organism
        )

    def __hash__(self):
        return hash((self.x, self.y))

    def get_pos(self):
        return self.x, self.y

    def get_type(self):
        return self.cell_type

    def get_light(self):
        return self.light

    def get_organism(self):
        return self.organism


if __name__ == "__main__":
    cell = Cell(1, 2, "wall")
    print(cell)
