from cell import Cell
class Environment:
    """
    An environment.
    """
    def __init__(self, width, height, cell_type):
        """
        Initialize the environment.
        """
        self.width = width
        self.height = height
        self.cells = [[Cell(x, y, cell_type) for y in range(height)] for x in range(width)]
        self.cell_type = cell_type
        self.organism = None

    def __str__(self):
        """
        Return a string representation of the environment.
        """
        return "\n".join([" ".join([str(cell) for cell in row]) for row in self.cells])

    def __eq__(self, other):
        """
        Return True if the environments are equal.
        """
        return self.cells == other.cells

    def __hash__(self):
        """
        Return a hash of the environment.
        """
        return hash(tuple(tuple(row) for row in self.cells))

    def __getitem__(self, index):
        """
        Return the cell at the specified index.
        """
        return self.cells[index]

    def __setitem__(self, index, value):
        """
        Set the cell at the specified index.
        """
        self.cells[index] = value

    def __len__(self):
        """
        Return the number of cells in the environment.
        """
        return len(self.cells)

    def __iter__(self):
        """
        Return an iterator over the cells in the environment.
        """
        for row in self.cells:
            for cell in row:
                yield cell

    def get_cell(self, x, y):
        """
        Return the cell at the specified coordinates.
        """
        return self.cells[x][y]

    def set_cell(self, x, y, cell):
        """
        Set the cell at the specified coordinates.
        """
        self.cells[x][y] = cell

    def get_neighbors(self, x, y):
        pass