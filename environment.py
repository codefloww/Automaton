import random


class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._create_cells_matrix()
        self.cells_objects = []

    def _create_cells_matrix(self):
        self.cells_matrix = []
        for i in range(self.height):
            self.cells_matrix.append([])
            for _ in range(self.width):
                self.cells_matrix[i].append(0)

    def evolve(self):
        for cell in self.cells_objects:
            cell.go(random.choice(["up", "down", "left", "right"]))
    # підключитись до pygame і запустити просто рандомний рух
