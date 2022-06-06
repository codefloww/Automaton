from cell import Cell
from automata import Automata


class Environment:
    """
    An environment.
    """

    def __init__(self, width, height, cell_type="empty", lighting=10):
        """
        Initialize the environment.
        """
        self.width = width
        self.height = height
        self.size = width * height
        self.light = False
        self.grid = [
            [Cell(x, y, cell_type, lighting) for y in range(height)]
            for x in range(width)
        ]
        self.killed_before = []

        self.new_cells = []

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

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_organisms(self):
        organisms = []
        for row in self.grid:
            for cell in row:
                if cell.get_type() == "organism":
                    organisms.append(cell.organism)
        return organisms

    def run_authomatons(self):

        organsims = self.get_organisms()
        for organism in organsims:
            organism.make_move()

    def get_cells_pos(self, cell_type="empty"):
        """
        Return the positions of all cells of the specified type.
        """
        cell_type = cell_type
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

    def get_neighbors(self, x, y, see_dist=1):
        """
        Gets the neighbors of a cell at the specified coordinates.
        """
        output = []

        for i in range(-see_dist, see_dist + 1):
            for j in range(-see_dist, see_dist + 1):
                try:

                    output.append(self.get_cell(x + i, y + j)) if (x + i, y + j) != (
                        x,
                        y,
                    ) and x + i >= 0 and y + j >= 0 else 1
                except IndexError:
                    pass
        return output

    def get_environment_state(self):
        """
        Return the environment state.
        """
        states = []
        for row in self.grid:
            for cell in row:
                states.append(cell.get_type())

        return states

    def lighting(self, y):
        """
        Return coefficient of external illumination
        0 <= coefficient <= 1
        """
        return (self.height - y) / self.height

    def set_light(self, boolean):
        """
        change cell.light for every object in grid
        """
        for width in self.grid:
            for item in width:
                item.light = boolean
