from cell import Cell


class Environment:
    """
    An environment.
    """

    def __init__(self, width, height, cell_type="empty", lighting=None):
        """
        Initialize the environment.
        """
        self.width = width
        self.height = height
        self.size = width * height
        self.grid = [
            [Cell(x, y, cell_type, lighting) for y in range(height)]
            for x in range(width)
        ]

    def __str__(self):
        """
        Return a string representation of the environment.
        """
        return "\n".join([" ".join([str(cell) for cell in row]) for row in self.grid])

    def __eq__(self, other):
        """
        Return True if the environments are equal.
        """
        return self.grid == other.grid

    def __hash__(self):
        """
        Return a hash of the environment.
        """
        return hash(tuple(tuple(row) for row in self.grid))

    def __getitem__(self, index):
        """
        Return the cell at the specified index.
        """
        return self.grid[index]

    def __setitem__(self, index, value):
        """
        Set the cell at the specified index.
        """
        self.grid[index] = value

    def __len__(self):
        """
        Return the number of cells in the environment.
        """
        return len(self.grid)

    def __iter__(self):
        """
        Return an iterator over the cells in the environment.
        """
        for row in self.grid:
            for cell in row:
                yield cell

    def get_cell(self, x, y):
        """
        Return the cell at the specified coordinates.
        """
        return self.grid[x][y]

    def get_cells_pos(self, cell_type=None):
        """
        Return the positions of all cells of the specified type.
        """
        cell_type = cell_type or "empty"
        cell_positions = []
        for row in self.grid:
            for cell in row:
                if cell.get_type() == cell_type:
                    cell_positions.append(cell.get_pos())
        return cell_positions

    def set_cell(self, x, y, cell):
        """
        Set the cell at the specified coordinates.
        """
        self.grid[x][y] = cell

    def get_neighbors(self, x, y):
        pass

    def get_environment_state(self):
        """
        Return the environment state.
        """
        states = []
        for row in self.grid:
            for cell in row:
                states.append(cell.get_type())

    def lighting(self, y):
        """
        Return coefficient of external illumination
        0 <= coefficient <= 1
        """
        return (self.height-y)/self.height



if __name__ == "__main__":
    env = Environment(10, 10, "empty")
    env[5][3] = Cell(5, 3, "wall")
    print(env)
